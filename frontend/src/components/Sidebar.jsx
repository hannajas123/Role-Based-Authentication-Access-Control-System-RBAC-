
import { NavLink } from "react-router-dom";
import { canAccessModule } from "../services/permissions";

function Sidebar({ user }) {
  const menuItems = [
    { name: "Dashboard", path: "/dashboard", module: "Dashboard" },
    { name: "User Management", path: "/users", module: "User Management" },
    { name: "Role Management", path: "/roles", module: "Role Management" },
    { name: "Permission Management", path: "/permissions", module: "Role Management" },
    { name: "Employee Management", path: "/employees", module: "Employee Management" },
    { name: "Reports", path: "/reports", module: "Reports" },
    { name: "Settings", path: "/settings", module: "Settings" },
  ];

  return (
    <aside className="sidebar">
      <h2>RBAC System</h2>

      <div className="user-info">
        <strong>{user.username}</strong>
        <p>{user.role || "No role assigned"}</p>
      </div>

      <nav>
        {menuItems.map((item) => {
          if (!canAccessModule(user, item.module)) return null;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "nav-link active-menu" : "nav-link"
              }
            >
              {item.name}
            </NavLink>
          );
        })}

        <NavLink
          to="/profile"
          className={({ isActive }) =>
            isActive ? "nav-link active-menu" : "nav-link"
          }
        >
          User Profile
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
