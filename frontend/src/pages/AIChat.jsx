import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { sendAIChat, getConversations, getBehavior } from '../api/api';
import './AIChat.css';

export default function AIChat() {
  const { studentId } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState('chat'); // 'chat' | 'behavior'
  const [behavior, setBehavior] = useState(null);
  const [tokenQuota, setTokenQuota] = useState(0);
  const maxQuota = 10000; // arbitrary max for meter
  const messagesEndRef = useRef(null);


  useEffect(() => {
    if (studentId) loadConversations();
  }, [studentId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadConversations = async () => {
    try {
      const res = await getConversations(studentId);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error('Failed to load conversations');
    }
  };

  const loadBehavior = async () => {
    try {
      const res = await getBehavior(studentId);
      setBehavior(res.data);
    } catch (err) {
      console.error('Failed to load behavior');
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendAIChat({ student_id: studentId, message: input });
      const aiMsg = { role: 'assistant', content: res.data.response, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, aiMsg]);
      if (res.data.daily_tokens !== undefined) {
        setTokenQuota(res.data.daily_tokens);
      }
    } catch (err) {

      const errMsg = { role: 'assistant', content: 'Sorry, I had trouble processing that. Please try again.', timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (newTab) => {
    setTab(newTab);
    if (newTab === 'behavior') loadBehavior();
  };

  return (
    <div className="chat-page">
      <div className="page-container">
        <div className="chat-layout">
          {/* Main Chat */}
          <div className="chat-main glass-card">
            <div className="chat-tabs">
              <button className={`chat-tab ${tab === 'chat' ? 'active' : ''}`} onClick={() => handleTabChange('chat')}>
                💬 Chat
              </button>
              <button className={`chat-tab ${tab === 'behavior' ? 'active' : ''}`} onClick={() => handleTabChange('behavior')}>
                📊 Behavior Report
              </button>
            </div>
            
            {tab === 'chat' && (
              <div className="quota-meter" style={{ padding: '0 1.5rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Daily AI Quota</span>
                <div className="progress-bar" style={{ height: '6px', flex: 1, maxWidth: '200px' }}>
                  <div className="progress-fill" style={{ width: `${Math.min(100, (tokenQuota / maxQuota) * 100)}%`, background: tokenQuota > maxQuota * 0.8 ? '#ef4444' : '#10b981' }}></div>
                </div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{tokenQuota} / {maxQuota}</span>
              </div>
            )}

            {tab === 'chat' ? (

              <>
                <div className="chat-messages" id="chat-messages">
                  {messages.length === 0 && (
                    <div className="chat-empty">
                      <span className="chat-empty-icon">🤖</span>
                      <h3>Hi! I'm your GENZ AI assistant</h3>
                      <p>Ask me about your subjects, study plans, resources, or anything academic!</p>
                      <div className="chat-suggestions">
                        <button onClick={() => setInput('What should I study this semester?')} className="suggestion-btn">
                          📚 What to study this semester?
                        </button>
                        <button onClick={() => setInput('Give me a weekly study plan')} className="suggestion-btn">
                          📅 Weekly study plan
                        </button>
                        <button onClick={() => setInput('Explain Data Structures simply')} className="suggestion-btn">
                          🧠 Explain a topic
                        </button>
                      </div>
                    </div>
                  )}
                  {messages.map((msg, i) => (
                    <div key={i} className={`chat-bubble ${msg.role}`}>
                      <div className="bubble-avatar">
                        {msg.role === 'user' ? '👤' : '⚡'}
                      </div>
                      <div className="bubble-content">
                        <pre className="bubble-text">{msg.content}</pre>
                        <span className="bubble-time">
                          {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                        </span>
                      </div>
                    </div>
                  ))}
                  {loading && (
                    <div className="chat-bubble assistant">
                      <div className="bubble-avatar">⚡</div>
                      <div className="bubble-content">
                        <div className="typing-indicator">
                          <span></span><span></span><span></span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
                <form className="chat-input-bar" onSubmit={handleSend} id="chat-form">
                  <input
                    id="chat-input"
                    type="text"
                    className="form-input chat-input"
                    placeholder="Ask anything about your academics..."
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    disabled={loading}
                  />
                  <button type="submit" className="btn-primary chat-send" disabled={loading || !input.trim()}>
                    Send
                  </button>
                </form>
              </>
            ) : (
              <div className="behavior-panel">
                {!behavior ? (
                  <div className="loading-page"><div className="loading-spinner"></div><p>Analyzing your behavior...</p></div>
                ) : (
                  <div className="behavior-content animate-fadeInUp">
                    <h2>📊 Your Behavior Report</h2>
                    <div className="behavior-grid">
                      <div className="behavior-card glass-card">
                        <h4>💪 Strong Subjects</h4>
                        {behavior.strong_subjects?.length > 0 ? (
                          <ul>{behavior.strong_subjects.map(s => <li key={s}>{s}</li>)}</ul>
                        ) : <p className="text-muted">Not enough data yet</p>}
                      </div>
                      <div className="behavior-card glass-card">
                        <h4>⚠️ Needs Improvement</h4>
                        {behavior.weak_subjects?.length > 0 ? (
                          <ul>{behavior.weak_subjects.map(s => <li key={s}>{s}</li>)}</ul>
                        ) : <p className="text-muted">Not enough data yet</p>}
                      </div>
                      <div className="behavior-card glass-card">
                        <h4>🧠 Study Pattern</h4>
                        <p className="pattern-value">{behavior.study_pattern || 'Unknown'}</p>
                      </div>
                      <div className="behavior-card glass-card">
                        <h4>⏱️ Total Study Time</h4>
                        <p className="pattern-value">{behavior.total_study_time_mins || 0} mins</p>
                      </div>
                    </div>
                    <div className="recommendations glass-card">
                      <h4>🎯 Recommendations</h4>
                      <ul>
                        {(behavior.recommended_actions || []).map((r, i) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
