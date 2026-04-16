import { useState, useEffect, useCallback } from "react";
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

  const [dark, setDark] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });

  const [tab, setTab] = useState("home");

  const loadAccounts = useCallback(async () => {
    try {
      const r = await API.get("/accounts");
      const data = r.data;

      setAccounts(data);

      if (data.length === 0) {
        setSelected(null);
        return;
      }

      const exists = data.some(
        (a) => Number(a.id) === Number(selected)
      );

      if (!selected || !exists) {
        setSelected(Number(data[0].id));
      }

    } catch (err) {
      console.error("Failed to load accounts:", err);
    }
  }, [selected]);

  useEffect(() => {
    async function init() {
      await loadAccounts();
    }

    init();
  }, [loadAccounts]);

  useEffect(() => {
    function updateTheme() {
      const isDark = localStorage.getItem("theme") === "dark";
      setDark(isDark);
      document.body.className = isDark ? "dark" : "light";
    }

    window.addEventListener("themeChange", updateTheme);

    return () =>
      window.removeEventListener("themeChange", updateTheme);
  }, []);

  const selAcc = accounts.find(
    (a) => Number(a.id) === Number(selected)
  );

  const hasAccounts = accounts.length > 0;

  return (
    <div className={`app-shell ${dark ? "dark" : "light"}`}>

      {/* HEADER */}
      {tab !== "profile" && (
        <header className="header">
          <div
            className="avatar clickable"
            onClick={() => setTab("profile")}
          >
            {user ? user[0].toUpperCase() : "U"}
          </div>
        </header>
      )}

      {/* HOME */}
      {tab === "home" && (
        <>
          <div className="hero">
            <p className="hero-label">Cash Balance</p>

            <p style={{ opacity: 0.6 }}>
              Account • #{selAcc?.acc_no || "-"}
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
            onSelect={(id) => setSelected(Number(id))}
          />
        </>
      )}

      {/* ACTIONS */}
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

      {/* PROFILE */}
      {tab === "profile" && (
        <Profile user={user} onLogout={onLogout} />
      )}

      {/* PANELS */}
      {panel === "deposit" && selected && (
        <Deposit accountId={Number(selected)} onDone={loadAccounts} />
      )}

      {panel === "withdraw" && selected && (
        <Withdraw accountId={Number(selected)} onDone={loadAccounts} />
      )}

      {panel === "transfer" && selected && (
        <Transfer
          accountId={Number(selected)}
          fromAccNo={selAcc?.acc_no}
          onDone={loadAccounts}
        />
      )}

      {panel === "new" && (
        <CreateAccount onDone={loadAccounts} />
      )}

      {/* BOTTOM NAV */}
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