import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 

export default function SetupPassword() {
  const [username, setUsername] = useState('');
  const [code, setCode] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate(); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await fetch('https://voting-system-project-1.onrender.com/api/setup-password/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, code, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
      
        navigate('/home'); 
      } else {
        setMessage('error: ' + (data.error || 'Failed to set password.'));
      }
    } catch (error) {
      setMessage('error: Could not connect to the server.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ballot-container" style={{ maxWidth: '500px', width: '100%' }}>
      <header className="ballot-header">
        <h1>Account Setup</h1>
      </header>

      <form onSubmit={handleSubmit} style={{ padding: '40px' }}>
        {message && (
          <div className={`message ${message.startsWith('success') ? 'success' : 'error'}`} style={{ marginBottom: '20px' }}>
            {message.replace('success: ', '').replace('error: ', '')}
          </div>
        )}

        <div style={{ marginBottom: '20px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', color: '#a1c4fd' }}>Username</label>
          <input
            type="text"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ 
              width: '100%', padding: '15px', borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.2)', 
              background: 'rgba(0, 0, 0, 0.2)', color: 'white', fontSize: '16px', boxSizing: 'border-box'
            }}
          />
        </div>

        <div style={{ marginBottom: '20px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', color: '#a1c4fd' }}>5-Digit Approval Code</label>
          <input
            type="text"
            required
            maxLength="5"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            style={{ 
              width: '100%', padding: '15px', borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.2)', 
              background: 'rgba(0, 0, 0, 0.2)', color: 'white', fontSize: '16px', boxSizing: 'border-box', letterSpacing: '2px'
            }}
          />
        </div>

        <div style={{ marginBottom: '30px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', color: '#a1c4fd' }}>New Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ 
              width: '100%', padding: '15px', borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.2)', 
              background: 'rgba(0, 0, 0, 0.2)', color: 'white', fontSize: '16px', boxSizing: 'border-box'
            }}
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={isLoading} style={{ width: '100%', padding: '15px' }}>
          {isLoading ? 'Verifying...' : 'Set Password'}
        </button>
      </form>
    </div>
  );
}