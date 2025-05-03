// src/pages/Disaster.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Disaster.css";

interface DisasterEvent {
  source: string;
  type: string;
  country: string | null;
  location: string | null;
  latitude: number;
  longitude: number;
  date: string;
  headline: string;
  status: string;
}

const Disaster = () => {
  const [events, setEvents] = useState<DisasterEvent[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/events/raw")
      .then((res) => {
        setEvents(res.data);
      })
      .catch((err) => {
        console.error("Error fetching disaster events:", err);
        setError("Failed to load disaster events.");
      });
  }, []);

  return (
    <div className="disaster-container">
      <div className="left-panel">
        <div className="summary-box">
          <h3>📰 News of Interest</h3>
          <p>Will be populated soon...</p>
        </div>

        <div className="orders-box">
          <h3>🧾 Orders to Be Placed</h3>
          <p>Prediction model output will show here.</p>
        </div>

        <div className="orders-table">
          <h3>📦 Orders Table</h3>
          <p>Table of recommended inventory will appear here.</p>
        </div>
      </div>

      <div className="right-panel">
        <h3>🌍 Extracted News</h3>
        {error && <p className="error">{error}</p>}
        <ul className="news-list">
          {events.map((event, index) => (
            <li key={index} className="news-item">
              <p><strong>{event.date.split("T")[0]}</strong></p>
              <p>{event.headline}</p>
              <p className="source">Source: {event.source}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Disaster;
