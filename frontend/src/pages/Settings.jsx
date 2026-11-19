
import { useEffect, useState } from "react";
import api from "../services/api";

function Settings() {
  const [settings, setSettings] = useState({
    email_notifications: true,
    theme: "light",
  });

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await api.get("auth/settings/");
        setSettings(response.data);
      } catch (err) {
        setError(
          JSON.stringify(err.response?.data || "Unable to load settings.")
        );
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await api.patch("auth/settings/", settings);
      setSettings(response.data);
      setMessage("Settings saved successfully!");
    } catch (err) {
      setError(
        JSON.stringify(err.response?.data || "Unable to save settings.")
      );
    }
  };

  if (loading) return <p>Loading settings...</p>;

  return (
    <div className="content-card">
      <h2>Account Settings</h2>

      {error && <p className="error">{error}</p>}
      {message && <p className="success-message">{message}</p>}

      <form className="settings-form" onSubmit={handleSave}>
        <label>
          <input
            type="checkbox"
            checked={settings.email_notifications}
            onChange={(e) =>
              setSettings({
                ...settings,
                email_notifications: e.target.checked,
              })
            }
          />
          Enable email notifications
        </label>

        <label htmlFor="theme">Theme</label>

        <select
          id="theme"
          value={settings.theme}
          onChange={(e) =>
            setSettings({
              ...settings,
              theme: e.target.value,
            })
          }
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>

        <button type="submit">Save Settings</button>
      </form>
    </div>
  );
}

export default Settings;
