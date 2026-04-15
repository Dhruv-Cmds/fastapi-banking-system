import { useState } from "react";
import API from "../api/api";
import "./panel.css";

const QUICK = [500, 1000, 5000, 10000];

export default function Deposit({ accountId, onDone }) {

  const [amount, setAmount] = useState("");
  const [msg, setMsg] = useState(null);

  async function submit() {

    if (!amount) return;

    try {

      await API.post(`/accounts/${accountId}/deposit`, {
        amount: parseFloat(amount),
      });

      setMsg({ text: "Deposit successful!", type: "ok" });

      setTimeout(onDone, 900);

    } 

    catch (e) {
      setMsg({
        text: e.response?.data?.detail || "Deposit failed.",
        type: "err",
      });

    }

  }

  return (
    <div className="panel">

      <p className="panelTitle">Add Cash</p>

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
        Confirm Deposit →
      </button>

      {msg && <div className={`toast ${msg.type}`}>{msg.text}</div>}
      
    </div>
  );
}