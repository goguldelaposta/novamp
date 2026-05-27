import { useState } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import "./App.css";

const servers = [
  {
    id: 1,
    name: "NovaRP Official",
    players: 124,
    maxPlayers: 256,
    mode: "Roleplay",
    ip: "play.novarp.ro:22005",
  },
  {
    id: 2,
    name: "Nova Freeroam",
    players: 45,
    maxPlayers: 128,
    mode: "Freeroam",
    ip: "free.novarp.ro:22005",
  },
  {
    id: 3,
    name: "Nova Drift",
    players: 23,
    maxPlayers: 64,
    mode: "Drift",
    ip: "drift.novarp.ro:22005",
  },
];

function App() {
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <div className="launcher">
      <div className="titlebar">
        <span className="titlebar-title">NovaMP</span>
        <div className="titlebar-buttons">
          <button onClick={() => getCurrentWindow().minimize()}>─</button>
          <button onClick={() => getCurrentWindow().close()}>✕</button>
        </div>
      </div>

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
