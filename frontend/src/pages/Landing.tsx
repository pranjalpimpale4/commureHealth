// src/pages/Landing.tsx
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Landing.css";

const navItems = [
  {
    title: "Inventory",
    path: "/inventory",
    description: "Track, monitor and replenish medical supplies in real time.",
    img: "https://cdn-icons-png.flaticon.com/512/1170/1170678.png",
  },
  {
    title: "Disaster",
    path: "/disaster",
    description: "Predict and respond to disasters with data-driven insights.",
    img: "https://cdn-icons-png.flaticon.com/512/1159/1159633.png",
  },
  {
    title: "Demand",
    path: "/demand",
    description: "Forecast hospital needs and ensure optimal resource allocation.",
    img: "https://cdn-icons-png.flaticon.com/512/4149/4149656.png",
  },
  {
    title: "Home",
    path: "/",
    description: "View performance dashboards and system-wide insights.",
    img: "https://cdn-icons-png.flaticon.com/512/3081/3081559.png",
  },
];

const Landing = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const tiles = document.querySelectorAll(".feature-tile");
    tiles.forEach((tile, index) => {
      (tile as HTMLElement).style.animationDelay = `${index * 0.1}s`;
      tile.classList.add("animate-in");
    });
  }, []);

  return (
    <div className="landing-container">
      <section className="hero-section">
        <div className="hero-text-wrapper">
          <h1 className="hero-title">
            The technology behind<br /> advanced health systems.
          </h1>
          <p className="hero-subtitle">
            We build software and AI experiences that simplify provider, administrator, and patient workflows.
          </p>
        </div>
        <video className="full-width-video" autoPlay muted loop playsInline>
          <source src="/hero.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </section>

      <section className="features-section full-width-screen">
        <h3 className="features-heading">
          EXTENSIBLE, INTEGRATED TECHNOLOGY THAT SIMPLIFIES HEALTH SYSTEMS.
        </h3>
        <div className="feature-grid">
          {navItems.map((item, index) => (
            <div
              className="feature-tile centered"
              key={index}
              onClick={() => navigate(item.path)}
              onMouseEnter={(e) => {
                e.currentTarget.classList.add("hover-active");
              }}
              onMouseLeave={(e) => {
                e.currentTarget.classList.remove("hover-active");
              }}
            >
              <img
                src={item.img}
                alt={item.title}
                className="tile-icon greyscale"
              />
              <h4>{item.title}</h4>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Landing;