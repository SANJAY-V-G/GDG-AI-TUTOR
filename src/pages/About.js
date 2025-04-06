import React from 'react';
import './About.css';
import Navbar from './Navbar';

const About = () => {
  return (
    <>
      <Navbar />
      <div className="about-container">
        <h1>About Edumateo AI</h1>
        <p className="about-description">
          Edumateo AI is your intelligent companion in the journey of learning.
          We combine cutting-edge AI with expert guidance to create a truly personalized educational experience for every learner.
        </p>

        <h2 className="section-heading">Our Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>AI-Powered Learning</h3>
            <p>Adaptive AI systems to fit your unique learning style and pace.</p>
          </div>
          <div className="feature-card">
            <h3>Interactive Content</h3>
            <p>Engaging, hands-on materials designed to boost retention.</p>
          </div>
          <div className="feature-card">
            <h3>Expert Tutors</h3>
            <p>Access to a team of subject matter experts for guidance.</p>
          </div>
          <div className="feature-card">
            <h3>Progress Tracking</h3>
            <p>Monitor your learning journey with detailed analytics.</p>
          </div>
        </div>

        <h2 className="section-heading">Meet the Team</h2>
        <div className="team-grid">
          <div className="team-member">
            <img src="/sk3.jpg" alt="Sivakarthikeyan M" />
            <h4>Sivakarthikeyan M</h4>
            <p>Founder & CEO</p>
          </div>
          <div className="team-member">
            <img src="/tej.jpg" alt="Tejas Chalam" />
            <h4>Tejas Chalam</h4>
            <p>Lead Developer</p>
          </div>
          <div className="team-member">
            <img src="/vg.jpg" alt="Sanjay VG" />
            <h4>Sanjay VG</h4>
            <p>AI Specialist</p>
          </div>
          <div className="team-member">
            <img src="/vi.jpg" alt="Vikas AK" />
            <h4>Vikas AK</h4>
            <p>UI/UX Designer</p>
          </div>
        </div>

        <div className="call-to-action">
          <h2>Want to join us?</h2>
          <p>We’re always looking for passionate minds to help shape the future of learning.</p>
          <a href="/contact" className="cta-button">Contact Here!</a>
        </div>

        <h2 className="section-heading">Our Vision</h2>
        <p className="vision-text">
          To revolutionize education by making it universally accessible, intelligent, and empowering.
          We believe every learner deserves a chance to thrive, and technology is our tool to achieve it.
        </p>
      </div>
    </>
  );
};

export default About;
