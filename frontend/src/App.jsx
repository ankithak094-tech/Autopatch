
import { useRef, useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  const selectFile = (selectedFile) => {
    if (selectedFile) setFile(selectedFile);
  };

  return (
    <div className="app-shell">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">A</div>
          <span>Auto<span className="purple">Patch</span></span>
        </div>

        <p className="nav-label">WORKSPACE</p>

        <nav className="navigation">
          <a className="nav-item active" href="#dashboard">
            <span>◈</span> Dashboard
          </a>
          <a className="nav-item" href="#upload">
            <span>↑</span> Upload Code
          </a>
          <a className="nav-item" href="#reports">
            <span>⌘</span> Bug Reports
          </a>
          <a className="nav-item" href="#patches">
            <span>⚒</span> Patch Suggestions
          </a>
          <a className="nav-item" href="#tests">
            <span>✓</span> Test Results
          </a>
          <a className="nav-item" href="#history">
            <span>◷</span> History
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot"></div>
          <span>System ready</span>
          <div className="version">v1.0</div>
        </div>
      </aside>

      <main className="main-area" id="dashboard">

        <header className="topbar">
          <div>
            <p className="breadcrumb">WORKSPACE / DASHBOARD</p>
            <h2>Overview</h2>
          </div>
          <div className="profile">
            <div className="avatar">A</div>
            <div>
              <strong>Developer</strong>
              <small>Project workspace</small>
            </div>
          </div>
        </header>

        <section className="hero">
          <div className="hero-content">
            <div className="eyebrow">
              ✦ YOUR INTELLIGENT CODE ASSISTANT
            </div>

            <h1>
              Your code deserves
              <br />
              <span>to run flawlessly.</span>
            </h1>

            <p>
              Detect bugs, discover root causes and generate
              safer code patches — all in one workspace.
            </p>

            <button
              className="primary-button"
              onClick={() => document.getElementById("upload").scrollIntoView({behavior:"smooth"})}
            >
              Start analyzing <span>→</span>
            </button>
          </div>

          <div className="hero-visual">
            <div className="orbit orbit-one"></div>
            <div className="orbit orbit-two"></div>
            <div className="core">
              <span>✦</span>
            </div>
            <div className="floating-card float-one">
              <span className="green-dot"></span>
              Code analysis
              <strong>Ready</strong>
            </div>
            <div className="floating-card float-two">
              <span>⌘</span> Smart repair
              <strong>Enabled</strong>
            </div>
          </div>
        </section>

        <section className="section-heading">
          <div>
            <h2>Workspace overview</h2>
            <p>Your code quality at a glance</p>
          </div>
          <span className="live-tag">● LIVE WORKSPACE</span>
        </section>

        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-top">
              <span>Total bugs</span>
              <span className="stat-icon blue-icon">⌘</span>
            </div>
            <h2>--</h2>
            <small>Awaiting first scan</small>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Critical issues</span>
              <span className="stat-icon red-icon">!</span>
            </div>
            <h2>--</h2>
            <small>Severity analysis pending</small>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Patches generated</span>
              <span className="stat-icon purple-icon">⚒</span>
            </div>
            <h2>--</h2>
            <small>No patches generated yet</small>
          </div>

          <div className="stat-card">
            <div className="stat-top">
              <span>Tests passed</span>
              <span className="stat-icon green-icon">✓</span>
            </div>
            <h2>--</h2>
            <small>Validation pending</small>
          </div>
        </section>

        <section className="workspace-grid">

          <div className="upload-panel" id="upload">
            <div className="panel-heading">
              <div>
                <h2>Start a new analysis</h2>
                <p>Upload your source code to find hidden issues.</p>
              </div>
              <span className="step-label">STEP 01</span>
            </div>

            <div
              className={`dropzone ${dragging ? "dragging" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragging(false);
                selectFile(e.dataTransfer.files[0]);
              }}
              onClick={() => inputRef.current.click()}
            >
              <input
                ref={inputRef}
                type="file"
                hidden
                accept=".py,.js,.jsx,.java,.c,.cpp,.html,.css"
                onChange={(e) => selectFile(e.target.files[0])}
              />

              <div className="upload-icon">↑</div>
              <h3>{file ? file.name : "Drop your code here"}</h3>
              <p>
                {file
                  ? "File selected successfully"
                  : "or click to browse files from your computer"}
              </p>
              <span className="file-types">
                PY · JS · JSX · JAVA · C · CPP · HTML · CSS
              </span>
            </div>

            <div className="upload-footer">
              <span>◇ Your code stays under your control</span>
              <button
                className="scan-button"
                disabled={!file}
                onClick={() => alert("Upload interface ready. Backend scanning will be connected next.")}
              >
                Scan code →
              </button>
            </div>
          </div>

          <div className="process-panel">
            <h2>How AutoPatch works</h2>
            <p className="process-subtitle">
              From an error to a verified solution.
            </p>

            <div className="process-list">
              <div className="process-item">
                <div className="process-number">01</div>
                <div>
                  <h3>Detect</h3>
                  <p>Identify bugs and suspicious code.</p>
                </div>
              </div>

              <div className="process-item">
                <div className="process-number">02</div>
                <div>
                  <h3>Understand</h3>
                  <p>Analyze the likely root cause.</p>
                </div>
              </div>

              <div className="process-item">
                <div className="process-number">03</div>
                <div>
                  <h3>Generate</h3>
                  <p>Suggest focused code corrections.</p>
                </div>
              </div>

              <div className="process-item">
                <div className="process-number">04</div>
                <div>
                  <h3>Validate</h3>
                  <p>Run tests and review the results.</p>
                </div>
              </div>
            </div>
          </div>

        </section>

        <footer>
          <span>© 2026 AutoPatch</span>
          <span>Built for developers, designed for trust.</span>
        </footer>

      </main>
    </div>
  );
}

export default App;
