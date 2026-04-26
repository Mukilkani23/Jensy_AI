import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import AIChat from './pages/AIChat';
import Resources from './pages/Resources';
import Profile from './pages/Profile';
import Planner from './pages/Planner';
import Career from './pages/Career';
import Analytics from './pages/Analytics';
import './index.css';




function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/onboarding" element={
          <ProtectedRoute><Onboarding /></ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />
        <Route path="/chat" element={
          <ProtectedRoute><AIChat /></ProtectedRoute>
        } />
        <Route path="/resources" element={
          <ProtectedRoute><Resources /></ProtectedRoute>
        } />
        <Route path="/planner" element={
          <ProtectedRoute><Planner /></ProtectedRoute>
        } />
        <Route path="/career" element={
          <ProtectedRoute><Career /></ProtectedRoute>
        } />
        <Route path="/analytics" element={
          <ProtectedRoute><Analytics /></ProtectedRoute>
        } />
        <Route path="/profile" element={



          <ProtectedRoute><Profile /></ProtectedRoute>
        } />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}
