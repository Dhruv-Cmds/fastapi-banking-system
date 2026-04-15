import { useState, useEffect, useMemo} from "react";
import API from "../api/api";

import AccountsList from "./AccountsList";
import CreateAccount from "./CreateAccount";
import Deposit from "./Deposit";
import Withdraw from "./Withdraw";
import Transfer from "./Transfer";

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

  const totalBal = useMemo(
    () => accounts.reduce((s, a) => s + (a.balance || 0), 0),
    [accounts]
  );

  const selAcc = accounts.find((a) => a.id === selected);

  <p>Active: {selAcc?.account_name}</p>

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
        setSelected(data[0].id);
      }

    } 
    
    catch (err) {
      console.error("Failed to load accounts:", err);
    }
    
  }

  useEffect(() => {
  loadAccounts();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="app-shell">
      
      {/* Header */}
      <header className="header">

        <div className="header-left">
          <div className="avatar">
            {user ? user[0].toUpperCase() : "U"}
          </div
          >
          <div>
            <p className="greeting">Good Morning</p>
            <p className="username">{user}</p>
          </div>

        </div>

        <button className="logout-btn" onClick={onLogout}>
          Sign out
        </button>

      </header>

      {/* Balance */}
      <div className="hero">

        <p className="hero-label">Cash Balance</p>
        <p className="hero-amount">{fmt(totalBal)}</p>

        <div className="hero-actions">

          <button disabled={!hasAccounts} onClick={() => setPanel("deposit")}>
            Add Cash
          </button>

          <button disabled={!hasAccounts} onClick={() => setPanel("transfer")}>
            Send Money
          </button>

        </div>

      </div>

      {/* Actions */}
      <div className="quick-actions">
        {[
          { label: "Deposit", action: "deposit" },
          { label: "Withdraw", action: "withdraw" },
          { label: "Transfer", action: "transfer" },
          { label: "New Acc", action: "new" },
        ].map(({ label, action }) => (

          <button
            key={action}
            onClick={() =>
              setPanel((prev) => (prev === action ? null : action))
            }
          >
            {label}

          </button>

        ))}

      </div>

      {/* Panels */}
      {panel === "deposit" && selected && (
        <Deposit accountId={selected} onDone={loadAccounts} />
      )}

      {panel === "withdraw" && selected && (
        <Withdraw accountId={selected} onDone={loadAccounts} />
      )}

      {panel === "transfer" && selected && (
        <Transfer accountId={selected} onDone={loadAccounts} />
      )}

      {panel === "new" && (
        <CreateAccount onDone={loadAccounts} />
      )}

      {/* Accounts */}
      <AccountsList
        accounts={accounts}
        selected={selected}
        onSelect={setSelected}
      />
    </div>

  );
}