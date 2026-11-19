
import { useEffect, useState } from "react";
import api from "../services/api";

function UserProfile({ user }) {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await api.get("employees/me/");
        setEmployee(response.data);
      } catch (err) {
        // A user may not have an employee profile.
        setError(
          err.response?.data?.detail ||
          "No employee profile is available for this account."
        );
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, []);

  return (
    <div className="content-card">
      <h2>My Profile</h2>

      <div className="profile-details">
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Role:</strong> {user.role || "Not assigned"}</p>
      </div>

      <hr />

      <h3>Employee Information</h3>

      {loading && <p>Loading employee profile...</p>}

      {!loading && employee && (
        <div className="profile-details">
          <p><strong>Employee ID:</strong> {employee.employee_id}</p>
          <p><strong>Department:</strong> {employee.department}</p>
          <p><strong>Designation:</strong> {employee.designation}</p>
          <p><strong>Phone:</strong> {employee.phone || "Not provided"}</p>
          <p><strong>Address:</strong> {employee.address || "Not provided"}</p>
          <p>
            <strong>Date of Joining:</strong>{" "}
            {employee.date_of_joining || "Not provided"}
          </p>
        </div>
      )}

      {!loading && error && <p>{error}</p>}
    </div>
  );
}

export default UserProfile;
