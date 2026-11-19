import UserManagement from "../pages/UserManagement";

function Dashboard({ user, onLogout }) {
    if (activePage === "User Management") {
  return <UserManagement user={user} />;
}
  return (
    <div className="dashboard">
      <header>
        <h1>RBAC Dashboard</h1>
        <button onClick={onLogout}>Logout</button>
      </header>

      <section className="welcome-card">
        <h2>Welcome, {user.username}!</h2>
        <p>Email: {user.email}</p>
        <p>Role: {user.role || "No role assigned"}</p>
      </section>

      <section className="permissions-card">
        <h2>Your Permissions</h2>

        {user.permissions?.length > 0 ? (
          <ul>
            {user.permissions.map((permission, index) => (
              <li key={index}>{permission}</li>
            ))}
          </ul>
        ) : (
          <p>No permissions assigned.</p>
        )}
      </section>
    </div>
  );
}

export default Dashboard;
