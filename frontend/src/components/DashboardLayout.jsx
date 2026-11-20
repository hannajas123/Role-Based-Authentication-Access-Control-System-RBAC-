
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";

function DashboardLayout({ user, onLogout }) {
  const location = useLocation();

  const getPageTitle = (pathname) => {
    switch (pathname) {
      case "/dashboard":
        return "Dashboard";
      case "/users":
        return "User Management";
      case "/roles":
        return "Role Management";
      case "/permissions":
        return "Permission Management";
      case "/employees":
        return "Employee Management";
      case "/reports":
        return "Reports Management";
      case "/settings":
        return "System Settings";
      case "/profile":
        return "User Profile";
      default:
        return "RBAC System";
    }
  };

  return (
    <div className="app-layout">
      <Sidebar user={user} />

      <main className="main-content">
        <header className="topbar">
          <h2>{getPageTitle(location.pathname)}</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
            <span style={{ fontSize: "14px", color: "#666" }}>
              Logged in: <strong>{user.username}</strong> ({user.role || "No Role"})
            </span>
            <button onClick={onLogout}>Logout</button>
          </div>
        </header>

        <Outlet />
      </main>
    </div>
  );
}

export default DashboardLayout;
