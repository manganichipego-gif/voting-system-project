import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Ballot from './Ballot';
import Register from './Register';
import SetupPassword from './SetupPassword'; // <-- New Import
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        {/* The new Setup Password Route */}
        <Route path="/setup-password" element={<SetupPassword />} /> 
        <Route path="/ballot" element={<Ballot />} />
        <Route path="/" element={<Navigate to="/register" />} />
      </Routes>
    </Router>
  );
}

export default App;