
import { canAccessModule } from "../services/permissions";


function Sidebar({ user, activePage, setActivePage }) {
  const menuItems = [
    { name: "Dashboard", module: "Dashboard" },
    { name: "User Management", module: "User Management" },
    { name: "Role Management", module: "Role Management" },
    { name: "Employee Management", module: "Employee Management" },
    { name: "Reports", module: "Reports" },
    { name: "Settings", module: "Settings" },
  ];

  return (
    <aside className="sidebar">
      <h2>RBAC System</h2>

      <div className="user-info">
        <strong>{user.username}</strong>
        <p>{user.role}</p>
      </div>

      <nav>
        {menuItems.map((item) => {
          if (!canAccessModule(user, item.module)) return null;

          return (
            <button
              key={item.name}
              className={
                activePage === item.name ? "active-menu" : ""
              }
              onClick={() => setActivePage(item.name)}
            >
              {item.name}
            </button>
          );
        })}

        <button
          className={activePage === "User Profile" ? "active-menu" : ""}
          onClick={() => setActivePage("User Profile")}
        >
          User Profile
        </button>
      </nav>
    </aside>
  );
}

export default Sidebar;
