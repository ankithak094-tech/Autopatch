
import React, { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:5000";

const SAMPLE_CODE = `def divide(a, b):
    return a / b

print(divide(10, 0))`;

export default function App() {
  const [code, setCode] = useState(SAMPLE_CODE);
  const [bugs, setBugs] = useState([]);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [fixedCode, setFixedCode] = useState("");
  const [loading, setLoading] = useState("");
  const [status, setStatus] = useState("Checking...");
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("editor");

  async function apiRequest(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || `Server error: ${response.status}`);
    }

    return data;
  }

  async function checkHealth() {
    try {
      await apiRequest("/health");
      setStatus("Connected");
    } catch {
      setStatus("Disconnected");
    }
  }

  async function loadHistory() {
    try {
      const data = await apiRequest("/history");
      setHistory(data.history || []);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    checkHealth();
    loadHistory();
    const timer = setInterval(checkHealth, 5000);
    return () => clearInterval(timer);
  }, []);

  async function analyzeCode() {
    setLoading("analyze");
    setError("");
    setBugs([]);
    setResult(null);

    try {
      const data = await apiRequest("/analyze", {
        method: "POST",
        body: JSON.stringify({ code }),
      });

      setResult(data);
      setBugs(data.bugs || data.detected_bugs || []);
      await loadHistory();
      setActiveTab("results");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading("");
    }
  }

  async function repairCode() {
    setLoading("repair");
    setError("");

    try {
      const data = await apiRequest("/ai-repair", {
        method: "POST",
        body: JSON.stringify({ code }),
      });

      const repaired =
        data.fixed_code ||
        data.repaired_code ||
        data.code ||
        "";

      if (repaired) {
        setFixedCode(repaired);
      }

      setResult(data);
      await loadHistory();
      setActiveTab("repair");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading("");
    }
  }

  async function validateCode() {
    setLoading("validate");
    setError("");

    try {
      const data = await apiRequest("/validate", {
        method: "POST",
        body: JSON.stringify({ code: fixedCode || code }),
      });

      setResult(data);
      await loadHistory();
      setActiveTab("results");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading("");
    }
  }

  const displayCode = fixedCode || code;

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">A</div>
          <div>
            <h2>AutoPatch</h2>
            <span>AI CODE REPAIR</span>
          </div>
        </div>

        <div className="side-label">WORKSPACE</div>
        <button className="nav active" onClick={() => setActiveTab("editor")}>
          <span>⌘</span> Code Editor
        </button>
        <button className="nav" onClick={() => setActiveTab("results")}>
          <span>⌕</span> Bug Analysis
        </button>
        <button className="nav" onClick={() => setActiveTab("repair")}>
          <span>✧</span> AI Repair
        </button>
        <button className="nav" onClick={() => setActiveTab("history")}>
          <span>◷</span> History
        </button>

        <div className="sidebar-bottom">
          <div className="connection">
            <span className={status === "Connected" ? "dot online" : "dot"} />
            <div>
              <strong>{status}</strong>
              <small>Backend API</small>
            </div>
          </div>
          <p>AutoPatch v1.0 · Hackathon Edition</p>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace /</span>
            <strong> AutoPatch Dashboard</strong>
          </div>
          <div className="top-right">
            <span className="status-pill">
              <span className={status === "Connected" ? "dot online" : "dot"} />
              {status}
            </span>
            <div className="avatar">AP</div>
          </div>
        </header>

        <section className="welcome">
          <div>
            <span className="eyebrow">AUTONOMOUS DEBUGGING PLATFORM</span>
            <h1>Code smarter. <span>Fix faster.</span></h1>
            <p>Detect bugs, generate AI-powered fixes and validate your code in a secure sandbox.</p>
          </div>
          <div className="welcome-icon">✧</div>
        </section>

        <section className="stats">
          <div className="stat-card">
            <span>Total submissions</span>
            <strong>{history.length}</strong>
            <small>Stored in SQL history</small>
          </div>
          <div className="stat-card">
            <span>Detected issues</span>
            <strong>{bugs.length}</strong>
            <small>Current analysis</small>
          </div>
          <div className="stat-card">
            <span>Repair status</span>
            <strong className="stat-status">{fixedCode ? "Ready" : "Waiting"}</strong>
            <small>AI repair engine</small>
          </div>
          <div className="stat-card">
            <span>Environment</span>
            <strong className="stat-status">Python</strong>
            <small>Docker sandbox</small>
          </div>
        </section>

        <div className="workspace">
          <section className="editor-panel">
            <div className="panel-heading">
              <div>
                <h3>Code Workspace</h3>
                <span>Write or paste your Python code</span>
              </div>
              <span className="language-tag">PYTHON</span>
            </div>

            <div className="editor-toolbar">
              <span><i className="python-dot" /> main.py</span>
              <button onClick={() => { setCode(SAMPLE_CODE); setFixedCode(""); }}>
                Reset sample
              </button>
            </div>

            <textarea
              className="code-editor"
              spellCheck="false"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Write your Python code here..."
            />

            <div className="editor-footer">
              <span>Python · UTF-8</span>
              <span>{code.split("\n").length} lines</span>
            </div>

            <div className="actions">
              <button className="btn primary" disabled={!!loading || !code.trim()} onClick={analyzeCode}>
                {loading === "analyze" ? "Analyzing..." : "⌕ Analyze Bugs"}
              </button>
              <button className="btn ai" disabled={!!loading || !code.trim()} onClick={repairCode}>
                {loading === "repair" ? "Repairing..." : "✧ AI Auto Repair"}
              </button>
              <button className="btn secondary" disabled={!!loading || !(fixedCode || code).trim()} onClick={validateCode}>
                {loading === "validate" ? "Validating..." : "▷ Validate"}
              </button>
            </div>
          </section>

          <section className="output-panel">
            <div className="tabs">
              <button className={activeTab === "editor" ? "selected" : ""} onClick={() => setActiveTab("editor")}>Overview</button>
              <button className={activeTab === "results" ? "selected" : ""} onClick={() => setActiveTab("results")}>Analysis</button>
              <button className={activeTab === "repair" ? "selected" : ""} onClick={() => setActiveTab("repair")}>AI Repair</button>
              <button className={activeTab === "history" ? "selected" : ""} onClick={() => { setActiveTab("history"); loadHistory(); }}>History</button>
            </div>

            {error && <div className="error-box">⚠ {error}</div>}

            {activeTab === "editor" && (
              <div className="empty-state">
                <div className="empty-icon">⌘</div>
                <h3>Ready to analyze</h3>
                <p>Submit your code to detect potential bugs and security issues.</p>
                <div className="feature-list">
                  <div>✓ Static bug detection</div>
                  <div>✓ AI-powered code correction</div>
                  <div>✓ Secure sandbox validation</div>
                </div>
              </div>
            )}

            {activeTab === "results" && (
              <div className="result-content">
                <h3>Analysis results</h3>
                {bugs.length > 0 ? bugs.map((bug, i) => (
                  <div className="bug-card" key={i}>
                    <span className="bug-type">{bug.type || bug.category || "Issue"}</span>
                    <p>{bug.message || bug.description || JSON.stringify(bug)}</p>
                    <small>Line: {bug.line || bug.line_number || "Not specified"}</small>
                  </div>
                )) : (
                  <p className="muted">
                    {result ? "No bug details were returned by the API. Check the response below." : "No analysis submitted yet."}
                  </p>
                )}
                {result && <pre className="response-box">{JSON.stringify(result, null, 2)}</pre>}
              </div>
            )}

            {activeTab === "repair" && (
              <div className="result-content">
                <h3>AI repair output</h3>
                {fixedCode ? (
                  <>
                    <span className="success-label">Repaired code received</span>
                    <pre className="code-output">{fixedCode}</pre>
                    <button className="btn secondary" onClick={() => setCode(fixedCode)}>Use repaired code</button>
                  </>
                ) : (
                  <p className="muted">Click AI Auto Repair to request a fix from Groq.</p>
                )}
                {result && <pre className="response-box">{JSON.stringify(result, null, 2)}</pre>}
              </div>
            )}

            {activeTab === "history" && (
              <div className="result-content">
                <div className="history-heading">
                  <h3>Submission history</h3>
                  <button onClick={loadHistory}>Refresh</button>
                </div>
                {history.length ? history.map((item) => (
                  <div className="history-card" key={item.id}>
                    <strong>Submission #{item.id}</strong>
                    <span>{item.status || item.repair_mode || "Saved"}</span>
                    <small>{item.created_at || ""}</small>
                    <button onClick={() => {
                      setCode(item.original_code || "");
                      setFixedCode(item.fixed_code || "");
                      setActiveTab("editor");
                    }}>Load code</button>
                  </div>
                )) : <p className="muted">No saved submissions yet.</p>}
              </div>
            )}
          </section>
        </div>

        <footer className="footer">
          <span>AutoPatch · Autonomous Software Bug Detection & Repair</span>
          <span>Powered by Python · Groq AI · Docker · SQL</span>
        </footer>
      </main>
    </div>
  );
}
