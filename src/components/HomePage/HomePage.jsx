import React from "react";
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import "./HomePage.css";

const Homepage = () => {
  const navigate = useNavigate(); // Initialize useNavigate
  
  const handleExploreClick = () => {
    navigate('/quiz'); // Navigate to QuizPage
  };

  return (
    <div className="HomePage container">
      <div className="home-text">
        <h1>Unlock Your Learning Potential</h1>
        <p>
          Dive into a dynamic learning experience where expert guidance merges
          with personalized inspiration. Engage with knowledgeable mentors
          committed to fostering your academic growth and realizing your
          educational goals. Begin a tailored learning journey designed
          specifically for your interests and ambitions.
        </p>
        <button className="btn" onClick={handleExploreClick}> Explore more</button> {/* Add onClick handler */}
      </div>
    </div>
  );
};

export default Homepage;
