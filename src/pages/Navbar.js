import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar">
      <div className="logo-container">
        <img src="https://assets.onecompiler.app/42yahxteg/43cuw4s2n/1000038911.png" alt="Logo" />
        <div className="title">Edumateo AI</div>
      </div>
      <div className="nav-links">
        <NavLink to="/" className="nav-link">Home</NavLink>
        <NavLink to="/about" className="nav-link">About</NavLink>
        <NavLink to="/courses" className="nav-link">Courses</NavLink>
        <NavLink to="/dashboard" className="nav-link">Dashboard</NavLink>
        <NavLink to="/contact" className="nav-link">Contact</NavLink>
      </div>
    </div>
  );
};

export default Navbar;
