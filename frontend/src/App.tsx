import { useRef, useEffect } from "react";
import { Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Inventory from "./pages/Inventory";
import Disaster from "./pages/Disaster";
import Landing from "./pages/Landing";
import "./App.css";

function App() {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 0.5; // Slow down video
    }
  }, []);

  return (
    <>
      {/* ✅ Background Video */}
      <video
        ref={videoRef}
        autoPlay
        muted
        loop
        playsInline
        className="background-video"
      >
        <source src="/hospital-bg.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* ✅ Overlay to darken */}
      <div className="background-overlay"></div>

      {/* ✅ Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div className="container-fluid">
          <Link className="navbar-brand fw-bold" to="/">SUPPLYLINE</Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" to="/home">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/inventory">Inventory</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/disaster">Disaster</Link>
              </li>
            </ul>
            <form className="d-flex">
              <input className="form-control me-2" type="search" placeholder="Search" />
              <button className="btn btn-outline-success" type="submit">Search</button>
            </form>
          </div>
        </div>
      </nav>

      {/* ✅ Page Content */}
      <div style={{ paddingTop: "80px" }}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/home" element={<Home />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/disaster" element={<Disaster />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
