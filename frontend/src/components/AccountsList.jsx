import "./panel.css";
import API from "../api/api";

const fmt = (n) =>
  "₹" +
  Number(n || 0).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
  });

export default function AccountsList({ accounts, selected, onSelect, onRefresh }) {

  async function handleDelete(e, id) {
    e.stopPropagation();

    const confirmDelete = window.confirm(
      "Close this account? This action cannot be undone."
    );

    if (!confirmDelete) return;

    try {
      await API.delete(`/accounts/${id}`);

      alert("Account closed");

      onRefresh();
    } 
    
    catch (err) {
      alert(err.response?.data?.detail || "Action failed");
    }
    
  }

  if (!accounts.length) {
    return <p className="empty">No accounts yet. Create one below.</p>;
  }

  return (
      <div className="accounts-grid">
        {accounts
          .filter((a) => a.status === "ACTIVE")
          .map((a) => (
            <div
                key={a.id}
                className={`account-card ${
                  Number(selected) === Number(a.id) ? "active" : ""
                }`}

                onClick={() => onSelect(a.id)}
              >
                <p className="acc-name">
                  {a.account_name || "Account"}
                </p>

                <p className="acc-balance">
                  {fmt(a.balance)}
                </p>

                <p className="acc-number">
                  •••• {a.acc_no}
                </p>

                <button
                  className="btn btn-accent"
                  style={{ marginTop: "10px" }}
                  onClick={(e) => handleDelete(e, a.id)}
                >
                  Close
                </button>
            </div>
          ))}
    </div>
  );
}