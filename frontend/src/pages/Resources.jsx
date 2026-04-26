import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { getResources, uploadResource, voteResource } from '../api/api';
import './Resources.css';


export default function Resources() {
  const { studentId } = useAuth();
  const [subjectCode, setSubjectCode] = useState('');
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  // Upload form
  const [showUpload, setShowUpload] = useState(false);
  const [uploadData, setUploadData] = useState({
    subject_code: '', semester: 1, type: 'note', title: '', url: ''
  });
  const [uploading, setUploading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!subjectCode.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const res = await getResources(subjectCode.trim().toUpperCase());
      setResources(res.data.resources || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    setUploading(true);
    try {
      await uploadResource(uploadData);
      setShowUpload(false);
      setUploadData({ subject_code: '', semester: 1, type: 'note', title: '', url: '' });
      // Refresh if same subject
      if (uploadData.subject_code.toUpperCase() === subjectCode.toUpperCase()) {
        const res = await getResources(subjectCode.trim().toUpperCase());
        setResources(res.data.resources || []);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleVote = async (e, id, vote) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      await voteResource(id, vote);
      const res = await getResources(subjectCode.trim().toUpperCase());
      setResources(res.data.resources || []);
    } catch (err) {
      console.error(err);
    }
  };

  const typeIcon = (t) => t === 'video' ? '🎥' : t === 'pyq' ? '📝' : '📄';


  return (
    <div className="resources-page">
      <div className="page-container">
        <div className="res-header animate-fadeInUp">
          <h1>📁 Resource Library</h1>
          <p>Search by subject code to find notes, videos, and previous year questions.</p>
        </div>

        <div className="res-search-bar glass-card">
          <form onSubmit={handleSearch} id="resource-search-form" className="res-search-form">
            <input
              id="resource-search-input"
              type="text"
              className="form-input"
              placeholder="Enter subject code (e.g. CS3351)"
              value={subjectCode}
              onChange={e => setSubjectCode(e.target.value)}
            />
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Searching...' : '🔍 Search'}
            </button>
          </form>
          <button className="btn-secondary btn-small" onClick={() => setShowUpload(!showUpload)}>
            {showUpload ? '✕ Cancel' : '➕ Upload Resource'}
          </button>
        </div>

        {/* Upload Form */}
        {showUpload && (
          <div className="upload-form glass-card animate-fadeInUp">
            <h3>Upload a Resource</h3>
            <form onSubmit={handleUpload} id="upload-form">
              <div className="upload-grid">
                <div className="form-group">
                  <label>Subject Code</label>
                  <input className="form-input" placeholder="CS3351" value={uploadData.subject_code}
                    onChange={e => setUploadData({...uploadData, subject_code: e.target.value})} required />
                </div>
                <div className="form-group">
                  <label>Semester</label>
                  <select className="form-input" value={uploadData.semester}
                    onChange={e => setUploadData({...uploadData, semester: parseInt(e.target.value)})}>
                    {[1,2,3,4,5,6,7,8].map(s => <option key={s} value={s}>Semester {s}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Type</label>
                  <select className="form-input" value={uploadData.type}
                    onChange={e => setUploadData({...uploadData, type: e.target.value})}>
                    <option value="note">📄 Note</option>
                    <option value="video">🎥 Video</option>
                    <option value="pyq">📝 PYQ</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Title</label>
                  <input className="form-input" placeholder="Unit 1 Notes" value={uploadData.title}
                    onChange={e => setUploadData({...uploadData, title: e.target.value})} required />
                </div>
              </div>
              <div className="form-group">
                <label>Resource URL</label>
                <input className="form-input" placeholder="https://drive.google.com/..." value={uploadData.url}
                  onChange={e => setUploadData({...uploadData, url: e.target.value})} required />
              </div>
              <button type="submit" className="btn-primary" disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload Resource'}
              </button>
            </form>
          </div>
        )}

        {/* Results */}
        {searched && (
          <div className="res-results animate-fadeInUp">
            <h2 className="section-title">
              {resources.length > 0 ? `Resources for ${subjectCode.toUpperCase()}` : 'No resources found'}
            </h2>
            {resources.length === 0 && (
              <p className="res-empty">No resources uploaded yet for this subject. Be the first to add one!</p>
            )}
            <div className="res-list">
              {resources.map(r => (
                <div key={r.id} className="res-card-wrapper" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <div className="res-vote" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', background: 'rgba(0,0,0,0.2)', padding: '0.5rem', borderRadius: '8px' }}>
                    <button onClick={(e) => handleVote(e, r.id, 1)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: '#10b981' }}>▲</button>
                    <span style={{ fontWeight: 'bold' }}>{(r.upvotes || 0) - (r.downvotes || 0)}</span>
                    <button onClick={(e) => handleVote(e, r.id, -1)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: '#ef4444' }}>▼</button>
                  </div>
                  <a href={r.url} target="_blank" rel="noopener noreferrer" className="res-card glass-card" style={{ flex: 1, textDecoration: 'none' }}>
                    <span className="res-icon">{typeIcon(r.type)}</span>
                    <div className="res-info">
                      <span className="res-title">{r.title}</span>
                      <span className="res-meta">
                        <span className={`badge ${r.type === 'video' ? 'badge-lab' : 'badge-theory'}`}>{r.type}</span>
                        <span>Sem {r.semester}</span>
                      </span>
                    </div>
                    <span className="res-arrow">→</span>
                  </a>
                </div>
              ))}

            </div>
          </div>
        )}
      </div>
    </div>
  );
}
