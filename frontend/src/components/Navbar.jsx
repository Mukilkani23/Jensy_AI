import { useState, useEffect } from 'react';

import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import './Navbar.css';


export default function Navbar() {
  const { isAuthenticated, logout, token } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifsOpen, setNotifsOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (isAuthenticated && token) {
      axios.get('http://localhost:8000/student/me/notifications', {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => setNotifications(res.data.notifications || []))
      .catch(err => console.error("Failed to fetch notifications"));
    }
  }, [isAuthenticated, token]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };


  return (
    <nav className="navbar">
      <div className="nav-inner">
        <Link to="/" className="nav-logo">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">GENZ</span>
        </Link>

        <button className="nav-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          <span></span><span></span><span></span>
        </button>

        <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/chat" className="nav-link">AI Chat</Link>
              <Link to="/resources" className="nav-link">Resources</Link>
              <Link to="/planner" className="nav-link">Planner</Link>
              <Link to="/career" className="nav-link">Career</Link>
              <Link to="/analytics" className="nav-link">Analytics</Link>
              <Link to="/profile" className="nav-link">Profile</Link>

              
              <div className="nav-notifs" onClick={() => setNotifsOpen(!notifsOpen)} style={{position: 'relative', cursor: 'pointer', margin: '0 10px'}}>
                <span className="bell-icon" style={{fontSize: '1.2rem'}}>🔔</span>
                {notifications.length > 0 && <span className="notif-badge" style={{position: 'absolute', top: '-5px', right: '-10px', background: 'red', color: 'white', borderRadius: '50%', padding: '2px 5px', fontSize: '0.6rem'}}>{notifications.length}</span>}
                {notifsOpen && (
                  <div className="notifs-dropdown" style={{position: 'absolute', top: '30px', right: '0', background: '#1e293b', padding: '10px', borderRadius: '5px', width: '250px', zIndex: 100, boxShadow: '0 4px 6px rgba(0,0,0,0.1)'}}>
                    {notifications.length === 0 ? <p style={{fontSize: '0.8rem', color: '#94a3b8'}}>No new notifications</p> : 
                      notifications.map(n => (
                        <div key={n.id} style={{padding: '8px', borderBottom: '1px solid #334155', fontSize: '0.85rem'}}>
                          {n.message}
                        </div>
                      ))
                    }
                  </div>
                )}
              </div>
              
              <button onClick={handleLogout} className="nav-link nav-logout">Logout</button>

            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="btn-primary btn-small">Get Started</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
