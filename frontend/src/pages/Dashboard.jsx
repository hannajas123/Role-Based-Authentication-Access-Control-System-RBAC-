
import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard({ user, onNavigate }) {
  const [stats, setStats] = useState({
    usersCount: 0,
    rolesCount: 0,
    employeesCount: 0,
    reportsCount: 0,
  });
  const [employeeProfile, setEmployeeProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);

        if (user.role === "Administrator") {
          const [usersRes, rolesRes, empRes, repRes] = await Promise.allSettled([
            api.get("auth/users/"),
            api.get("roles/roles/"),
            api.get("employees/"),
            api.get("reports/"),
          ]);

          setStats({
            usersCount: usersRes.status === "fulfilled" ? usersRes.value.data.length : 0,
            rolesCount: rolesRes.status === "fulfilled" ? rolesRes.value.data.length : 0,
            employeesCount: empRes.status === "fulfilled" ? empRes.value.data.length : 0,
            reportsCount: repRes.status === "fulfilled" ? repRes.value.data.length : 0,
          });
        } else if (user.role === "HR Manager" || user.role === "HR Executive") {
          const [empRes, repRes] = await Promise.allSettled([
            api.get("employees/"),
            api.get("reports/"),
          ]);
          setStats((prev) => ({
            ...prev,
            employeesCount: empRes.status === "fulfilled" ? empRes.value.data.length : 0,
            reportsCount: repRes.status === "fulfilled" ? repRes.value.data.length : 0,
          }));
        } else if (user.role === "Finance Manager") {
          const repRes = await api.get("reports/").catch(() => ({ data: [] }));
          setStats((prev) => ({
            ...prev,
            reportsCount: repRes.data ? repRes.data.length : 0,
          }));
        }

        // Fetch personal profile for all users
        try {
          const profileRes = await api.get("employees/me/");
          setEmployeeProfile(profileRes.data);
        } catch {
          // Employee profile might not exist for some test users
        }
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user]);

  // Navigate helper
  const goTo = (path) => {
    if (onNavigate) {
      onNavigate(path);
    }
  };

  // 1. Administrator Dashboard
  if (user.role === "Administrator") {
    return (
      <div className="dashboard-view">
        <div className="role-banner admin-banner">
          <div>
            <h2>Administrator Dashboard</h2>
            <p>Welcome back, <strong>{user.username}</strong>! Complete system access granted.</p>
          </div>
          <span className="role-tag admin-tag">System Admin</span>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Registered Users</h3>
            <p className="stat-number">{loading ? "..." : stats.usersCount}</p>
            <button onClick={() => goTo("/users")}>Manage Users →</button>
          </div>

          <div className="stat-card">
            <h3>Active Roles</h3>
            <p className="stat-number">{loading ? "..." : stats.rolesCount}</p>
            <button onClick={() => goTo("/roles")}>Configure Roles →</button>
          </div>

          <div className="stat-card">
            <h3>Employee Records</h3>
            <p className="stat-number">{loading ? "..." : stats.employeesCount}</p>
            <button onClick={() => goTo("/employees")}>View Directory →</button>
          </div>

          <div className="stat-card">
            <h3>System Reports</h3>
            <p className="stat-number">{loading ? "..." : stats.reportsCount}</p>
            <button onClick={() => goTo("/reports")}>Access Reports →</button>
          </div>
        </div>

        <div className="dashboard-sections-grid">
          <div className="content-card">
            <h3>Quick Administration</h3>
            <div className="quick-action-buttons">
              <button onClick={() => goTo("/users")}>+ Add New User</button>
              <button onClick={() => goTo("/roles")}>+ Create New Role</button>
              <button onClick={() => goTo("/permissions")}>⚙ Permission Matrix</button>
              <button onClick={() => goTo("/reports")}>📊 View All Reports</button>
            </div>
          </div>

          <div className="content-card">
            <h3>System Security & RBAC Status</h3>
            <ul className="security-checklist">
              <li>✅ <strong>JWT Authentication:</strong> Active (Access + Refresh Token Rotation)</li>
              <li>✅ <strong>Backend Permission Guards:</strong> Enforced via <code>HasModulePermission</code></li>
              <li>✅ <strong>Database:</strong> PostgreSQL (ACID Compliant)</li>
              <li>✅ <strong>Administrator Role Protection:</strong> Cannot be deleted or modified</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // 2. HR Manager Dashboard
  if (user.role === "HR Manager") {
    return (
      <div className="dashboard-view">
        <div className="role-banner hr-banner">
          <div>
            <h2>HR Management Dashboard</h2>
            <p>Welcome, <strong>{user.username}</strong>. Full access to Employee records and HR reports.</p>
          </div>
          <span className="role-tag hr-tag">HR Manager</span>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Employees</h3>
            <p className="stat-number">{loading ? "..." : stats.employeesCount}</p>
            <button onClick={() => goTo("/employees")}>Manage Employees →</button>
          </div>

          <div className="stat-card">
            <h3>HR Reports</h3>
            <p className="stat-number">{loading ? "..." : stats.reportsCount}</p>
            <button onClick={() => goTo("/reports")}>Generate Reports →</button>
          </div>
        </div>

        <div className="content-card">
          <h3>HR Quick Actions</h3>
          <div className="quick-action-buttons">
            <button onClick={() => goTo("/employees")}>+ Register New Employee</button>
            <button onClick={() => goTo("/reports")}>📊 Generate Headcount Report</button>
            <button onClick={() => goTo("/profile")}>👤 My Profile</button>
          </div>
        </div>
      </div>
    );
  }

  // 3. HR Executive Dashboard
  if (user.role === "HR Executive") {
    return (
      <div className="dashboard-view">
        <div className="role-banner hrexec-banner">
          <div>
            <h2>HR Executive Dashboard</h2>
            <p>Welcome, <strong>{user.username}</strong>. View and create employee records.</p>
          </div>
          <span className="role-tag hrexec-tag">HR Executive</span>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Employee Directory</h3>
            <p className="stat-number">{loading ? "..." : stats.employeesCount}</p>
            <button onClick={() => goTo("/employees")}>View Directory →</button>
          </div>
        </div>

        <div className="content-card">
          <h3>Your Scope of Access</h3>
          <p>
            You are authorized to <strong>View</strong> and <strong>Create</strong> employee records.
          </p>
          <div className="info-box">
            ℹ <strong>Notice:</strong> Per RBAC policy, HR Executives cannot edit or delete existing employee records.
          </div>
          <div className="quick-action-buttons" style={{ marginTop: "15px" }}>
            <button onClick={() => goTo("/employees")}>+ Register Employee</button>
            <button onClick={() => goTo("/profile")}>👤 My Profile</button>
          </div>
        </div>
      </div>
    );
  }

  // 4. Finance Manager Dashboard
  if (user.role === "Finance Manager") {
    return (
      <div className="dashboard-view">
        <div className="role-banner finance-banner">
          <div>
            <h2>Financial Management Dashboard</h2>
            <p>Welcome, <strong>{user.username}</strong>. Access to financial data and reports.</p>
          </div>
          <span className="role-tag finance-tag">Finance Manager</span>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Financial Reports</h3>
            <p className="stat-number">{loading ? "..." : stats.reportsCount}</p>
            <button onClick={() => goTo("/reports")}>Financial Statements →</button>
          </div>
        </div>

        <div className="content-card">
          <h3>Finance Actions</h3>
          <p>You have access to generate and export financial CSV statement reports.</p>
          <div className="quick-action-buttons">
            <button onClick={() => goTo("/reports")}>📊 Generate Financial Report</button>
            <button onClick={() => goTo("/reports")}>📥 Download Statement CSV</button>
          </div>
        </div>
      </div>
    );
  }

  // 5. Employee Personal Dashboard (Default)
  return (
    <div className="dashboard-view">
      <div className="role-banner employee-banner">
        <div>
          <h2>Employee Personal Dashboard</h2>
          <p>Welcome back, <strong>{user.username}</strong>!</p>
        </div>
        <span className="role-tag employee-tag">Employee</span>
      </div>

      <div className="dashboard-sections-grid">
        <div className="content-card">
          <h3>My Profile Snapshot</h3>
          {employeeProfile ? (
            <div className="profile-details">
              <p><strong>Employee ID:</strong> {employeeProfile.employee_id}</p>
              <p><strong>Department:</strong> {employeeProfile.department}</p>
              <p><strong>Designation:</strong> {employeeProfile.designation}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Date of Joining:</strong> {employeeProfile.date_of_joining || "N/A"}</p>
            </div>
          ) : (
            <p>Standard employee account. Access to personal dashboard and permitted profile information.</p>
          )}
          <button onClick={() => goTo("/profile")} style={{ marginTop: "15px" }}>
            View Full Profile →
          </button>
        </div>

        <div className="content-card">
          <h3>My Permitted Modules</h3>
          <p>Your current assigned permissions:</p>
          <ul style={{ paddingLeft: "20px", color: "#555" }}>
            {user.permissions && user.permissions.length > 0 ? (
              user.permissions.map((p, idx) => (
                <li key={idx}>
                  <strong>{p.module}</strong>: {p.action}
                </li>
              ))
            ) : (
              <li>Dashboard: View</li>
            )}
          </ul>
          <button onClick={() => goTo("/settings")} style={{ marginTop: "15px" }}>
            Account Settings →
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
