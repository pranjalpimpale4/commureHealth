import { useEffect, useState } from "react";

type Message = {
  round: number;
  role: string;
  content: string;
};

const AgentChat = () => {
  const [chatLog, setChatLog] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const parseRawLog = (data: string[]): Message[] => {
    let roundCounter = 1;
    return data.map((line) => {
      const match = line.match(/^(.+?):\s+(.*)$/);
      if (match) {
        const [, role, content] = match;
        return {
          round: roundCounter++,
          role,
          content,
        };
      } else {
        return {
          round: roundCounter++,
          role: "System",
          content: line,
        };
      }
    });
  };

  const fetchChat = () => {
    setLoading(true);
    setError(null);
    fetch("http://localhost:8000/chat-log")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          const parsed = parseRawLog(data);
          setChatLog(parsed);
        } else {
          console.warn("Unexpected response format:", data);
          setError("Invalid response format from server.");
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch chat log:", err);
        setError("Failed to load chat log.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchChat();
    const interval = setInterval(fetchChat, 2000); // Live polling every 2 sec
    return () => clearInterval(interval);
  }, []);

  const handleStartNegotiation = async () => {
    setStarting(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/start-negotiation", {
        method: "POST",
      });
      const data = await response.json();
      console.log("Negotiation started:", data);
      fetchChat(); // Refresh chat log
    } catch (err) {
      console.error("Failed to start negotiation", err);
      setError("Error starting negotiation.");
    } finally {
      setStarting(false);
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{
        minHeight: "100vh",
        padding: "40px",
        background: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <div style={{ maxWidth: "800px", width: "100%", color: "#fff" }}>
        <h2 className="mb-4 text-center">Agent Negotiation Chat</h2>

        <div className="text-center">
          <button
            onClick={handleStartNegotiation}
            className="btn btn-primary mb-4"
            disabled={starting}
          >
            {starting ? "Starting..." : "Start Negotiation"}
          </button>
        </div>

        {loading && <p className="text-center">Loading chat...</p>}

        {error && (
          <div className="alert alert-danger text-center">{error}</div>
        )}

        {!loading && !error && chatLog.length === 0 && (
          <p className="text-center">No messages yet. Start a negotiation.</p>
        )}

        {!loading &&
          !error &&
          chatLog.map((msg, idx) => (
            <div
              key={idx}
              style={{
                background: "rgba(255, 255, 255, 0.1)",
                border: "1px solid rgba(255,255,255,0.2)",
                padding: "15px",
                marginBottom: "15px",
                borderRadius: "12px",
                boxShadow: "0 0 10px rgba(255,255,255,0.1)",
              }}
            >
              <strong>
                Round {msg.round} - {msg.role}
              </strong>
              <p>{msg.content}</p>
            </div>
          ))}
      </div>
    </div>
  );
};

export default AgentChat;
