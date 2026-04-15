import { useState } from "react";
import API from "../api/api";
import "./panel.css";

const QUICK = [500, 1000, 5000, 10000];

export default function Transfer({ accountId, fromAccNo, onDone }) {
  const [amount, setAmount] = useState("");
  const [toAccNo, setToAccNo] = useState("");
  const [msg, setMsg] = useState(null);

  async function submit() {
    setMsg(null);

    if (!amount || !toAccNo) {
      setMsg({ text: "Fill all fields", type: "err" });
      return;
    }

    // 🔥 SELF TRANSFER BLOCK
    if (Number(toAccNo) === Number(fromAccNo)) {
      setMsg({ text: "Cannot send to your own account", type: "err" });
      return;
    }

    try {
      await API.post("/transfer", {
        from_account_id: accountId,
        to_account_no: parseInt(toAccNo),
        amount: parseFloat(amount),
      });

      setMsg({ text: "Transfer successful!", type: "ok" });
      setTimeout(onDone, 800);
    } catch (e) {
      setMsg({
        text: e.response?.data?.detail || "Transfer failed",
        type: "err",
      });
    }
  }

  return (
    <div className="panel">
      <p className="panelTitle">Send Money</p>

      {/* Account Input */}
      <div className="field">
        <label>To Account</label>
        <input
          type="number"
          placeholder="Enter account number"
          value={toAccNo}
          onChange={(e) => setToAccNo(e.target.value)}
        />
      </div>

      {/* Amount */}
      <div className="field">
        <label>Amount (₹)</label>
        <input
          type="number"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </div>

      {/* Quick buttons */}
      <div className="chips">
        {QUICK.map((q) => (
          <button key={q} className="chip" onClick={() => setAmount(String(q))}>
            ₹{q >= 1000 ? q / 1000 + "k" : q}
          </button>
        ))}
      </div>

      {/* Submit */}
      <button className="btn btn-primary" onClick={submit}>
        Send Money →
      </button>

      {/* Message */}
      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
    </div>
  );
}