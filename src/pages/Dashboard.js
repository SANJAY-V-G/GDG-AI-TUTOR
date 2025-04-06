import React from 'react';
import Navbar from './Navbar';
import Footer from '../components/Footer';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-wrapper">
      <Navbar />
      <div className="dashboard">
        {/* Profile Section */}
        <div className="card profile-card">
          <img src="/po.png" alt="User Avatar" className="avatar-large" />
          <div>
            <h2>Hello, SK 👋</h2>
            <p>Keep pushing your limits. You're doing amazing!</p>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="stats-section">
          <div className="card stat-card">
            <h3>Enrolled Courses</h3>
            <span className="stat-number">5</span>
          </div>
          <div className="card stat-card">
            <h3>Completed</h3>
            <span className="stat-number">3</span>
          </div>
          <div className="card stat-card">
            <h3>Streak</h3>
            <span className="stat-number">12 Days</span>
          </div>
        </div>

        {/* Learning Tracker */}
        <div className="card learning-tracker">
          <h3>Progress Overview</h3>
          <div className="progress-bar">
            <div className="progress" style={{ width: '75%' }}>75% Complete</div>
          </div>
          <p>You’re just 1 course away from monthly goals 💪</p>
        </div>

        {/* Course Cards */}
        <h2 className="section-title">My Courses</h2>
        <div className="courses-grid">
          <div className="card course-card">
            <h4>React Mastery</h4>
            <p>75% complete</p>
            <button className="btn-primary">Continue</button>
          </div>
          <div className="card course-card">
            <h4>Node.js Essentials</h4>
            <p>40% complete</p>
            <button className="btn-primary">Continue</button>
          </div>
          <div className="card course-card">
            <h4>UI/UX Design Basics</h4>
            <p>Completed ✅</p>
            <button className="btn-secondary">Review</button>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Dashboard;
