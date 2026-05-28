import { useState, useEffect } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import "./App.css";

const isMac = navigator.userAgent.includes("Mac OS X");
const appWindow = getCurrentWindow();

interface Server {
  id: string;
  name: string;
  ip: string;
  port: string;
  mode: string;
  players: number;
  maxPlayers: number;
}

function App() {
  const [selected, setSelected] = useState<string | null>(null);
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchServers();
    const interval = setInterval(fetchServers, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchServers = async () => {
    try {
      const res = await fetch("http://localhost:3000/servers");
      const data = await res.json();
      setServers(data);
    } catch (err) {
      console.error("Masterlist offline");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="launcher">
      {!isMac && (
        <div className="titlebar" data-tauri-drag-region>
          <span className="titlebar-logo">Nova<span>MP</span></span>
          <div className="titlebar-buttons">
            <button className="tb-btn" onClick={() => appWindow.minimize()} title="Minimize">
              <svg width="10" height="1" viewBox="0 0 10 1"><rect width="10" height="1" fill="currentColor"/></svg>
            </button>
            <button className="tb-btn" onClick={() => appWindow.toggleMaximize()} title="Maximize">
              <svg width="10" height="10" viewBox="0 0 10 10"><rect x="0.5" y="0.5" width="9" height="9" stroke="currentColor" strokeWidth="1" fill="none"/></svg>
            </button>
            <button className="tb-btn close" onClick={() => appWindow.close()} title="Close">
              <svg width="10" height="10" viewBox="0 0 10 10"><line x1="0" y1="0" x2="10" y2="10" stroke="currentColor" strokeWidth="1.5"/><line x1="10" y1="0" x2="0" y2="10" stroke="currentColor" strokeWidth="1.5"/></svg>
            </button>
          </div>
        </div>
      )}
      <div className="main">
        <div className="sidebar">
          <div className="logo">
            <h1>Nova<span>MP</span></h1>
          </div>
          <nav>
            <button className="nav-btn active">Servere</button>
            <button className="nav-btn">Stiri</button>
            <button className="nav-btn">Setari</button>
          </nav>
        </div>

        <div className="content">
          <div className="header">
            <h2>Alege un server</h2>
            <p>{servers.reduce((a, b) => a + b.players, 0)} jucatori online</p>
          </div>

          <div className="server-list">
            {loading && <p style={{color: "#888"}}>Se incarca serverele...</p>}
            {!loading && servers.length === 0 && <p style={{color: "#888"}}>Niciun server online</p>}
            {servers.map((server) => (
              <div
                key={server.id}
                className={`server-card ${selected === server.id ? "selected" : ""}`}
                onClick={() => setSelected(server.id)}
              >
                <div className="server-info">
                  <h3>{server.name}</h3>
                  <span className="mode">{server.mode}</span>
                </div>
                <div className="server-players">
                  <span>{server.players}/{server.maxPlayers}</span>
                  <small>jucatori</small>
                </div>
              </div>
            ))}
          </div>

          <button
            className={`play-btn ${selected ? "active" : ""}`}
            disabled={!selected}
          >
            {selected ? "CONECTEAZA-TE" : "Selecteaza un server"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;