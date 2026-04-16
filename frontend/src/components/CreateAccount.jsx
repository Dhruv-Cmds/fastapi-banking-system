import { useState } from "react";
import API from "../api/api";
import "./panel.css";

export default function CreateAccount({ onDone }) {
  const [form, setForm] = useState({
    account_number: "",   // 🔥 renamed for clarity
    account_type: "savings",
  });

  const [msg, setMsg] = useState(null);

  const set = (k) => (e) =>
    setForm((p) => ({ ...p, [k]: e.target.value }));

  async function submit() {
    if (!form.account_number) return;

    try {
      await API.post("/accounts", {
        acc_no: Number(form.account_number), // 🔥 FIX: convert to number
        balance: 0,
      });

      setMsg({ text: "Account created!", type: "ok" });

      onDone();
    } catch (e) {
      setMsg({
        text: e.response?.data?.detail || "Failed to create.",
        type: "err",
      });
    }
  }

  return (
    <div className="panel">
      <p className="panelTitle">Open New Account</p>

      <div className="field">
        <label>Account Number</label>
        <input
          placeholder="Enter account number"
          value={form.account_number}
          onChange={set("account_number")}
        />
      </div>

      <div className="field">
        <label>Account Type</label>

        <select
          value={form.account_type}
          onChange={set("account_type")}
        >
          <option value="savings">Savings</option>
          <option value="checking">Checking</option>
        </select>
      </div>

      <button className="btn btn-primary" onClick={submit}>
        Create Account →
      </button>

      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
    </div>
  );
}