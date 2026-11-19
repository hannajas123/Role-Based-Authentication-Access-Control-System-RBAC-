
import { useEffect, useState } from "react";
import api from "../services/api";
import { hasPermission } from "../services/permissions";

function EmployeeManagement({ user }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    employee_id: "",
    department: "",
    designation: "",
    phone: "",
    address: "",
    date_of_joining: "",
  });

  const canView = hasPermission(user, "Employee Management", "View");
  const canCreate = hasPermission(user, "Employee Management", "Create");
  const canEdit = hasPermission(user, "Employee Management", "Edit");
  const canDelete = hasPermission(user, "Employee Management", "Delete");

  const loadEmployees = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("employees/");
      setEmployees(response.data);
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to load employees.")
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEmployees();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const resetForm = () => {
    setEditingId(null);
    setForm({
      username: "",
      email: "",
      password: "",
      employee_id: "",
      department: "",
      designation: "",
      phone: "",
      address: "",
      date_of_joining: "",
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      if (editingId) {
        const payload = {
          department: form.department,
          designation: form.designation,
          phone: form.phone,
          address: form.address,
          date_of_joining: form.date_of_joining || null,
        };

        await api.patch(`employees/${editingId}/`, payload);
      } else {
        await api.post("employees/", {
          ...form,
          date_of_joining: form.date_of_joining || null,
        });
      }

      resetForm();
      await loadEmployees();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to save employee.")
      );
    }
  };

  const handleEdit = (employee) => {
    setEditingId(employee.id);

    setForm({
      username: employee.username,
      email: employee.email,
      password: "",
      employee_id: employee.employee_id,
      department: employee.department,
      designation: employee.designation,
      phone: employee.phone || "",
      address: employee.address || "",
      date_of_joining: employee.date_of_joining || "",
    });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this employee?")) {
      return;
    }

    try {
      await api.delete(`employees/${id}/`);
      await loadEmployees();
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to delete employee.")
      );
    }
  };

  if (!canView) {
    return (
      <div className="content-card">
        <h2>Access Denied</h2>
        <p>You do not have permission to view employee records.</p>
      </div>
    );
  }

  if (loading) return <p>Loading employees...</p>;

  return (
    <div className="content-card">
      <h2>Employee Management</h2>

      {error && <p className="error">{error}</p>}

      {(canCreate || (editingId && canEdit)) && (
        <form className="employee-form" onSubmit={handleSubmit}>
          <h3>{editingId ? "Edit Employee" : "Create Employee"}</h3>

          {!editingId && (
            <>
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
                placeholder="Initial Password (minimum 8 characters)"
                value={form.password}
                onChange={handleChange}
                minLength={8}
                required
              />

              <input
                name="employee_id"
                placeholder="Employee ID"
                value={form.employee_id}
                onChange={handleChange}
                required
              />
            </>
          )}

          {editingId && (
            <p>
              Employee: <strong>{form.username}</strong> ({form.employee_id})
            </p>
          )}

          <input
            name="department"
            placeholder="Department"
            value={form.department}
            onChange={handleChange}
            required
          />

          <input
            name="designation"
            placeholder="Designation"
            value={form.designation}
            onChange={handleChange}
            required
          />

          <input
            name="phone"
            placeholder="Phone"
            value={form.phone}
            onChange={handleChange}
          />

          <textarea
            name="address"
            placeholder="Address"
            value={form.address}
            onChange={handleChange}
          />

          <label>Date of Joining</label>
          <input
            name="date_of_joining"
            type="date"
            value={form.date_of_joining}
            onChange={handleChange}
          />

          <div className="form-actions">
            <button type="submit">
              {editingId ? "Update Employee" : "Create Employee"}
            </button>

            {editingId && (
              <button type="button" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
      )}

      <h3>Employee Records</h3>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Department</th>
              <th>Designation</th>
              <th>Phone</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.employee_id}</td>
                <td>{employee.username}</td>
                <td>{employee.email}</td>
                <td>{employee.department}</td>
                <td>{employee.designation}</td>
                <td>{employee.phone}</td>
                <td>
                  {canEdit && (
                    <button onClick={() => handleEdit(employee)}>
                      Edit
                    </button>
                  )}

                  {canDelete && (
                    <button
                      className="delete-button"
                      onClick={() => handleDelete(employee.id)}
                    >
                      Delete
                    </button>
                  )}
                </td>
              </tr>
            ))}

            {employees.length === 0 && (
              <tr>
                <td colSpan="7">No employee records found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EmployeeManagement;
