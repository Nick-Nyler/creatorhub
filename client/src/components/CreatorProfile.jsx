import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const CreatorProfile = () => {
  const { id } = useParams();
  const [creator, setCreator] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/v1/creators/${id}`)
      .then(response => setCreator(response.data))
      .catch(error => console.error(error));
  }, [id]);

  if (!creator) return <div>Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{creator.name}</h2>
        <p>{creator.bio}</p>
        <p>Skills: {creator.skills}</p>
        {creator.profile_img && <img src={creator.profile_img} alt="Profile" className="profile-img" />}
        <h3>Portfolio</h3>
        <div className="grid">
          {creator.portfolio_items.map(item => (
            <div key={item.id} className="card">
              <h4>{item.title}</h4>
              <p>{item.description}</p>
              {item.image_url && <img src={item.image_url} alt={item.title} className="portfolio-img" />}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CreatorProfile;