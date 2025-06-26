import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import JobList from './components/JobList';
import JobDetail from './components/JobDetail';
import CreatorList from './components/CreatorList';
import CreatorProfile from './components/CreatorProfile';
import Dashboard from './components/Dashboard';
import PortfolioUploader from './components/PortfolioUploader';
import axios from 'axios';

const App = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  return (
    <Router>
      <div style={{ minHeight: '100vh' }}>
        <Navbar user={user} setUser={setUser} />
        <Routes>
          <Route path="/login" element={<LoginForm setUser={setUser} />} />
          <Route path="/signup" element={<SignupForm setUser={setUser} />} />
          <Route path="/jobs" element={<JobList />} />
          <Route path="/jobs/:id" element={<JobDetail user={user} />} />
          <Route path="/creators" element={<CreatorList />} />
          <Route path="/creators/:id" element={<CreatorProfile />} />
          <Route path="/dashboard" element={<Dashboard user={user} />} />
          <Route path="/portfolio/upload" element={<PortfolioUploader user={user} />} />
          <Route path="/" element={<Navigate to="/jobs" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;