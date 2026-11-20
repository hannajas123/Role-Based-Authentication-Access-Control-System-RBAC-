
import { useEffect, useState } from "react";
import api from "../services/api";

function PermissionManagement() {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingRoleId, setSavingRoleId] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Map of roleId -> Set of permission IDs
  const [rolePermMap, setRolePermMap] = useState({});

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");
      const [rolesRes, permsRes] = await Promise.all([
        api.get("roles/roles/"),
        api.get("roles/permissions/"),
      ]);

      const loadedRoles = rolesRes.data;
      const loadedPerms = permsRes.data;

      setRoles(loadedRoles);
      setPermissions(loadedPerms);

      const mapping = {};
      loadedRoles.forEach((role) => {
        mapping[role.id] = (role.permissions || []).map((p) => p.id);
      });
      setRolePermMap(mapping);
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to load roles and permissions.")
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleToggle = (roleId, permId) => {
    const role = roles.find((r) => r.id === roleId);
    if (role?.name === "Administrator") return; // Admin permissions cannot be revoked

    setRolePermMap((prev) => {
      const current = prev[roleId] || [];
      const updated = current.includes(permId)
        ? current.filter((id) => id !== permId)
        : [...current, permId];
      return { ...prev, [roleId]: updated };
    });
  };

  const handleSaveRole = async (role) => {
    if (role.name === "Administrator") return;
    setError("");
    setSuccess("");
    setSavingRoleId(role.id);

    try {
      await api.patch(`roles/roles/${role.id}/`, {
        permission_ids: rolePermMap[role.id] || [],
      });
      setSuccess(`Permissions for '${role.name}' updated successfully!`);
      await loadData();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || `Failed to update permissions for ${role.name}.`)
      );
    } finally {
      setSavingRoleId(null);
    }
  };

  if (loading) return <p>Loading permission matrix...</p>;

  // Group permissions by module
  const modules = {};
  permissions.forEach((perm) => {
    if (!modules[perm.module]) {
      modules[perm.module] = [];
    }
    modules[perm.module].push(perm);
  });

  return (
    <div className="content-card">
      <div className="permission-header">
        <h2>Permission Management Matrix</h2>
        <p>Assign module-level predefined permissions across system roles.</p>
      </div>

      {error && <p className="error">{error}</p>}
      {success && <p className="success-message">{success}</p>}

      <div className="table-wrapper">
        <table className="permission-matrix">
          <thead>
            <tr>
              <th style={{ minWidth: "220px" }}>Module & Action</th>
              {roles.map((role) => (
                <th key={role.id} style={{ textAlign: "center", minWidth: "140px" }}>
                  <div>{role.name}</div>
                  {role.name !== "Administrator" && (
                    <button
                      style={{ padding: "4px 8px", fontSize: "11px", marginTop: "5px" }}
                      onClick={() => handleSaveRole(role)}
                      disabled={savingRoleId === role.id}
                    >
                      {savingRoleId === role.id ? "Saving..." : "Save"}
                    </button>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.entries(modules).map(([moduleName, permList]) => (
              <>
                <tr key={moduleName} className="module-group-header">
                  <td
                    colSpan={roles.length + 1}
                    style={{ background: "#243b67", color: "white", fontWeight: "bold" }}
                  >
                    Module: {moduleName}
                  </td>
                </tr>
                {permList.map((perm) => (
                  <tr key={perm.id}>
                    <td>
                      <strong>{perm.action}</strong>
                      <span style={{ color: "#666", fontSize: "12px", marginLeft: "8px" }}>
                        ({moduleName})
                      </span>
                    </td>
                    {roles.map((role) => {
                      const isChecked =
                        role.name === "Administrator" ||
                        (rolePermMap[role.id] && rolePermMap[role.id].includes(perm.id));
                      const isDisabled = role.name === "Administrator";

                      return (
                        <td key={role.id} style={{ textAlign: "center" }}>
                          <input
                            type="checkbox"
                            checked={isChecked}
                            disabled={isDisabled}
                            onChange={() => handleToggle(role.id, perm.id)}
                            title={
                              isDisabled
                                ? "Administrator permissions cannot be modified"
                                : `Toggle ${perm.module} - ${perm.action} for ${role.name}`
                            }
                          />
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PermissionManagement;
