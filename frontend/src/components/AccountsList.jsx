import "./panel.css";

const fmt = (n) =>
  "₹" +
  Number(n || 0).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
  });

export default function AccountsList({ accounts, selected, onSelect }) {
  if (!accounts.length) {
    return <p className="empty">No accounts yet. Create one below.</p>;
  }

  return (
    <div className="accounts-grid">
      {accounts.map((a) => (
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
        </div>
      ))}
    </div>
  );
}