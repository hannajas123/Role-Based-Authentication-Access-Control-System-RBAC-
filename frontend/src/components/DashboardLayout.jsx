
import { useState } from "react";
import Sidebar from "./Sidebar";
import { hasPermission } from "../services/permissions";

import UserManagement from "../pages/UserManagement";
import RoleManagement from "../pages/RoleManagement";
import EmployeeManagement from "../pages/EmployeeManagement";
import Reports from "../pages/Reports";
import Settings from "../pages/Settings";
import UserProfile from "../pages/UserProfile";

function DashboardLayout({ user, onLogout }) {
  const [activePage, setActivePage] = useState("Dashboard");

  const renderPage = () => {
    // User Profile is personal information.
    if (activePage === "User Profile") {
      return <UserProfile user={user} />;
    }

    // Check View permission before opening protected modules.
    if (!hasPermission(user, activePage, "View")) {
      return (
        <div className="content-card">
          <h2>Access Denied</h2>
          <p>You do not have permission to view this module.</p>
        </div>
      );
    }

    // Dashboard
    if (activePage === "Dashboard") {
      return (
        <div className="content-card">
          <h2>Dashboard</h2>
          <p>Welcome, {user.username}!</p>
          <p>Your role: {user.role}</p>
        </div>
      );
    }

    // User Management
    if (activePage === "User Management") {
      return <UserManagement user={user} />;
    }

    // Role Management
    if (activePage === "Role Management") {
      return <RoleManagement />;
    }

    // Employee Management
    if (activePage === "Employee Management") {
      return <EmployeeManagement user={user} />;
    }

    // Reports
    if (activePage === "Reports") {
      return <Reports user={user} />;
    }

    // Settings
    if (activePage === "Settings") {
      return <Settings />;
    }

    return (
      <div className="content-card">
        <h2>Access Denied</h2>
        <p>Module not found or permission not granted.</p>
      </div>
    );
  };

  return (
    <div className="app-layout">
      <Sidebar
        user={user}
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="main-content">
        <header className="topbar">
          <h2>{activePage}</h2>
          <button onClick={onLogout}>Logout</button>
        </header>

        {renderPage()}
      </main>
    </div>
  );
}

export default DashboardLayout;
