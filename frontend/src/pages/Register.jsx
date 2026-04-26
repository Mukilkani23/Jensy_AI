import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { registerStudent } from '../api/api';
import './Auth.css';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await registerStudent({ name, email, password });
      login(res.data.token, res.data.student_id);
      navigate('/onboarding');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card glass-card animate-fadeInUp">
        <div className="auth-header">
          <span className="auth-icon">🚀</span>
          <h1>Join GENZ</h1>
          <p>Create your academic companion account</p>
        </div>
        <form onSubmit={handleSubmit} id="register-form">
          {error && <div className="auth-error">{error}</div>}
          <div className="form-group">
            <label htmlFor="reg-name">Full Name</label>
            <input id="reg-name" type="text" className="form-input" placeholder="John Doe"
              value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="reg-email">Email</label>
            <input id="reg-email" type="email" className="form-input" placeholder="you@example.com"
              value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="reg-password">Password</label>
            <input id="reg-password" type="password" className="form-input" placeholder="Min 6 characters"
              value={password} onChange={e => setPassword(e.target.value)} required minLength={6} />
          </div>
          <button type="submit" className="btn-primary auth-submit" disabled={loading}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
