import React, { useState } from 'react';
import './App.css';

function App() {
  const [ticketText, setTicketText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copyStatus, setCopyStatus] = useState('');
  const [activeTab, setActiveTab] = useState('analyzer');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const analyzeTicket = async () => {
    if (!ticketText.trim()) {
      setError('Please enter ticket text');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
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

  const useDemoText = (text) => {
    setTicketText(text);
    setError('');
  };

  const getPriorityClass = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return '';
    }
  };

  const formatConfidence = (confidence) => {
    if (typeof confidence !== 'number') return null;
    return `${Math.round(confidence * 100)}%`;
  };

  const copyResponse = async () => {
    if (!result?.response) return;
    try {
      await navigator.clipboard.writeText(result.response);
      setCopyStatus('Copied!');
      setTimeout(() => setCopyStatus(''), 1500);
    } catch (_) {
      setCopyStatus('Copy failed');
      setTimeout(() => setCopyStatus(''), 1500);
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-dot"></span>
          <span>TicketAI Console</span>
        </div>
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'analyzer' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyzer')}
            type="button"
          >
            Analyzer
          </button>
          <button className="tab" type="button" disabled>
            History
          </button>
          <button className="tab" type="button" disabled>
            Settings
          </button>
        </div>
      </header>

      <main className="layout">
        <section className="panel input-panel">
          <div className="panel-header">
            <h1>Analyze Support Ticket</h1>
            <p>Classify intent, detect entities, assign priority, and draft a response.</p>
          </div>

          <label className="label" htmlFor="ticket-input">Ticket Description</label>
          <textarea
            id="ticket-input"
            value={ticketText}
            onChange={(e) => setTicketText(e.target.value)}
            placeholder="Example: I can't login, and password reset email is not arriving."
            rows="7"
            disabled={loading}
          />
          <div className="input-meta">
            <span>{ticketText.length} chars</span>
            <span>{ticketText.trim().split(/\s+/).filter(Boolean).length} words</span>
          </div>

          <div className="sample-row">
            <button
              className="sample-btn"
              type="button"
              onClick={() => useDemoText('I was charged twice for one subscription payment.')}
            >
              Billing Sample
            </button>
            <button
              className="sample-btn"
              type="button"
              onClick={() => useDemoText('The app crashes when I upload an invoice PDF.')}
            >
              Technical Sample
            </button>
            <button
              className="sample-btn"
              type="button"
              onClick={() => useDemoText('I cannot login and I am not receiving verification code.')}
            >
              Account Sample
            </button>
          </div>

          <button
            onClick={analyzeTicket}
            disabled={loading || !ticketText.trim()}
            className={`analyze-btn ${loading ? 'loading' : ''}`}
            type="button"
          >
            {loading ? 'Analyzing...' : 'Analyze Ticket'}
          </button>

          {error && <div className="error-box">{error}</div>}
        </section>

        <section className="panel output-panel">
          <div className="panel-header">
            <h2>Analysis Result</h2>
            <p>AI outputs are shown here after submitting a ticket.</p>
          </div>

          {!result ? (
            <div className="empty-state">
              <p>No analysis yet. Submit a ticket to see intent, entities, priority, and response.</p>
            </div>
          ) : (
            <>
              <div className="stat-grid">
                <div className="stat-card">
                  <span className="stat-label">Intent</span>
                  <span className="stat-value">{result.intent || 'unknown'}</span>
                </div>
                <div className={`stat-card ${getPriorityClass(result.priority)}`}>
                  <span className="stat-label">Priority</span>
                  <span className="stat-value">{result.priority || 'Low'}</span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">Confidence</span>
                  <span className="stat-value">{formatConfidence(result.confidence) || 'N/A'}</span>
                </div>
              </div>
              {result.needs_review && (
                <div className="error-box">
                  Low confidence prediction. Manual review is recommended.
                </div>
              )}

              <div className="entity-section">
                <h3>Entities</h3>
                {result.entities && Object.keys(result.entities).length > 0 ? (
                  <div className="entities-list">
                    {Object.entries(result.entities).map(([key, value]) => (
                      <span key={key} className="entity-chip">
                        <strong>{key}:</strong> {Array.isArray(value) ? value.join(', ') : String(value)}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="muted">No entities detected.</p>
                )}
              </div>

              <div className="response-section">
                <h3>Suggested Response</h3>
                <p className="response-text">{result.response}</p>
                <button className="copy-btn" onClick={copyResponse} type="button">
                  {copyStatus || 'Copy Response'}
                </button>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;