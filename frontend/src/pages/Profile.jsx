import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getStudent, updateStudent } from '../api/api';
import './Profile.css';

export default function Profile() {
  const { studentId, logout } = useAuth();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    if (studentId) fetchProfile();
  }, [studentId]);

  const fetchProfile = async () => {
    try {
      const res = await getStudent(studentId);
      setStudent(res.data);
      setEditData({
        preference: res.data.preference || 'balanced',
        semester_current: res.data.semester_current || 1,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      await updateStudent(studentId, editData);
      setEditing(false);
      fetchProfile();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <div className="loading-page"><div className="loading-spinner"></div></div>;
  }

  if (!student) {
    return <div className="loading-page"><p>Profile not found.</p></div>;
  }

  return (
    <div className="profile-page">
      <div className="page-container">
        <div className="profile-header animate-fadeInUp">
          <div className="profile-avatar">
            {student.name?.charAt(0)?.toUpperCase() || '?'}
          </div>
          <div>
            <h1>{student.name}</h1>
            <p className="profile-email">{student.email}</p>
          </div>
        </div>

        <div className="profile-grid stagger">
          <div className="profile-card glass-card">
            <h3>🎓 Academic Info</h3>
            <div className="profile-fields">
              <div className="pf-row">
                <span className="pf-label">Degree</span>
                <span className="pf-value">{student.degree || 'Not set'}</span>
              </div>
              <div className="pf-row">
                <span className="pf-label">Branch</span>
                <span className="pf-value">{student.branch || 'N/A'}</span>
              </div>
              <div className="pf-row">
                <span className="pf-label">College Type</span>
                <span className="pf-value">{student.college_type || 'Not set'}</span>
              </div>
              <div className="pf-row">
                <span className="pf-label">Regulation</span>
                <span className="pf-value">{student.regulation || 'Not set'}</span>
              </div>
              <div className="pf-row">
                <span className="pf-label">Current Semester</span>
                <span className="pf-value">
                  {editing ? (
                    <select className="form-input pf-select" value={editData.semester_current}
                      onChange={e => setEditData({...editData, semester_current: parseInt(e.target.value)})}>
                      {[1,2,3,4,5,6,7,8].map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                  ) : student.semester_current}
                </span>
              </div>
            </div>
          </div>

          <div className="profile-card glass-card">
            <h3>🧭 Preferences</h3>
            <div className="profile-fields">
              <div className="pf-row">
                <span className="pf-label">Learning Track</span>
                <span className="pf-value">
                  {editing ? (
                    <select className="form-input pf-select" value={editData.preference}
                      onChange={e => setEditData({...editData, preference: e.target.value})}>
                      <option value="coding">💻 Coding</option>
                      <option value="noncoding">📖 Non-Coding</option>
                      <option value="balanced">⚖️ Balanced</option>
                    </select>
                  ) : (
                    <span className={`badge badge-${student.preference === 'coding' ? 'coding' : 'noncoding'}`}>
                      {student.preference || 'balanced'}
                    </span>
                  )}
                </span>
              </div>
            </div>
            <div className="profile-actions">
              {editing ? (
                <>
                  <button className="btn-primary btn-small" onClick={handleSave}>Save Changes</button>
                  <button className="btn-secondary btn-small" onClick={() => setEditing(false)}>Cancel</button>
                </>
              ) : (
                <button className="btn-secondary btn-small" onClick={() => setEditing(true)}>✏️ Edit Preferences</button>
              )}
            </div>
          </div>

          <div className="profile-card glass-card">
            <h3>📊 Behavior Stats</h3>
            <div className="profile-fields">
              <div className="pf-row">
                <span className="pf-label">Strong Subjects</span>
                <span className="pf-value">
                  {student.behavior_profile?.strong_subjects?.length > 0
                    ? student.behavior_profile.strong_subjects.join(', ')
                    : 'Not enough data'}
                </span>
              </div>
              <div className="pf-row">
                <span className="pf-label">Weak Subjects</span>
                <span className="pf-value">
                  {student.behavior_profile?.weak_subjects?.length > 0
                    ? student.behavior_profile.weak_subjects.join(', ')
                    : 'Not enough data'}
                </span>
              </div>
              <div className="pf-row">
                <span className="pf-label">Avg Daily Study</span>
                <span className="pf-value">
                  {student.behavior_profile?.avg_daily_time_mins || 0} mins
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="profile-danger">
          <button className="btn-secondary" onClick={logout} style={{ color: 'var(--accent-tertiary)', borderColor: 'rgba(255,107,157,0.3)' }}>
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  );
}
