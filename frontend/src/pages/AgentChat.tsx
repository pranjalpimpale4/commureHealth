// src/pages/AgentChat.tsx
import React from "react";
import "./AgentChat.css";

const AgentChat = () => {
  return (
    <div className="agentchat-container">
      <div className="agentchat-header">
        <h1>Medical Supply Negotiation Portal</h1>
      </div>

      <div className="negotiation-grid">
        {/* Participants */}
        <div className="left-panel">
          <div className="room-title">🟣 Active Negotiation Room</div>
          <div className="participant-list">
            <div className="participant"><span className="avatar ha">HA</span><div><strong>Hospital Agent</strong><br /><span className="org">St. Mary Medical</span></div></div>
            <div className="participant"><span className="avatar ca">CA</span><div><strong>Clinic Agent</strong><br /><span className="org">Downtown Health</span></div></div>
            <div className="participant"><span className="avatar pa">PA</span><div><strong>Pharmacy Agent</strong><br /><span className="org">MedRx Solutions</span></div></div>
            <div className="participant"><span className="avatar na">NA</span><div><strong>NGO Agent</strong><br /><span className="org">Global Health Aid</span></div></div>
          </div>
          <div className="online-status">🟢 4 online <span className="invite">Invite +</span></div>
        </div>

        {/* Chat */}
        <div className="center-panel">
          <div className="messages">
            <div className="message msg-hospital">• Pharmacy: 800 units at $7.50<br />• NGO: 700 units at $6.75</div>
            <div className="message msg-hospital">We aim to distribute everything before the expiration deadline.</div>
            <div className="message msg-ngo">We agree to $6.75 for 700 units, delivery within 2 days.</div>
            <div className="message msg-clinic">We accept $7.25 for 500 units. Please confirm timeline.</div>
          </div>
          <div className="input-area">
            <input type="text" placeholder="Type your message..." />
            <button className="send-btn">Send</button>
          </div>
        </div>

        {/* Deal Summary */}
        <div className="right-panel">
          <div className="deal-card">
            <h4>Product Information</h4>
            <p><strong>Medicine:</strong> Amoxicillin<br />
              <strong>Dosage:</strong> 500mg<br />
              <strong>Quantity:</strong> 2,000 units<br />
              <strong>Expires:</strong> In 3 months</p>
          </div>
          <div className="deal-card">
            <h4>Current Offers</h4>
            <p><strong>Clinic:</strong> <span className="green">$7.25</span><br />
              <strong>Pharmacy:</strong> <span className="green">$7.50</span><br />
              <strong>NGO:</strong> <span className="green">$6.75</span></p>
          </div>
          <div className="deal-card">
            <button className="expert-btn">➕ Invite Expert Advisor</button>
          </div>
        </div>
      </div>

      {/* Bottom Insights */}
      <div className="bottom-info">
        <div className="bottom-card">
          <h4>Current Market Pricing</h4>
          <p><strong>Wholesale:</strong> $15.00<br />
            <strong>Retail:</strong> $22.50<br />
            <strong>Hospital Cost:</strong> $6.50<br />
            <strong>NGO Rate:</strong> $5.75</p>
        </div>

        <div className="bottom-card">
          <h4>Negotiation Timeline</h4>
          <p><strong>10:15 AM</strong> - Negotiation Started<br />
            <strong>10:18 AM</strong> - Offers Made<br />
            <strong>10:25 AM</strong> - Counter Proposed</p>
        </div>
      </div>
    </div>
  );
};

export default AgentChat;
