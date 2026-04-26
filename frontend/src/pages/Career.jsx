import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './Career.css';

export default function Career() {
  const { token } = useAuth();
  const [resume, setResume] = useState('');
  const [interview, setInterview] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const generateCareer = async () => {
    setLoading(true);
    setCopied(false);
    try {
      const res = await axios.get('http://localhost:8000/career/generate', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResume(res.data.resume);
      setInterview(res.data.interview);
    } catch (err) {
      console.error("Failed to generate career materials", err);
      alert("Failed to generate career materials.");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`RESUME:\n${resume}\n\nINTERVIEW:\n${interview}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="career-container">
      <div className="career-header">
        <h1>AI Career Builder</h1>
        <p>Generate your resume and mock interview questions based on your academic progress.</p>
      </div>

      <div className="career-controls glass-panel">
        <button onClick={generateCareer} disabled={loading} className="generate-btn">
          {loading ? "Generating..." : "Generate My Profile"}
        </button>
        {(resume || interview) && (
          <button onClick={copyToClipboard} className="btn-secondary copy-btn">
            {copied ? "Copied!" : "📋 Copy to Clipboard"}
          </button>
        )}
      </div>

      <div className="career-results">
        {resume && (
          <div className="result-card glass-panel">
            <h2>Resume Draft (Markdown)</h2>
            <pre className="markdown-box">{resume}</pre>
          </div>
        )}
        
        {interview && (
          <div className="result-card glass-panel">
            <h2>Mock Interview Q&A</h2>
            <pre className="markdown-box">{interview}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
