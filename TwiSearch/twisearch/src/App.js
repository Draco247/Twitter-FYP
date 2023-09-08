import React from 'react';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';
import SearchPage from './components/searchpage/search';
import ResultsPage from './components/results/results';

function App() {
  return (
  <Router>
    <Routes>
      <Route path="/" element={<SearchPage/>} />
      <Route path="/results" element={<ResultsPage/>} />
    </Routes>
  </Router>
  );
}

export default App;
