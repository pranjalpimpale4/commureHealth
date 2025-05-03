// src/pages/Home.tsx
import React from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";
import "./DashboardHome.css";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const DashboardHome = () => {
  const ppeData = [
    { date: "Jan", masks: 400, gloves: 300 },
    { date: "Feb", masks: 300, gloves: 250 },
    { date: "Mar", masks: 500, gloves: 450 },
    { date: "Apr", masks: 600, gloves: 550 },
  ];

  const medicineStock = [
    { name: "Paracetamol", quantity: 120 },
    { name: "Ibuprofen", quantity: 90 },
    { name: "Antibiotics", quantity: 150 },
    { name: "Insulin", quantity: 70 },
  ];

  const usageByDept = [
    { department: "ER", usage: 500 },
    { department: "ICU", usage: 420 },
    { department: "Pediatrics", usage: 210 },
    { department: "General", usage: 300 },
  ];

  const restockFrequency = [
    { item: "Masks", times: 10 },
    { item: "Gloves", times: 8 },
    { item: "Sanitizer", times: 6 },
    { item: "Gowns", times: 4 },
  ];

  return (
    <div className="dashboard-full">
      <h2 className="dashboard-title">🏥 Hospital Inventory Dashboard</h2>

      <div className="kpi-row">
        <div className="tile">
          <h3>Total Inventory</h3>
          <p>2,320</p>
          <small>+12%</small>
        </div>
        <div className="tile">
          <h3>Orders to Place</h3>
          <p>16</p>
          <small>-8%</small>
        </div>
        <div className="tile">
          <h3>Fulfillment Rate</h3>
          <p>94.5%</p>
          <small>+3.1%</small>
        </div>
        <div className="tile">
          <h3>On-Time Delivery</h3>
          <p>89.7%</p>
          <small>+2.3%</small>
        </div>
      </div>

      <div className="charts-row">
        <div className="chart-box">
          <h4 style={{ textAlign: "center" }}>PPE Inventory</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={ppeData}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="masks" stroke="#8884d8" />
              <Line type="monotone" dataKey="gloves" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-box">
          <h4 style={{ textAlign: "center" }}>Medicine Stock</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={medicineStock}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="quantity" fill="#00C49F" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-box">
          <h4 style={{ textAlign: "center" }}>Department Usage</h4>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={usageByDept}
                dataKey="usage"
                nameKey="department"
                outerRadius={100}
                label
              >
                {usageByDept.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-box">
          <h4 style={{ textAlign: "center" }}>Restock Frequency</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={restockFrequency}>
              <XAxis dataKey="item" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="times" fill="#FF8042" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
