import { useState } from "react";
import API from "../api/api";
import "./panel.css";

const QUICK = [500, 1000, 5000, 10000];

export default function Transfer({ accountId, onDone }) {
  const [amount, setAmount] = useState("");
  const [toId, setToId] = useState("");
  const [msg, setMsg] = useState(null);

  async function submit() {
    if (!amount || !toId) return;

    try {
        await API.post("/transfer", {
            from_account_id: accountId,
            to_account_id: parseInt(toId),
            amount: parseFloat(amount),
        });

      setMsg({ text: "Transfer successful!", type: "ok" });
      setTimeout(onDone, 900);
    } catch (e) {
      setMsg({
        text: e.response?.data?.detail || "Transfer failed.",
        type: "err",
      });
    }
  }

  return (
    <div className="panel">
      <p className="panelTitle">Send Money</p>

      <div className="field">
        <label>To Account ID</label>
        <input
          type="number"
          placeholder="Recipient account ID"
          value={toId}
          onChange={(e) => setToId(e.target.value)}
        />
      </div>

      <div className="field">
        <label>Amount (₹)</label>
        <input
          type="number"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </div>

      <div className="chips">
        {QUICK.map((q) => (
          <button
            key={q}
            className="chip"
            onClick={() => setAmount(String(q))}
          >
            ₹{q >= 1000 ? q / 1000 + "k" : q}
          </button>
        ))}
      </div>

      <button className="btn btn-primary" onClick={submit}>
        Send Money →
      </button>

      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
    </div>
  );
}