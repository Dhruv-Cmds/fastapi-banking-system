import { useState } from "react";
import API from "../api/api";
import "./panel.css";

export default function CreateAccount({ onDone }) {

  const [form, setForm] = useState({
    account_name: "",
    account_type: "savings",
  });

  const [msg, setMsg] = useState(null);

  const set = (k) => (e) =>
    setForm((p) => ({ ...p, [k]: e.target.value }));

  async function submit() {

    if (!form.account_name) return;

    try {
        await API.post("/accounts", {
            acc_no: form.account_name,
            balance: 0,
      });
        
      onDone();
    } 
    
    catch (e) {

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

        <label>Account Name</label>
        <input
          placeholder="e.g. Emergency Fund"
          value={form.account_name}
          onChange={set("account_name")}
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