import { useState } from "react";
import API from "../api/api";
import "./panel.css";

export default function Login({ onLogin }) {
  const [tab, setTab] = useState("login");

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) =>
    setForm((p) => ({ ...p, [k]: e.target.value }));

  async function submit() {
    // 🔥 FIX: validation first
    if (!form.username || !form.password) {
      setMsg({ text: "Enter username & password", type: "err" });
      return;
    }

    setMsg(null);
    setLoading(true);

    try {
      if (tab === "login") {
        const r = await API.post("/login", {
          username: form.username,
          password: form.password,
        });

        localStorage.setItem("token", r.data.access_token);

        onLogin(form.username);
      } else {
        // ✅ signup
        await API.post("/signup", {
          username: form.username,
          password: form.password,
          name: form.username,
        });

        // 🔐 auto login
        const r = await API.post("/login", {
          username: form.username,
          password: form.password,
        });

        localStorage.setItem("token", r.data.access_token);

        onLogin(form.username);

        setMsg({ text: "Account created!", type: "ok" });
        setTab("login");
      }

    } catch (e) {
      setMsg({
        text: e.response?.data?.detail || "Something went wrong.",
        type: "err",
      });
    } finally {
      setLoading(false); // 🔥 always stop loading
    }
  }

  return (
    <div className="page-center">
      <div className="wrap">

        <div className="orb" />

        <div className="logo">
          <span className="logoMark">V</span>

          <div>
            <h1 className="logoName">VaultX</h1>
            <p className="tagline">
              Save money & get best financial experience
            </p>
          </div>
        </div>

        <div className="tabs">
          {["login", "signup"].map((t) => (
            <button
              key={t}
              className={`tab ${tab === t ? "active" : ""}`}
              onClick={() => setTab(t)}
            >
              {t === "login" ? "Sign In" : "Sign Up"}
            </button>
          ))}
        </div>

        <div className="field">
          <label>Username</label>
          <input
            placeholder="username"
            value={form.username}
            onChange={set("username")}
          />
        </div>

        <div className="field">
          <label>Password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={form.password}
            onChange={set("password")}
          />
        </div>

        <button
          className="btn btn-primary"
          onClick={submit}
          disabled={loading}
        >
          {loading
            ? "Processing..."
            : tab === "login"
            ? "Continue →"
            : "Create Account →"}
        </button>

        {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}

        <div className="auth-box">
          <div className="switch">
            Don't have an account?
            <span onClick={() => setTab(tab === "login" ? "signup" : "login")}>
              Sign up
            </span>
          </div>
        </div>

      </div>
    </div>
  );
}