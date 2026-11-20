
import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
  Link,
} from "react-router-dom";
import Login from "./pages/Login";
import DashboardLayout from "./components/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import UserManagement from "./pages/UserManagement";
import RoleManagement from "./pages/RoleManagement";
import PermissionManagement from "./pages/PermissionManagement";
import EmployeeManagement from "./pages/EmployeeManagement";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import UserProfile from "./pages/UserProfile";
import { hasPermission } from "./services/permissions";
import api from "./services/api";
import "./App.css";

function ProtectedRoute({ user, module, action = "View", children }) {
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (module && !hasPermission(user, module, action)) {
    return (
      <div className="content-card access-denied-card">
        <h2>403 - Access Denied</h2>
        <p>
          You do not have permission to access the <strong>{module}</strong> module.
        </p>
        <p>
          Current Assigned Role: <strong>{user.role || "None"}</strong>
        </p>
        <Link to="/dashboard">
          <button style={{ marginTop: "15px" }}>Return to Dashboard</button>
        </Link>
      </div>
    );
  }

  return children;
}

function AppContent() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    try {
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const navigate = useNavigate();

  const handleLogin = (userData) => {
    setUser(userData);
    navigate("/dashboard");
  };

  const handleLogout = async () => {
    const refresh = localStorage.getItem("refresh_token");

    try {
      if (refresh) {
        await api.post("auth/logout/", { refresh });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      setUser(null);
      navigate("/login");
    }
  };

  return (
    <Routes>
      <Route
        path="/login"
        element={
          user ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Login onLogin={handleLogin} />
          )
        }
      />

      <Route
        element={
          user ? (
            <DashboardLayout user={user} onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      >
        <Route
          path="/dashboard"
          element={<Dashboard user={user} onNavigate={(path) => navigate(path)} />}
        />
        <Route
          path="/users"
          element={
            <ProtectedRoute user={user} module="User Management">
              <UserManagement user={user} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/roles"
          element={
            <ProtectedRoute user={user} module="Role Management">
              <RoleManagement />
            </ProtectedRoute>
          }
        />
        <Route
          path="/permissions"
          element={
            <ProtectedRoute user={user} module="Role Management">
              <PermissionManagement />
            </ProtectedRoute>
          }
        />
        <Route
          path="/employees"
          element={
            <ProtectedRoute user={user} module="Employee Management">
              <EmployeeManagement user={user} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute user={user} module="Reports">
              <Reports user={user} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute user={user} module="Settings">
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute user={user}>
              <UserProfile user={user} />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
