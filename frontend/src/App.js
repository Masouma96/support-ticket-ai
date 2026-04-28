import React, { useState } from 'react';
import './App.css';

function App() {
  const [ticketText, setTicketText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeTicket = async () => {
    if (!ticketText.trim()) {
      setError('Please enter ticket text');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: ticketText }),
      });

      if (!response.ok) {
        throw new Error('Server connection error');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Error analyzing ticket. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getPriorityClass = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return '';
    }
  };

  return (
    <div className="app">
      <div className="background-pattern"></div>
      
      <header className="navbar">
        <div className="logo">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">TicketAI</span>
        </div>
        <div className="nav-links">
          <span className="nav-item active">Analyzer</span>
          <span className="nav-item">History</span>
          <span className="nav-item">Settings</span>
        </div>
      </header>

      <main className="main">
        <div className="hero-section">
          <h1>Intelligent Support Ticket Analyzer</h1>
          <p>AI-powered analysis to categorize, prioritize, and generate responses</p>
        </div>

        <div className="analyzer-card">
          <div className="input-group">
            <label>Describe your issue</label>
            <textarea
              value={ticketText}
              onChange={(e) => setTicketText(e.target.value)}
              placeholder="e.g., I can't login to my account and need help resetting my password..."
              rows="4"
              disabled={loading}
            />
            <div className="input-footer">
              <span className="char-count">{ticketText.length} characters</span>
            </div>
          </div>

          <button 
            onClick={analyzeTicket} 
            disabled={loading || !ticketText.trim()}
            className={`analyze-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                Analyze Ticket
              </>
            )}
          </button>
          
          {error && <div className="error-toast">{error}</div>}
        </div>

        {result && (
          <div className="results-grid">
            <div className="result-card intent-card">
              <div className="card-header">
                <span className="card-icon">🎯</span>
                <h3>Intent</h3>
              </div>
              <div className="card-body">
                <span className="intent-badge">{result.intent}</span>
              </div>
            </div>

            <div className={`result-card priority-card ${getPriorityClass(result.priority)}`}>
              <div className="card-header">
                <span className="card-icon">⚡</span>
                <h3>Priority</h3>
              </div>
              <div className="card-body">
                <span className={`priority-badge ${getPriorityClass(result.priority)}`}>
                  {result.priority}
                </span>
              </div>
            </div>

            <div className="result-card entities-card">
              <div className="card-header">
                <span className="card-icon">🏷️</span>
                <h3>Entities</h3>
              </div>
              <div className="card-body">
                {result.entities && Object.keys(result.entities).length > 0 ? (
                  <div className="entities-list">
                    {Object.entries(result.entities).map(([key, value]) => (
                      <span key={key} className="entity-chip">
                        <span className="entity-key">{key}</span>
                        <span className="entity-value">{value}</span>
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="no-entities">No entities detected</span>
                )}
              </div>
            </div>

            <div className="result-card response-card">
              <div className="card-header">
                <span className="card-icon">💬</span>
                <h3>AI Response</h3>
              </div>
              <div className="card-body">
                <p className="response-text">{result.response}</p>
              </div>
              <div className="card-footer">
                <button className="copy-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
                  </svg>
                  Copy
                </button>
                <button className="edit-btn">Edit</button>
              </div>
            </div>
          </div>
        )}

        <footer className="footer">
          <p>Powered by Machine Learning • FastAPI • React</p>
        </footer>
      </main>
    </div>
  );
}

export default App;