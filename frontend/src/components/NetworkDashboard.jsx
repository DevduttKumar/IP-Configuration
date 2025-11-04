import React, { useState } from "react";
import DataViewer from "./DataViewer";

export default function NetworkDashboard() {
  const [data, setData] = useState({});
  const [showPopup, setShowPopup] = useState(false);
  const [popupMsg, setPopupMsg] = useState("");

  const handleChangeIP = async () => {
    try {
      const res = await fetch("http://localhost:5050/api/change-ip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await res.json();
      setPopupMsg(result.message || "Operation complete");
    } catch (err) {
      setPopupMsg("Failed to change IP: " + err.message);
    }
    setShowPopup(true);
  };

  return (
    <div className="dashboard">
      <h1>Network Dashboard</h1>
      <DataViewer onData={(d) => setData(d)} />

      {data.ip && (
        <button className="change-btn" onClick={handleChangeIP}>
          Change IP
        </button>
      )}

      {showPopup && (
        <div className="popup">
          <div className="popup-inner">
            <p>{popupMsg}</p>
            <button onClick={() => setShowPopup(false)}>OK</button>
          </div>
        </div>
      )}
    </div>
  );
}
