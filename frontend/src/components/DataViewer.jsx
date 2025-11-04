import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5050", { transports: ["websocket"] });

export default function DataViewer({ onData }) {
  const [data, setData] = useState({ ip: "", subnet: "", gateway: "" });

  useEffect(() => {
    socket.on("connect", () => console.log("[SOCKET] Connected"));
    socket.on("disconnect", () => console.log("[SOCKET] Disconnected"));

    socket.on("hercules_data", (msg) => {
      console.log("[SOCKET] Received:", msg);
      if (msg.ip && msg.subnet && msg.gateway) {
        setData(msg);
        if (onData) onData(msg);
      }
    });

    return () => {
      socket.off("hercules_data");
    };
  }, [onData]);

  return (
    <div className="data-box">
      <h3>Current Network</h3>
      <p><strong>IP:</strong> {data.ip || "Waiting..."}</p>
      <p><strong>Subnet:</strong> {data.subnet || "Waiting..."}</p>
      <p><strong>Gateway:</strong> {data.gateway || "Waiting..."}</p>
    </div>
  );
}
