import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getDashboard, updateProgress } from '../api/api';
import './Dashboard.css';

export default function Dashboard() {
  const { studentId, logout } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openSem, setOpenSem] = useState(null);

  useEffect(() => {
    if (studentId) {
      fetchDashboard();
    } else {
      setLoading(false);
    }
  }, [studentId]);

  const fetchDashboard = async () => {
    try {
      const res = await getDashboard(studentId);
      if (!res.data.degree) {
         navigate('/onboarding');
         return;
      }
      setData(res.data);
      setOpenSem(res.data.semester_current || 1);
    } catch (err) {
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProgressUpdate = async (semester, subjectCode, newPct) => {
    try {
      await updateProgress({
        student_id: studentId,
        semester,
        subject_code: subjectCode,
        completion_pct: newPct,
        time_spent_mins: 0,
      });
      fetchDashboard();
    } catch (err) {
      console.error('Progress update error:', err);
    }
  };

  if (loading) {
    return (
      <div className="loading-page">
        <div className="loading-spinner"></div>
        <p>Loading your dashboard...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="loading-page">
        <p>No dashboard data available. Please complete your setup.</p>
        <button className="btn-primary" onClick={() => navigate('/onboarding')}>Complete Onboarding</button>
        <button className="btn-secondary" style={{marginLeft: '10px'}} onClick={logout}>Sign Out</button>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="page-container">
        {/* Header */}
        <div className="dash-header animate-fadeInUp">
          <div>
            <h1>👋 Hey, {data.student_name}!</h1>
            <p className="dash-subtitle">
              {data.degree} {data.regulation && `• ${data.regulation}`} • Semester {data.semester_current}
            </p>
          </div>
          <div className="dash-preference-badge">
            <span className={`badge badge-${data.preference === 'coding' ? 'coding' : data.preference === 'noncoding' ? 'noncoding' : 'theory'}`}>
              {data.preference === 'coding' ? '💻 Coding Track' : data.preference === 'noncoding' ? '📖 Non-Coding' : '⚖️ Balanced'}
            </span>
          </div>
        </div>

        {/* Stats */}
        <div className="dash-stats stagger">
          <div className="stat-card glass-card">
            <div className="stat-value">{data.stats?.total_subjects || 0}</div>
            <div className="stat-label-d">Total Subjects</div>
          </div>
          <div className="stat-card glass-card">
            <div className="stat-value accent-green">{data.stats?.completed_subjects || 0}</div>
            <div className="stat-label-d">Completed</div>
          </div>
          <div className="stat-card glass-card">
            <div className="stat-value accent-purple">{data.stats?.overall_completion || 0}%</div>
            <div className="stat-label-d">Overall Progress</div>
          </div>
          <div className="stat-card glass-card">
            <div className="stat-value accent-pink">{data.semesters?.length || 8}</div>
            <div className="stat-label-d">Semesters</div>
          </div>
        </div>

        {/* Gamification / XP System */}
        <div className="gamification-section glass-card animate-fadeInUp" style={{ marginBottom: '2.5rem', padding: '1.5rem' }}>
          <div className="gamification-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="section-title" style={{ margin: 0 }}>🎮 Your Academic Journey</h2>
            <div className="streak-badge" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255, 107, 157, 0.2)', padding: '0.5rem 1rem', borderRadius: '20px', color: '#ff6b9d', fontWeight: 'bold' }}>
              🔥 {data.xp_system?.streak || 0} Day Streak
            </div>
          </div>
          
          <div className="xp-container" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span>Total XP: <strong className="accent-purple">{data.xp_system?.total_xp || 0} XP</strong></span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Next Badge at {((Math.floor((data.xp_system?.total_xp || 0) / 500) + 1) * 500)} XP</span>
            </div>
            <div className="progress-bar" style={{ height: '12px' }}>
              <div 
                className="progress-fill" 
                style={{ 
                  width: `${((data.xp_system?.total_xp || 0) % 500) / 5}%`,
                  background: 'linear-gradient(90deg, #7c5cfc, #a78bfa)' 
                }}
              ></div>
            </div>
          </div>

          <div className="badges-shelf">
            <h4 style={{ marginBottom: '0.75rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Earned Badges</h4>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {data.xp_system?.badges?.length > 0 ? (
                data.xp_system.badges.map((badge, idx) => (
                  <div key={idx} className="badge-item" style={{ 
                    background: 'rgba(255,255,255,0.05)', 
                    border: '1px solid rgba(255,255,255,0.1)', 
                    padding: '0.5rem 1rem', 
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <span>🏆</span> {badge}
                  </div>
                ))
              ) : (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>
                  Complete subjects, chat with AI, or upload resources to earn your first badge!
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Semester Blocks */}

        <div className="semesters-section">
          <h2 className="section-title">📚 Your Semester Roadmap</h2>
          <div className="semester-list stagger">
            {(data.semesters || []).map((sem) => (
              <div key={sem.semester} className={`semester-block glass-card ${openSem === sem.semester ? 'open' : ''}`}>
                <button className="semester-header" onClick={() => setOpenSem(openSem === sem.semester ? null : sem.semester)}>
                  <div className="sem-info">
                    <span className="sem-number">Semester {sem.semester}</span>
                    <span className="sem-count">{sem.subjects.length} subjects</span>
                  </div>
                  <div className="sem-right">
                    <div className="sem-progress-mini">
                      <div className="progress-bar" style={{ width: '80px' }}>
                        <div className="progress-fill" style={{
                          width: `${sem.subjects.length > 0 ? sem.subjects.reduce((a, s) => a + (s.progress?.completion_pct || 0), 0) / sem.subjects.length : 0}%`
                        }}></div>
                      </div>
                    </div>
                    <span className="sem-toggle">{openSem === sem.semester ? '▲' : '▼'}</span>
                  </div>
                </button>
                {openSem === sem.semester && (
                  <div className="semester-body animate-fadeIn">
                    <div className="subject-list">
                      {sem.subjects.map((subj) => (
                        <div key={subj.code} className="subject-row">
                          <div className="subj-info">
                            <span className={`badge ${subj.type === 'lab' ? 'badge-lab' : 'badge-theory'}`}>
                              {subj.type}
                            </span>
                            <span className="subj-code">{subj.code}</span>
                            <span className="subj-name">{subj.name}</span>
                          </div>
                          <div className="subj-right">
                            <span className="subj-credits">{subj.credits} cr</span>
                            <div className="subj-progress">
                              <div className="progress-bar">
                                <div className="progress-fill" style={{ width: `${subj.progress?.completion_pct || 0}%` }}></div>
                              </div>
                              <span className="progress-pct">{Math.round(subj.progress?.completion_pct || 0)}%</span>
                            </div>
                            <div className="subj-actions">
                              <button className="btn-tiny" onClick={() => handleProgressUpdate(sem.semester, subj.code, Math.min((subj.progress?.completion_pct || 0) + 10, 100))}>
                                +10%
                              </button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    {data.preference === 'coding' && (
                      <div className="track-info glass-card">
                        <h4>💻 Coding Track — Semester {sem.semester}</h4>
                        <p>Focus on DSA problems: arrays, linked lists, trees. Build a mini-project using concepts from this semester.</p>
                      </div>
                    )}
                    {data.preference === 'noncoding' && (
                      <div className="track-info glass-card">
                        <h4>📖 Theory Track — Semester {sem.semester}</h4>
                        <p>Deep dive into core concepts. Research papers and case studies recommended for depth.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
