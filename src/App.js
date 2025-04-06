import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import About from './pages/About';
import Courses from './pages/Courses';
import ContactPage from './pages/ContactPage';
import Dashboard from './pages/Dashboard';
import CoursePage1 from './pages/CoursePage1';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/about" element={<About />} />
      <Route path="/courses" element={<Courses />} />
      <Route path="/courses/agriculture" element={<CoursePage1 />} />
      <Route path="/contact" element={<ContactPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;
