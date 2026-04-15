import { useState } from "react";
import API from "../api/api";
import "./panel.css";

const QUICK = [500, 1000, 5000, 10000];



export default function Transfer({ accountId, fromAccNo, onDone }) {
  const [amount, setAmount] = useState("");
  const [toAccNo, setToAccNo] = useState("");
  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    setMsg(null);
    setLoading(true);

    const to = Number(toAccNo);
    const from = Number(fromAccNo);
    const amt = Number(amount);

    if (!amt || amt <= 0 || !to) {
      setMsg({ text: "Enter valid details", type: "err" });
      return;
    }

    if (to === from) {
      setMsg({ text: "Cannot send to your own account", type: "err" });
      return;
    }

    try {
      console.log("Transfer:", accountId, to, amt);

      await API.post("/transfer", {
        from_account_id: Number(accountId),   
        to_account_no: to,
        amount: amt,                         
      });

      setMsg({ text: "Transfer successful!", type: "ok" });

      setTimeout(() => setMsg(null), 3000);
      setLoading(false); 
      setTimeout(onDone, 800);

    } catch (e) {
      setLoading(false);
      setMsg({
        text: e.response?.data?.detail || "Transfer failed",
        type: "err",
      });

      setTimeout(() => setMsg(null), 3000);
    }
  }

  return (
    <div className="panel">
      <p className="panelTitle">Send Money</p>

      <div className="field">
        <label>To Account</label>
        <input
          type="number"
          placeholder="Enter account number"
          value={toAccNo}
          onChange={(e) => setToAccNo(e.target.value)}
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
          <button key={q} className="chip" onClick={() => setAmount(String(q))}>
            ₹{q >= 1000 ? q / 1000 + "k" : q}
          </button>
        ))}
      </div>

      <button
        className="btn btn-primary"
        onClick={submit}
        disabled={loading}
      >
        {loading ? "Processing..." : "Send Money →"}
      </button>

      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
    </div>
  );
}