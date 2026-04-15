import API from "../api/api";
import { useState, useEffect } from "react";
import "./panel.css";

export default function Profile({ user, onLogout }) {
  const [name, setName] = useState("");
  const [msg, setMsg] = useState(null);

  useEffect(() => {
  const saved = localStorage.getItem("profile_name");

    setTimeout(() => {
        setName(saved || user);
    }, 0);

    }, [user]);

async function save() {
  try {
    await API.put("/me", {
      name: name,
    });

    setMsg("Saved!");
    setTimeout(() => setMsg(null), 2000);

  } catch (e) {
    console.log("PROFILE ERROR:", e.response); // 👈 IMPORTANT DEBUG

    setMsg(
      e.response?.data?.detail || "Update failed"
    );

    setTimeout(() => setMsg(null), 2000);
  }
}

  return (
    <div className="profile-container">

      {/* Header */}
      <div className="profile-header">
        <div className="profile-avatar">
          {name ? name[0].toUpperCase() : "U"}
        </div>

        <div>
          <p className="profile-name">{name}</p>
          <p className="profile-sub">@{user}</p>
        </div>
      </div>

      {/* Divider */}
      <div className="divider" />

      {/* Name Edit */}
      <div className="field">
        <label>Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <button className="btn btn-primary" onClick={save}>
        Save Changes
      </button>

      {msg && <div className="toast ok">{msg}</div>}

      {/* Divider */}
      <div className="divider" />

      {/* Menu */}
      <div className="profile-menu">
        <div className="menu-item">⚙ Settings</div>
        <div className="menu-item">🎨 Appearance</div>
        <div className="menu-item">🔒 Security</div>

        <div className="menu-item" onClick={onLogout}>
          🚪 Sign out
        </div>
      </div>

    </div>
  );
}