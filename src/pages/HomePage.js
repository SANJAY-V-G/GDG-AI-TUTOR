// src/pages/HomePage.js
import React from "react";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "../components/Footer";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="homepage-wrapper">
      <Navbar />
      <div className="home-container">
        <h1>Welcome to Edumateo AI</h1>
        <p>Your personal AI-powered learning assistant</p>

        <div className="button-row">
          <Link to="/courses" className="home-button">Explore Courses</Link>
          <Link to="/dashboard" className="home-button">Get Started</Link>
        </div>

        <div className="bot-image-row">
          <img src="/doca1.jpg" alt="AI Bot 1" />
          <img src="/doca2.jpg" alt="AI Bot 2" />
          <img src="/doca1.jpg" alt="AI Bot 3" />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default HomePage;
