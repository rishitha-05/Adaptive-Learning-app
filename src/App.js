import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage/HomePage';
import Login from './components/LoginPage/LoginPage';
import QuizPage from './components/QuizPage/QuizPage'; // Import QuizPage component

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
        <Route path="/quiz" element={<QuizPage />} /> {/* Add this line for QuizPage */}
        <Route path="/" element={isLoggedIn ? <HomePage /> : <Login onLogin={() => setIsLoggedIn(true)} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
