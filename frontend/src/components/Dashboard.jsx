import { useState, useEffect } from "react";
import API from "../api/api";

import AccountsList from "./AccountsList";
import CreateAccount from "./CreateAccount";
import Deposit from "./Deposit";
import Withdraw from "./Withdraw";
import Transfer from "./Transfer";
import Profile from "./Profile";

import "./panel.css";

const fmt = (n) =>
  "₹" +
  Number(n || 0).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
  });

export default function Dashboard({ user, onLogout }) {
  const [accounts, setAccounts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [panel, setPanel] = useState(null);
  const [dark, setDark] = useState(true);
  const [showProfile, setShowProfile] = useState(false);
  const [tab, setTab] = useState("home");

  const selAcc = accounts.find(
    (a) => Number(a.id) === Number(selected)
  );

  const hasAccounts = accounts.length > 0;

  async function loadAccounts() {
    try {
      const r = await API.get("/accounts");
      const data = r.data;

      setAccounts(data);

      if (data.length === 0) {
        setSelected(null);
        return;
      }

      const exists = data.some((a) => a.id === selected);

      if (!selected || !exists) {
        setSelected(Number(data[0].id));
      }
    } catch (err) {
      console.error("Failed to load accounts:", err);
    }
  }

  useEffect(() => {
    loadAccounts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={`app-shell ${dark ? "dark" : "light"}`}>
      
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div
            className="avatar clickable"
            onClick={() => setShowProfile(true)}
          >
            {user ? user[0].toUpperCase() : "U"}
          </div>

          <div>
            <p className="greeting">Welcome Back</p>
            <p className="username">{user}</p>
          </div>
        </div>

        <button
          className="theme-toggle"
          onClick={() => setDark(!dark)}
        >
          <span className="icon">
            {dark ? "☀️" : "🌙"}
          </span>
          <span className="label">
            {dark ? "Light Mode" : "Dark Mode"}
          </span>
        </button>

        <button className="logout-btn" onClick={onLogout}>
          Sign out
        </button>
      </header>

      {/* 🔥 HOME TAB */}
      {tab === "home" && (
        <>
          <div className="hero">
            <p className="hero-label">Cash Balance</p>

            <p style={{ opacity: 0.6 }}>
              {selAcc?.account_name || "Account"} • #{selAcc?.acc_no || "-"}
            </p>

            <p className="hero-amount">
              {fmt(selAcc?.balance || 0)}
            </p>

            <div className="hero-actions">
              <button
                disabled={!hasAccounts}
                onClick={() => setPanel("deposit")}
              >
                Add Cash
              </button>

              <button
                disabled={!hasAccounts}
                onClick={() => setPanel("transfer")}
              >
                Send Money
              </button>
            </div>
          </div>

          <AccountsList
            accounts={accounts}
            selected={selected}
            onSelect={setSelected}
          />
        </>
      )}

      {/* ⚡ ACTIONS TAB */}
      {tab === "actions" && (
        <div className="quick-actions">
          {[
            { label: "Deposit", action: "deposit" },
            { label: "Withdraw", action: "withdraw" },
            { label: "Transfer", action: "transfer" },
            { label: "New Acc", action: "new" },
          ].map(({ label, action }) => (
            <button key={action} onClick={() => setPanel(action)}>
              {label}
            </button>
          ))}
        </div>
      )}

      {/* 👤 PROFILE TAB */}
      {tab === "profile" && (
        <Profile user={user} onLogout={onLogout} />
      )}

      {/* Panels */}
      {panel === "deposit" && selected && (
        <Deposit accountId={selected} onDone={loadAccounts} />
      )}

      {panel === "withdraw" && selected && (
        <Withdraw accountId={selected} onDone={loadAccounts} />
      )}

      {panel === "transfer" && selected && (
        <Transfer
          accountId={selected}
          fromAccNo={selAcc?.acc_no}
          onDone={loadAccounts}
        />
      )}

      {panel === "new" && (
        <CreateAccount onDone={loadAccounts} />
      )}

      {/* 🔥 PROFILE DRAWER (still works) */}
      {showProfile && (
        <>
          <div
            className="overlay"
            onClick={() => setShowProfile(false)}
          />

          <div className={`profile-drawer ${showProfile ? "open" : ""}`}>
            <Profile user={user} onLogout={onLogout} />
          </div>
        </>
      )}

      {/* 🔥 BOTTOM NAV */}
      <div className="bottom-nav">
        <button
          className={tab === "home" ? "active" : ""}
          onClick={() => setTab("home")}
        >
          🏠 Home
        </button>

        <button
          className={tab === "actions" ? "active" : ""}
          onClick={() => setTab("actions")}
        >
          ⚡ Actions
        </button>

        <button
          className={tab === "profile" ? "active" : ""}
          onClick={() => setTab("profile")}
        >
          👤 Profile
        </button>
      </div>

    </div>
  );
}