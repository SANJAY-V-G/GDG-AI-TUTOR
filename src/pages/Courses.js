import React from 'react';
import Navbar from './Navbar';
import Footer from '../components/Footer';
import { Link } from 'react-router-dom';
import './Courses.css';

const Courses = () => {
  return (
    <div>
      <Navbar />
      <div className="courses-container">
        <h1>Courses</h1>
        <p>Explore our available AI-powered learning courses.</p>

        <div className="course-item">
          <img src="/agri.jpeg" alt="Agriculture Icon" />
          <div className="course-text">
            <Link to="/courses/agriculture">1. Geography: Agriculture</Link>
            <p>Understand the role of agriculture in shaping human geography.</p>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Courses;
