import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './Home';
import Ballot from './Ballot';
import Register from './Register';
import SetupPassword from './SetupPassword';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        {/* The new Setup Password Route */}
        <Route path="/setup-password" element={<SetupPassword />} /> 
        <Route path="/ballot" element={<Ballot />} />
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Navigate to="/register" />} />
      </Routes>
    </Router>
  );
}

export default App;