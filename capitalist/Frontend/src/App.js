import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AppRoutes from './components/Routes';

function App() {
  
  return (
    <>
      <Router>
        <AppRoutes />
      </Router>
    </>
  );
}

export default App;