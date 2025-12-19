// src/pages/Disaster.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Disaster.css";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

// Fix Leaflet marker paths
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

interface Shortage {
  item_id: number;
  item: string;
  description: string;
  available: number;
  needed: number;
}

interface DisasterResponse {
  status: string;
  source: string;
  Event: string[];
  shortages: Shortage[];
}

const Disaster = () => {
  const [data, setData] = useState<DisasterResponse | null>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const cached = localStorage.getItem("disasterData");
    if (cached) {
      setData(JSON.parse(cached));
    }
  }, []);

  const fetchDisasterData = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await axios.post("http://127.0.0.1:8000/inventory/shortages/disaster");
      setData(res.data);
      localStorage.setItem("disasterData", JSON.stringify(res.data));
    } catch (err) {
      console.error("Error fetching disaster response:", err);
      setError("Failed to fetch disaster response data.");
    } finally {
      setLoading(false);
    }
  };

  const getLatLng = (event: string): [number, number] => {
    if (event.toLowerCase().includes("indonesia")) return [-2.5, 118];
    if (event.toLowerCase().includes("australia")) return [-25.2, 133.8];
    if (event.toLowerCase().includes("chile")) return [-35.7, -71.5];
    if (event.toLowerCase().includes("argentina")) return [-38.4, -63.6];
    if (event.toLowerCase().includes("papua new guinea")) return [-6.3, 147];
    if (event.toLowerCase().includes("malaysia")) return [4.2, 101];
    if (event.toLowerCase().includes("new zealand")) return [-40.9, 174.9];
    if (event.toLowerCase().includes("taiwan")) return [23.7, 121];
    if (event.toLowerCase().includes("mexico")) return [23.6, -102.5];
    if (event.toLowerCase().includes("germany")) return [51.2, 10.4];
    if (event.toLowerCase().includes("brazil")) return [-14.2, -51.9];
    if (event.toLowerCase().includes("slovakia")) return [48.7, 19.7];
    if (event.toLowerCase().includes("virgin")) return [18.5, -64.5];
    return [-10 + Math.random() * 10, 120 + Math.random() * 10];
  };

  return (
    <div className="disaster-page__container">
      <button className="disaster-page__fetch-button" onClick={fetchDisasterData}>
        Fetch Disaster Response
      </button>

      {data?.Event?.length > 0 && (
        <div className="disaster-page__map-box">
          <MapContainer center={[-10, 120]} zoom={2} scrollWheelZoom className="disaster-page__map-style">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />
            {data.Event.map((event, index) => {
              const [lat, lng] = getLatLng(event);
              return (
                <Marker key={index} position={[lat, lng]}>
                  <Popup>{event}</Popup>
                </Marker>
              );
            })}
            {data.Event.length > 0 && (
              <Circle center={getLatLng(data.Event[0])} radius={80000} pathOptions={{ color: "red" }} />
            )}
          </MapContainer>
        </div>
      )}

      <div className="disaster-page__content">
        <div className="disaster-page__left-panel">
          <h2 className="disaster-page__section-title">Emergency Events</h2>
          {error && <p className="disaster-page__error">{error}</p>}
          {loading && <p>Loading...</p>}
          <div className="disaster-page__event-grid">
            {data?.Event.map((event, index) => (
              <div key={index} className="disaster-page__event-tile">
                {event}
              </div>
            ))}
          </div>
        </div>

        <div className="disaster-page__right-panel">
          <h2 className="disaster-page__section-title">Inventory Shortages</h2>
          <table className="disaster-page__shortages-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Description</th>
                <th>Available</th>
                <th>Needed</th>
              </tr>
            </thead>
            <tbody>
              {data?.shortages.map((item) => (
                <tr key={item.item_id}>
                  <td>{item.item}</td>
                  <td>{item.description}</td>
                  <td>{item.available}</td>
                  <td>{item.needed}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Disaster;