
import { useEffect, useState } from "react";
import api from "../services/api";
import {
  hasPermission,
} from "../services/permissions";

function UserManagement({ user }) {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role_id: "",
    is_active: true,
  });

  const canCreate = hasPermission(user, "User Management", "Create");
  const canEdit = hasPermission(user, "User Management", "Edit");
  const canDelete = hasPermission(user, "User Management", "Delete");

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [userResponse, roleResponse] = await Promise.all([
        api.get("auth/users/"),
        api.get("roles/roles/"),
      ]);

      setUsers(userResponse.data);
      setRoles(roleResponse.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load users. Check your API permissions."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const resetForm = () => {
    setEditingId(null);
    setForm({
      username: "",
      email: "",
      password: "",
      role_id: "",
      is_active: true,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const payload = {
      ...form,
      role_id: form.role_id ? Number(form.role_id) : null,
    };

    if (!payload.password) {
      delete payload.password;
    }

    try {
      if (editingId) {
        await api.patch(`auth/users/${editingId}/`, payload);
      } else {
        await api.post("auth/users/", payload);
      }

      resetForm();
      await loadData();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to save user.")
      );
    }
  };

  const handleEdit = (selectedUser) => {
    setEditingId(selectedUser.id);

    setForm({
      username: selectedUser.username,
      email: selectedUser.email,
      password: "",
      role_id: selectedUser.role_id || "",
      is_active: selectedUser.is_active,
    });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) {
      return;
    }

    try {
      await api.delete(`auth/users/${id}/`);
      await loadData();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to delete user.")
      );
    }
  };

  if (loading) return <p>Loading users...</p>;

  return (
    <div className="content-card">
      <h2>User Management</h2>

      {error && <p className="error">{error}</p>}

      {(canCreate || (editingId && canEdit)) && (
        <form onSubmit={handleSubmit} className="user-form">
          <h3>{editingId ? "Edit User" : "Create User"}</h3>

          <input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            required
          />

          <input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            name="password"
            type="password"
            placeholder={editingId ? "New password (optional)" : "Password"}
            value={form.password}
            onChange={handleChange}
            required={!editingId}
            minLength={8}
          />

          <select
            name="role_id"
            value={form.role_id}
            onChange={handleChange}
          >
            <option value="">Select Role</option>

            {roles.map((role) => (
              <option key={role.id} value={role.id}>
                {role.name}
              </option>
            ))}
          </select>

          <label>
            <input
              type="checkbox"
              name="is_active"
              checked={form.is_active}
              onChange={handleChange}
            />
            Active User
          </label>

          <button type="submit">
            {editingId ? "Update User" : "Create User"}
          </button>

          {editingId && (
            <button type="button" onClick={resetForm}>
              Cancel
            </button>
          )}
        </form>
      )}

      <h3>Registered Users</h3>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {users.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.username}</td>
                <td>{item.email}</td>
                <td>{item.role_name || "No role"}</td>
                <td>{item.is_active ? "Active" : "Inactive"}</td>

                <td>
                  {canEdit && (
                    <button onClick={() => handleEdit(item)}>
                      Edit
                    </button>
                  )}

                  {canDelete && (
                    <button
                      className="delete-button"
                      onClick={() => handleDelete(item.id)}
                    >
                      Delete
                    </button>
                  )}
                </td>
              </tr>
            ))}

            {users.length === 0 && (
              <tr>
                <td colSpan="6">No users found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default UserManagement;
