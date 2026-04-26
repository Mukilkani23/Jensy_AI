import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('genz_token'));
  const [studentId, setStudentId] = useState(localStorage.getItem('genz_student_id'));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);

  useEffect(() => {
    setIsAuthenticated(!!token);
  }, [token]);

  const login = (newToken, newStudentId) => {
    localStorage.setItem('genz_token', newToken);
    localStorage.setItem('genz_student_id', newStudentId);
    setToken(newToken);
    setStudentId(newStudentId);
  };

  const logout = () => {
    localStorage.removeItem('genz_token');
    localStorage.removeItem('genz_student_id');
    setToken(null);
    setStudentId(null);
  };

  return (
    <AuthContext.Provider value={{ token, studentId, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
