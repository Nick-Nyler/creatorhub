import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const JobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/v1/jobs`)
      .then(response => setJobs(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container">
      <h2>Available Jobs</h2>
      <div className="grid">
        {jobs.map(job => (
          <div key={job.id} className="card">
            <h3>{job.title}</h3>
            <p>{job.description}</p>
            <p>Budget: ${job.budget}</p>
            <p>Deadline: {new Date(job.deadline).toLocaleDateString()}</p>
            <Link to={`/jobs/${job.id}`} style={{ color: '#007bff' }}>View Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobList;