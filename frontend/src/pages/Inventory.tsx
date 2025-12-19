// src/pages/Inventory.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Inventory.css";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface InventoryItem {
  item_id: number;
  name: string;
  available_count: number;
  threshold: number;
  status: string;
}

interface ForecastItem {
  item_id: number;
  item: string;
  description: string;
  available: number;
  needed: number;
}

const Inventory = () => {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [forecast, setForecast] = useState<ForecastItem[]>([]);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const cached = localStorage.getItem("inventoryData");
    if (cached) setInventory(JSON.parse(cached));

    const cachedForecast = localStorage.getItem("forecastData");
    if (cachedForecast) setForecast(JSON.parse(cachedForecast));
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      const res = await axios.get("http://127.0.0.1:8000/inventory/list");
      setInventory(res.data);
      localStorage.setItem("inventoryData", JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      setError("Failed to fetch inventory data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchForecast = async () => {
    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/inventory/shortages/forecast");
      setForecast(res.data.shortages);
      localStorage.setItem("forecastData", JSON.stringify(res.data.shortages));
    } catch (err) {
      console.error(err);
      setError("Failed to fetch forecast data.");
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: inventory.map((item) => item.name),
    datasets: [
      {
        label: "Available Stock",
        data: inventory.map((item) => item.available_count),
        backgroundColor: "#00b894",
      },
      {
        label: "Threshold",
        data: inventory.map((item) => item.threshold),
        backgroundColor: "#d63031",
      },
    ],
  };

  return (
    <div className="inventory-container">
      <div className="inventory-actions">
        <button className="fetch-button" onClick={fetchInventory}>Fetch Inventory</button>
        <button className="fetch-button" onClick={fetchForecast}>Fetch Forecast</button>
      </div>

      {loading && <p className="loading">Loading data...</p>}
      {error && <p className="error">{error}</p>}

      <div className="inventory-content">
        {/* Inventory Table Section */}
        <div className="inventory-table-section">
          <h2 className="section-title">Inventory Items</h2>
          <table className="inventory-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Available</th>
                <th>Threshold</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map((item) => (
                <tr key={item.item_id}>
                  <td>{item.name}</td>
                  <td>{item.available_count}</td>
                  <td>{item.threshold}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Analytics Section */}
        <div className="inventory-analytics-section">
          <h2 className="section-title">Stock Overview</h2>
          <div className="chart-container">
            <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
          <div className="forecast-tile">
            <h3>Forecasted Shortages</h3>
            {forecast.length === 0 ? (
              <p>No forecast data available.</p>
            ) : (
              <ul>
                {forecast.map((item) => (
                  <li key={item.item_id}>
                    <strong>{item.item}</strong>: {item.available} available, {item.needed} needed
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Inventory;
