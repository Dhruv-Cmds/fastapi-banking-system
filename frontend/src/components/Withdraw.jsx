import { useState } from "react";
import API from "../api/api";
import "./panel.css";

const QUICK = [500, 1000, 5000, 10000];

export default function Withdraw({ accountId, onDone }) {
  const [amount, setAmount] = useState("");
  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    setMsg(null);
    setLoading(true);

    const amt = Number(amount);

    if (!amt || amt <= 0) {
      setMsg({ text: "Enter valid amount", type: "err" });
      return;
    }

    try {
      console.log("WITHDRAW:", accountId, amt);

      await API.post(`/accounts/${accountId}/withdraw`, {
        amount: amt,
      });

      setMsg({ text: "Withdrawal successful!", type: "ok" });

      setTimeout(() => setMsg(null), 3000);
      setTimeout(() => {
        onDone();
      }, 600);

    } catch (e) {
      setLoading(false);
      setMsg({
        text: e.response?.data?.detail || "Withdrawal failed",
        type: "err",
      });

      setTimeout(() => setMsg(null), 3000);
    }
  }

  return (
    <div className="panel">
      <p className="panelTitle">Withdraw Cash</p>

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

      <button
        className="btn btn-accent"
        onClick={submit}
        disabled={loading}
      >
        {loading ? "Processing..." : "Confirm Withdrawal →"}
      </button>

      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
    </div>
  );
}