import { Link } from 'react-router-dom';
import './Landing.css';

export default function Landing() {
  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <div className="hero-bg-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
        </div>
        <div className="hero-content animate-fadeInUp">
          <div className="hero-badge">⚡ AI-Powered Academic Companion</div>
          <h1 className="hero-title">
            Your Degree,<br />
            <span className="gradient-text">Supercharged.</span>
          </h1>
          <p className="hero-subtitle">
            GENZ maps your entire bachelor's journey — every semester, subject, resource, 
            and deadline — with an AI assistant that knows your curriculum inside out.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="btn-primary">Start Your Journey</Link>
            <Link to="/login" className="btn-secondary">I Already Have an Account</Link>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">8</span>
              <span className="stat-label">Semester Roadmap</span>
            </div>
            <div className="stat">
              <span className="stat-number">AI</span>
              <span className="stat-label">Smart Assistant</span>
            </div>
            <div className="stat">
              <span className="stat-number">∞</span>
              <span className="stat-label">Resources</span>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <h2 className="section-heading">How GENZ Works</h2>
        <div className="steps-grid stagger">
          <div className="step-card glass-card">
            <div className="step-number">01</div>
            <div className="step-icon">🎓</div>
            <h3>Choose Your Degree</h3>
            <p>Select your degree, branch, and college. We auto-load your curriculum.</p>
          </div>
          <div className="step-card glass-card">
            <div className="step-number">02</div>
            <div className="step-icon">📚</div>
            <h3>Get Your Roadmap</h3>
            <p>See all 8 semesters with subjects, labs, credits, and resources.</p>
          </div>
          <div className="step-card glass-card">
            <div className="step-number">03</div>
            <div className="step-icon">🤖</div>
            <h3>AI Guides You</h3>
            <p>Ask anything — study plans, subject doubts, resource suggestions — your AI knows you.</p>
          </div>
          <div className="step-card glass-card">
            <div className="step-number">04</div>
            <div className="step-icon">📈</div>
            <h3>Track Progress</h3>
            <p>Monitor completion, identify weak areas, and get personalized recommendations.</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <h2 className="section-heading">Built for the Gen Z Student</h2>
        <div className="features-grid stagger">
          <div className="feature-card glass-card">
            <span className="feature-emoji">🧠</span>
            <h3>Smart AI Chat</h3>
            <p>GPT-4o powered assistant that adapts to your learning style — coding or non-coding.</p>
          </div>
          <div className="feature-card glass-card">
            <span className="feature-emoji">🏫</span>
            <h3>College Sync</h3>
            <p>Autonomous? We scrape your college syllabus. Affiliated? We load your regulation.</p>
          </div>
          <div className="feature-card glass-card">
            <span className="feature-emoji">📊</span>
            <h3>Behavior Analysis</h3>
            <p>Weekly reports on your study patterns with actionable improvement tips.</p>
          </div>
          <div className="feature-card glass-card">
            <span className="feature-emoji">📁</span>
            <h3>Resource Library</h3>
            <p>Notes, videos, PYQs — organized per subject. Upload yours, access everyone's.</p>
          </div>
          <div className="feature-card glass-card">
            <span className="feature-emoji">✅</span>
            <h3>To-Do Lists</h3>
            <p>Semester-wise checklists to keep track of assignments, labs, and deadlines.</p>
          </div>
          <div className="feature-card glass-card">
            <span className="feature-emoji">🛤️</span>
            <h3>DSA Roadmap</h3>
            <p>Coding track students get a personalized DSA roadmap + project ideas each semester.</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <div className="cta-card glass-card">
          <h2>Ready to ace your degree?</h2>
          <p>Join thousands of bachelor's students already using GENZ to stay ahead.</p>
          <Link to="/register" className="btn-primary">Create Free Account</Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>© 2026 GENZ — Built with ⚡ for the next generation of learners.</p>
      </footer>
    </div>
  );
}
