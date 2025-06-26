import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Dashboard = ({ user }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (user) {
      axios.get(`${process.env.REACT_APP_API_URL}/api/v1/applications`)
        .then(response => setData(response.data))
        .catch(error => console.error(error));
    }
  }, [user]);

  if (!user) return <div>Please log in</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>Dashboard</h2>
        {user.role === 'client' ? (
          <>
            <Link to="/jobs" className="btn btn-primary" style={{ display: 'inline-block', marginBottom: '20px' }}>
              Post a Job
            </Link>
            <h3>Your Posted Jobs</h3>
            <div className="grid">
              {data.map(app => (
                <div key={app.id} className="card">
                  <p>Job ID: {app.job_id}</p>
                  <p>Price Offer: ${app.price_offer}</p>
                  <p>Cover Letter: {app.cover_letter}</p>
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            <Link to="/portfolio/upload" className="btn btn-primary" style={{ display: 'inline-block', marginBottom: '20px' }}>
              Upload Portfolio Item
            </Link>
            <h3>Your Applications</h3>
            <div className="grid">
              {data.map(app => (
                <div key={app.id} className="card">
                  <p>Job ID: {app.job_id}</p>
                  <p>Price Offer: ${app.price_offer}</p>
                  <p>Cover Letter: {app.cover_letter}</p>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;