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

    <div className="list">

      {accounts.map((a) => (

        <div
          key={a.id}
          className={`card ${Number(selected) === Number(a.id) ? "active" : ""}`}
          onClick={() => {
            console.log("clicked:", a.id);
            onSelect(a.id);
          }}
        >
          <div className="left">
            <div className="icon">
              {a.account_type === "savings" ? "🏦" : "💳"}
            </div>

            <div>
              <p className="name">{a.account_name}</p>
              <p className="meta">
                {a.account_type} • #{a.id}
              </p>
            </div>

          </div>

          <div className="bal">{fmt(a.balance)}</div>

        </div>
        
      ))}

    </div>
  );
}