import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { setupOnboarding, scrapeCollege } from '../api/api';
import './Onboarding.css';

const DEGREES = ['B.E/B.Tech', 'BSc', 'BCom', 'BBA', 'Other'];
const BRANCHES = ['CSE', 'ECE', 'Mech', 'EEE', 'Civil', 'IT', 'AI & DS', 'Other'];
const REGULATIONS = ['Regulation 2021', 'Regulation 2025', 'Regulation 2017'];

export default function Onboarding() {
  const [step, setStep] = useState(1);
  const [degree, setDegree] = useState('');
  const [branch, setBranch] = useState('');
  const [collegeType, setCollegeType] = useState('');
  const [collegeUrl, setCollegeUrl] = useState('');
  const [regulation, setRegulation] = useState('');
  const [preference, setPreference] = useState('');
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [error, setError] = useState('');
  const { studentId } = useAuth();
  const navigate = useNavigate();

  const nextStep = () => setStep(s => Math.min(s + 1, 4));
  const prevStep = () => setStep(s => Math.max(s - 1, 1));

  const handleScrape = async () => {
    if (!collegeUrl) return;
    setScraping(true);
    setError('');
    try {
      await scrapeCollege(collegeUrl);
    } catch {
      setError('Could not scrape syllabus. You can still proceed.');
    } finally {
      setScraping(false);
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    setError('');
    try {
      await setupOnboarding({
        degree,
        branch: branch || null,
        college_type: collegeType,
        college_url: collegeUrl || null,
        regulation: regulation || null,
        preference,
        semester_current: 1,
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-container">
        {/* Progress */}
        <div className="onboarding-progress">
          {[1, 2, 3, 4].map(s => (
            <div key={s} className={`progress-step ${step >= s ? 'active' : ''} ${step === s ? 'current' : ''}`}>
              <div className="step-dot">{step > s ? '✓' : s}</div>
              <span className="step-name">
                {s === 1 ? 'Degree' : s === 2 ? 'College' : s === 3 ? 'Regulation' : 'Preference'}
              </span>
            </div>
          ))}
          <div className="progress-line">
            <div className="progress-line-fill" style={{ width: `${((step - 1) / 3) * 100}%` }}></div>
          </div>
        </div>

        {error && <div className="auth-error">{error}</div>}

        {/* Step 1 - Degree */}
        {step === 1 && (
          <div className="onboarding-step animate-fadeInUp">
            <h2>🎓 What's your degree?</h2>
            <p className="step-desc">Select your bachelor's degree program</p>
            <div className="option-grid">
              {DEGREES.map(d => (
                <button key={d} className={`option-btn glass-card ${degree === d ? 'selected' : ''}`}
                  onClick={() => setDegree(d)}>
                  {d}
                </button>
              ))}
            </div>
            {degree === 'B.E/B.Tech' && (
              <div className="sub-options animate-fadeIn">
                <h3>Select your branch:</h3>
                <div className="option-grid small">
                  {BRANCHES.map(b => (
                    <button key={b} className={`option-btn glass-card ${branch === b ? 'selected' : ''}`}
                      onClick={() => setBranch(b)}>
                      {b}
                    </button>
                  ))}
                </div>
              </div>
            )}
            <div className="step-actions">
              <button className="btn-primary" onClick={nextStep} disabled={!degree}>
                Continue →
              </button>
            </div>
          </div>
        )}

        {/* Step 2 - College Type */}
        {step === 2 && (
          <div className="onboarding-step animate-fadeInUp">
            <h2>🏫 College Type</h2>
            <p className="step-desc">Is your college autonomous or affiliated?</p>
            <div className="option-grid">
              <button className={`option-btn glass-card big ${collegeType === 'autonomous' ? 'selected' : ''}`}
                onClick={() => setCollegeType('autonomous')}>
                <span className="opt-icon">🌐</span>
                <span className="opt-title">Autonomous</span>
                <span className="opt-desc">College has its own curriculum</span>
              </button>
              <button className={`option-btn glass-card big ${collegeType === 'affiliated' ? 'selected' : ''}`}
                onClick={() => setCollegeType('affiliated')}>
                <span className="opt-icon">🎓</span>
                <span className="opt-title">Affiliated</span>
                <span className="opt-desc">Follows university regulation</span>
              </button>
            </div>
            {collegeType === 'autonomous' && (
              <div className="sub-options animate-fadeIn">
                <div className="form-group">
                  <label>College Syllabus URL</label>
                  <input type="url" className="form-input" placeholder="https://your-college.ac.in/syllabus"
                    value={collegeUrl} onChange={e => setCollegeUrl(e.target.value)} />
                </div>
                <button className="btn-secondary btn-small" onClick={handleScrape} disabled={scraping || !collegeUrl}>
                  {scraping ? 'Scraping...' : '🔍 Scrape Syllabus'}
                </button>
              </div>
            )}
            <div className="step-actions">
              <button className="btn-secondary" onClick={prevStep}>← Back</button>
              <button className="btn-primary" onClick={nextStep} disabled={!collegeType}>
                Continue →
              </button>
            </div>
          </div>
        )}

        {/* Step 3 - Regulation */}
        {step === 3 && (
          <div className="onboarding-step animate-fadeInUp">
            <h2>📋 Select Regulation</h2>
            <p className="step-desc">Choose your university regulation/year</p>
            <div className="option-grid">
              {REGULATIONS.map(r => (
                <button key={r} className={`option-btn glass-card ${regulation === r ? 'selected' : ''}`}
                  onClick={() => setRegulation(r)}>
                  {r}
                </button>
              ))}
            </div>
            <div className="step-actions">
              <button className="btn-secondary" onClick={prevStep}>← Back</button>
              <button className="btn-primary" onClick={nextStep} disabled={!regulation}>
                Continue →
              </button>
            </div>
          </div>
        )}

        {/* Step 4 - Preference */}
        {step === 4 && (
          <div className="onboarding-step animate-fadeInUp">
            <h2>🧭 Your Learning Style</h2>
            <p className="step-desc">This helps GENZ personalize your experience</p>
            <div className="option-grid">
              <button className={`option-btn glass-card big ${preference === 'coding' ? 'selected' : ''}`}
                onClick={() => setPreference('coding')}>
                <span className="opt-icon">💻</span>
                <span className="opt-title">Coding Track</span>
                <span className="opt-desc">DSA roadmap, projects, competitive programming</span>
              </button>
              <button className={`option-btn glass-card big ${preference === 'noncoding' ? 'selected' : ''}`}
                onClick={() => setPreference('noncoding')}>
                <span className="opt-icon">📖</span>
                <span className="opt-title">Non-Coding Track</span>
                <span className="opt-desc">Theory depth, research topics, conceptual learning</span>
              </button>
              <button className={`option-btn glass-card big ${preference === 'balanced' ? 'selected' : ''}`}
                onClick={() => setPreference('balanced')}>
                <span className="opt-icon">⚖️</span>
                <span className="opt-title">Balanced</span>
                <span className="opt-desc">Mix of coding projects and theory study</span>
              </button>
            </div>
            <div className="step-actions">
              <button className="btn-secondary" onClick={prevStep}>← Back</button>
              <button className="btn-primary" onClick={handleFinish} disabled={!preference || loading}>
                {loading ? 'Setting up...' : '🚀 Launch Dashboard'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
