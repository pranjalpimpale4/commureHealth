import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        backgroundColor: "#1f2937",
        color: "#fff",
        padding: "1rem 2rem",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        zIndex: 1000,
        boxShadow: "0 2px 5px rgba(0,0,0,0.2)",
      }}
    >
      <div style={{ fontWeight: "bold", fontSize: "1.2rem" }}>Hospital Inventory</div>
      <div style={{ display: "flex", gap: "1.5rem" }}>
        <Link style={{ color: "#fff", textDecoration: "none" }} to="/home">Home</Link>
        <Link style={{ color: "#fff", textDecoration: "none" }} to="/inventory">Inventory</Link>
        <Link style={{ color: "#fff", textDecoration: "none" }} to="/disaster">Disaster</Link>
      </div>
    </nav>
  );
};

export default Navbar;
