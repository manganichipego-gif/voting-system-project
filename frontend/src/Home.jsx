import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css'; // Make sure your CSS is imported

const Home = () => {
  const navigate = useNavigate();
  
  // State variables for dynamic data from Django
  const [candidates, setCandidates] = useState([]);
  const [showCandidates, setShowCandidates] = useState(false);
  const [isVotingOpen, setIsVotingOpen] = useState(false);
  const [resultsReleased, setResultsReleased] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [scheduleText, setScheduleText] = useState({ start: "Loading...", end: "Loading..." });

  useEffect(() => {
    
    const fetchSettings = async () => {
      try {
        const res = await fetch("https://Chipego.pythonanywhere.com/api/status/"); 
        
        if (res.ok) {
          const data = await res.json();
          
          
          setIsVotingOpen(data.is_open);
          setResultsReleased(data.results_released);
          
          
          if (data.start_time && data.end_time) {
            const startTime = new Date(data.start_time);
            const endTime = new Date(data.end_time);
            
            setScheduleText({
              start: startTime.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }),
              end: endTime.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })
            });
          } else {
            setScheduleText({ start: "TBA", end: "TBA" });
          }
        }
      } catch (error) {
        console.error("Error fetching election status:", error);
        setScheduleText({ start: "Error", end: "Error" });
      }
    };

    //  FETCH REAL CANDIDATES FROM DJANGO
    const fetchCandidates = async () => {
      try {
        const response = await fetch("https://Chipego.pythonanywhere.com/api/candidates/");
        if (response.ok) {
          const data = await response.json();
          setCandidates(data);
        }
      } catch (error) {
        console.error("Error fetching candidates:", error);
      } finally {
        setIsLoading(false);
      }
    };

    
    fetchSettings();
    fetchCandidates();
  }, []);

  
  const getImageUrl = (imagePath) => {
    if (!imagePath) return "https://via.placeholder.com/100x100?text=No+Photo";
    if (imagePath.startsWith("http")) return imagePath;
    const baseUrl = "https://Chipego.pythonanywhere.com";
    return `${baseUrl}${imagePath.startsWith("/") ? "" : "/"}${imagePath}`;
  };

  const handleVoteClick = () => {
    if (isVotingOpen) {
      navigate('/ballot');
    }
  };

  return (
    <div className="home-dashboard-container">
      
      <header className="dashboard-header">
        <h2>CAVENDISH ELECTION DASHBOARD</h2>
        <p>Welcome! Review the candidates and cast your official vote.</p>
        
        {/* Shows a warning banner if voting is closed */}
        {!isVotingOpen && (
          <div className="time-warning-banner">
            Voting is currently closed. Please check the schedule below.
          </div>
        )}
      </header>

      
      <div className="dashboard-action-panel">
        
        {/* Vote Button (Disabled if time is closed) */}
        <button 
          className={`action-btn vote-btn ${!isVotingOpen ? 'locked-btn' : ''}`} 
          onClick={handleVoteClick}
          disabled={!isVotingOpen}
        >
          <div className="btn-icon">🗳️</div>
          <h3>Cast Your Vote</h3>
          <p>{isVotingOpen ? "Enter the E-Ballot" : "Currently Locked"}</p>
        </button>

        {/*  View Candidates Button */}
        <button 
          className="action-btn candidates-btn" 
          onClick={() => setShowCandidates(!showCandidates)}
        >
          <div className="btn-icon">👥</div>
          <h3>{showCandidates ? "Hide Candidates" : "View Candidates"}</h3>
          <p>See who is running</p>
        </button>
    
        <button 
          className={`action-btn results-btn ${!resultsReleased ? 'locked-btn' : ''}`} 
          onClick={() => {
            if (resultsReleased) alert("Redirecting to results...");
            
          }}
          disabled={!resultsReleased}
        >
          <div className="btn-icon">📊</div>
          <h3>View Results</h3>
          <p>{resultsReleased ? "Live election data" : "Pending Publication"}</p>
        </button>

      </div>

      
      {showCandidates && (
        <section className="dashboard-candidates-section">
          <h3 className="section-title">Official Registered Candidates</h3>
          
          {isLoading ? (
            <p style={{textAlign: "center"}}>Loading candidates from database...</p>
          ) : candidates.length === 0 ? (
            <p style={{textAlign: "center"}}>No candidates registered yet.</p>
          ) : (
            <div className="candidates-grid">
              {candidates.map((cand) => (
                <div key={cand.id} className="candidate-mini-card">
                  <img src={getImageUrl(cand.portrait)} alt={cand.name} className="mini-photo" />
                  <h4>{cand.name}</h4>
                  <p>{cand.party || "Independent"}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <footer className="voting-time-banner">
        <div className="time-block">
          <span className="time-label">VOTING OPENS</span>
          <span className="time-value">{scheduleText.start}</span>
        </div>
        <div className="time-divider"></div>
        <div className="time-block">
          <span className="time-label">VOTING CLOSES</span>
          <span className="time-value">{scheduleText.end}</span>
        </div>
      </footer>

    </div>
  );
};

export default Home;