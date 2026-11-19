
import { useEffect, useState } from "react";
import api from "../services/api";

function RoleManagement() {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);
  const [selectedPermissions, setSelectedPermissions] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadRoles = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("roles/roles/");
      const data = response.data;

      setRoles(data);

      // The Administrator role contains the full permission catalogue.
      const adminRole = data.find(
        (role) => role.name === "Administrator"
      );

      if (adminRole) {
        setPermissions(adminRole.permissions || []);
      }
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to load roles.")
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRoles();
  }, []);

  const handleSelectRole = (role) => {
    setSelectedRole(role);
    setName(role.name);
    setDescription(role.description || "");

    setSelectedPermissions(
      (role.permissions || []).map((permission) => permission.id)
    );
  };

  const handlePermissionChange = (permissionId) => {
    setSelectedPermissions((previous) =>
      previous.includes(permissionId)
        ? previous.filter((id) => id !== permissionId)
        : [...previous, permissionId]
    );
  };

  const handleCreateRole = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await api.post("roles/roles/", {
        name,
        description,
        permission_ids: selectedPermissions,
      });

      setName("");
      setDescription("");
      setSelectedPermissions([]);
      setSelectedRole(null);

      await loadRoles();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to create role.")
      );
    }
  };

  const handleUpdateRole = async () => {
    if (!selectedRole) return;

    try {
      await api.patch(`roles/roles/${selectedRole.id}/`, {
        name,
        description,
        permission_ids: selectedPermissions,
      });

      setSelectedRole(null);
      setName("");
      setDescription("");
      setSelectedPermissions([]);

      await loadRoles();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to update role.")
      );
    }
  };

  const handleDeleteRole = async (role) => {
    if (role.name === "Administrator") {
      setError("The Administrator role cannot be deleted.");
      return;
    }

    if (!window.confirm(`Delete the ${role.name} role?`)) return;

    try {
      await api.delete(`roles/roles/${role.id}/`);
      setSelectedRole(null);
      await loadRoles();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to delete role.")
      );
    }
  };

  if (loading) return <p>Loading roles...</p>;

  return (
    <div className="content-card">
      <h2>Role Management</h2>

      {error && <p className="error">{error}</p>}

      <div className="role-list">
        <h3>Available Roles</h3>

        {roles.map((role) => (
          <div className="role-item" key={role.id}>
            <div>
              <strong>{role.name}</strong>
              <p>{role.description}</p>
              <small>
                {role.permissions?.length || 0} permissions
              </small>
            </div>

            <div>
              <button onClick={() => handleSelectRole(role)}>
                Edit Permissions
              </button>

              {role.name !== "Administrator" && (
                <button
                  className="delete-button"
                  onClick={() => handleDeleteRole(role)}
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <hr />

      <h3>
        {selectedRole
          ? `Edit ${selectedRole.name}`
          : "Create New Role"}
      </h3>

      <form
        className="role-form"
        onSubmit={
          selectedRole
            ? (e) => {
                e.preventDefault();
                handleUpdateRole();
              }
            : handleCreateRole
        }
      >
        <input
          placeholder="Role Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          disabled={selectedRole?.name === "Administrator"}
        />

        <textarea
          placeholder="Role Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <h4>Assign Permissions</h4>

        {permissions.map((permission) => (
          <label className="permission-item" key={permission.id}>
            <input
              type="checkbox"
              checked={selectedPermissions.includes(permission.id)}
              onChange={() => handlePermissionChange(permission.id)}
              disabled={selectedRole?.name === "Administrator"}
            />

            {permission.module} - {permission.action}
          </label>
        ))}

        <button type="submit">
          {selectedRole ? "Save Changes" : "Create Role"}
        </button>

        {selectedRole && (
          <button
            type="button"
            onClick={() => {
              setSelectedRole(null);
              setName("");
              setDescription("");
              setSelectedPermissions([]);
            }}
          >
            Cancel
          </button>
        )}
      </form>
    </div>
  );
}

export default RoleManagement;
