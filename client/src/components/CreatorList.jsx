import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const CreatorList = () => {
  const [creators, setCreators] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/v1/creators`)
      .then(response => setCreators(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container">
      <h2>Creators</h2>
      <div className="grid">
        {creators.map(creator => (
          <div key={creator.id} className="card">
            <h3>{creator.name}</h3>
            <p>{creator.bio}</p>
            <p>Skills: {creator.skills}</p>
            <Link to={`/creators/${creator.id}`} style={{ color: '#007bff' }}>View Profile</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CreatorList;