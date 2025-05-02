import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [quote, setQuote] = useState("");

  // Fetch backend status (/hello)
  const fetchData = async () => {
    try {
      const res = await axios.get("http://localhost:8000/hello");
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch /hello", err);
      setData({ error: "Backend not reachable." });
    }
  };

  const fetchQuote = async () => {
    try {
      const res = await axios.get("http://localhost:8000/quote");
      const quoteText = res.data.quote?.raw || res.data.error || "No quote received.";
      setQuote(quoteText);
    } catch (err) {
      console.error("Failed to fetch /quote", err);
      setQuote("Failed to get quote.");
    }
  };
  

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Hospital Agent App</h1>

      <h2>Backend Status:</h2>
      <pre>{data ? JSON.stringify(data, null, 2) : "Loading..."}</pre>

      <h2>Motivational Quote:</h2>
      <button onClick={fetchQuote}>Get Motivational Quote</button>
      <pre style={{ marginTop: "1rem", color: "#4caf50" }}>{quote}</pre>
    </div>
  );
}

export default App;
