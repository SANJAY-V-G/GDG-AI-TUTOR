import React from 'react';
import Navbar from './Navbar';
import Footer from '../components/Footer';
import './ContactPage.css';

const ContactPage = () => {
  return (
    <div>
      <Navbar />
      <div className="contact-wrapper">
        <div className="contact-header">
          <p>FOR EDUMATEO AI INQUIRIES</p>
          <h1>Contact Us</h1>
          <p className="sub-text">We'd love to hear from you. Reach out with questions, ideas, or feedback.</p>
        </div>

        <div className="contact-content">
          <div className="info-card">
            <div className="info-block">
              <i className="fas fa-clock"></i>
              <h3>Hours</h3>
              <p>Mon–Fri, 9:00AM–5:00PM IST</p>
            </div>
            <div className="info-block">
              <i className="fas fa-phone"></i>
              <h3>Phone</h3>
              <p>+91 9876543210</p>
            </div>
            <div className="info-block">
              <i className="fas fa-envelope"></i>
              <h3>Email</h3>
              <p>info@edumateoai.com</p>
            </div>
          </div>

          <form className="contact-form">
            <h2>Send Us a Message</h2>
            <input type="text" name="name" placeholder="Your Name" required />
            <input type="email" name="email" placeholder="Your Email" required />
            <input type="text" name="subject" placeholder="Subject" required />
            <textarea name="message" rows="5" placeholder="Your Message" required></textarea>
            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ContactPage;
