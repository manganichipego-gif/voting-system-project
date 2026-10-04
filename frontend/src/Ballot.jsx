import { useState, useEffect } from 'react'
import './App.css' // We will add styling here later

function Ballot() {
  const [candidates, setCandidates] = useState([])
  const [positions, setPositions] = useState([])
  const [currentStep, setCurrentStep] = useState(0)
  const [ballotSelections, setBallotSelections] = useState({})
  const [message, setMessage] = useState('')
  const [isReviewing, setIsReviewing] = useState(false)
  const [deviceId, setDeviceId] = useState('')

  useEffect(() => {
    // Fetch candidates from Django
    fetch('https://voting-system-project-1.onrender.com/api/candidates/')
      .then(response => response.json())
      .then(data => {
        setCandidates(data)
        
        const rawPositions = [...new Set(data.map(c => c.position))];
        
        
        const officialOrder = [
          "President",
          "Vice President",
          "Secretary General",
          "Treasurer",
          "President of BIT",
          "President of AESS",
          "President of Law",
          "President of Medicine",
          "Academic Minister",
          "Minister of Finance",
          "Minister of Communication and Information",
          "Minister of Sports and Entertainment" ,
          "Minister of Security and Discipline"
        ];

        
        const sortedPositions = rawPositions.sort((a, b) => {
          const indexA = officialOrder.indexOf(a);
          const indexB = officialOrder.indexOf(b);

          
          const weightA = indexA === -1 ? 999 : indexA;
          const weightB = indexB === -1 ? 999 : indexB;

          return weightA - weightB;
        });

        
        setPositions(sortedPositions);
      })
      .catch(error => console.error('Error:', error))
  }, [])

useEffect(() => {
    let footprint = localStorage.getItem('election_device_footprint');
    if (!footprint) {
      footprint = crypto.randomUUID();
      localStorage.setItem('election_device_footprint', footprint);
    }
    setDeviceId(footprint);
  }, []);

  // Handle ticking a box
  const handleSelection = (position, candidateId) => {
    setBallotSelections({
      ...ballotSelections,
      [position]: candidateId
    })
  }

  // Submit the final ballot
  const submitBallot = () => {
    fetch('https://voting-system-project-1.onrender.com/admin/login/?next=/admin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
          votes: ballotSelections, 
          device_id: deviceId 
        })
    })
    .then(response => {
      if (response.ok) setMessage('Ballot submitted successfully!')
      else setMessage('Error casting vote. You must be logged in.')
    })
  }

 

  if (positions.length === 0) return <div className="loading">Loading ballot...</div>

  // --- THE NEW REVIEW SCREEN ---
  if (isReviewing) {
    return (
      <div className="ballot-container">
        <header className="ballot-header">
          <h1>Review Your Ballot</h1>
          {message && <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>{message}</div>}
        </header>

        <div className="review-section">
          <h2 className="position-title">CONFIRM SELECTIONS</h2>
          {positions.map(position => {
            const selectedCandidateId = ballotSelections[position];
            const selectedCandidate = candidates.find(c => c.id === selectedCandidateId);
            
            return (
              <div key={position} className="review-item">
                <h3>{position.toUpperCase()}</h3>
                <div className="review-candidate">
                  {selectedCandidate ? (
                    <>
                      {selectedCandidate.portrait && (
                        <img 
                          className="review-thumb"
                          src={selectedCandidate.portrait.includes('http') ? selectedCandidate.portrait : `http://127.0.0.1:8000${selectedCandidate.portrait.startsWith('/') ? '' : '/media/'}${selectedCandidate.portrait}`} 
                          alt="thumb" 
                        />
                      )}
                      <p>{selectedCandidate.name} <span className="review-party">({selectedCandidate.party || 'Independent'})</span></p>
                    </>
                  ) : (
                    <p className="no-selection">No candidate selected</p>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <div className="pagination-controls">
          <button className="btn btn-secondary" onClick={() => setIsReviewing(false)}>
            Back to Editing
          </button>
          <button className="btn btn-success" onClick={submitBallot}>
            Confirm & Submit
          </button>
        </div>
      </div>
    )
  }

  // --- THE MAIN BALLOT SCREEN ---
  const currentPosition = positions[currentStep]
  const candidatesForPosition = candidates.filter(c => c.position === currentPosition)

  return (
    <div className="ballot-container">
      <header className="ballot-header">
        <h1>University Election Ballot</h1>
      </header>

      <div className="position-section">
        <h2 className="position-title">{currentPosition ? currentPosition.toUpperCase() : ''}</h2>
        
       <div className="candidate-list">
          {candidatesForPosition.map(candidate => (
            <label 
              key={candidate.id} 
              className={`candidate-card ${ballotSelections[currentPosition] === candidate.id ? 'selected' : ''}`}
            >
              <input 
                type="radio" 
                name={currentPosition}
                value={candidate.id}
                checked={ballotSelections[currentPosition] === candidate.id}
                onChange={() => handleSelection(currentPosition, candidate.id)}
                className="hidden-radio"
              />
              
              <div className="image-wrapper portrait">
                {candidate.portrait ? (
                  <img 
                    src={candidate.portrait.includes('http') ? candidate.portrait : `http://127.0.0.1:8000${candidate.portrait.startsWith('/') ? '' : '/media/'}${candidate.portrait}`} 
                    alt="portrait" 
                  />
                ) : (
                  <div className="placeholder-img">No Image</div>
                )}
              </div>

              <div className="candidate-info">
                <h3>{candidate.name}</h3>
                <span className="party-badge">{candidate.party || 'Independent'}</span>
              </div>

              <div className="image-wrapper logo">
                {candidate.party_logo && (
                  <img 
                    src={candidate.party_logo.includes('http') ? candidate.party_logo : `http://127.0.0.1:8000${candidate.party_logo.startsWith('/') ? '' : '/media/'}${candidate.party_logo}`} 
                    alt="logo" 
                  />
                )}
              </div>

              {/* NEW TICK BOX */}
              <div className="tick-box">
                {ballotSelections[currentPosition] === candidate.id ? '✅' : ''}
              </div>
            </label>
          ))}
        </div>

      </div>
      <div className="pagination-controls">
        <button 
          className="btn btn-secondary"
          disabled={currentStep === 0} 
          onClick={() => setCurrentStep(currentStep - 1)}
        >
          Previous
        </button>

        {currentStep < positions.length - 1 ? (
          <button 
            className="btn btn-primary"
            onClick={() => setCurrentStep(currentStep + 1)}
          >
            Next
          </button>
        ) : (
          <button 
            className="btn btn-primary"
            onClick={() => setIsReviewing(true)}
          >
            Review Ballot
          </button>
        )}
      </div>
    </div>
  )
}

export default Ballot