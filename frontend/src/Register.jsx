import { useState } from 'react';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await fetch('https://Chipego.pythonanywhere.com/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setMessage('success: ' + data.success);
        setUsername('');
        setEmail('');
      } else {
        setMessage('error: ' + (data.error || 'Registration failed.'));
      }
    } catch (error) {
      console.error('Fetch Error:', error);
      setMessage('error: Could not connect to the server.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ballot-container" style={{ maxWidth: '500px', width: '100%' }}>
      <header className="ballot-header">
        <h1>Voter Registration</h1>
      </header>

      <form onSubmit={handleSubmit} style={{ padding: '40px' }}>
        {message && (
          <div className={`message ${message.startsWith('success') ? 'success' : 'error'}`} style={{ marginBottom: '20px' }}>
            {message.replace('success: ', '').replace('error: ', '')}
          </div>
        )}

        <div style={{ marginBottom: '20px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', color: '#a1c4fd' }}>Student Username</label>
          <input
            type="text"
            required
            value={username}
            onChange={(e) => {
              const lettersAndSpaces = e.target.value.replace(/[^a-zA-Z ]/g, '');
              setUsername(lettersAndSpaces);
             }}
            style={{ 
              width: '100%', padding: '15px', borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.2)', 
              background: 'rgba(0, 0, 0, 0.2)', color: 'white', 
              fontSize: '16px', boxSizing: 'border-box'
            }}
            placeholder="e.g. jdoe2026"
          />
        </div>

        <div style={{ marginBottom: '30px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: '600', color: '#a1c4fd' }}>University Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ 
              width: '100%', padding: '15px', borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.2)', 
              background: 'rgba(0, 0, 0, 0.2)', color: 'white', 
              fontSize: '16px', boxSizing: 'border-box'
            }}
            placeholder="student@university.edu.zm"
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={isLoading}
          style={{ width: '100%', padding: '15px' }}
        >
          {isLoading ? 'Sending Request...' : 'Request Access'}
        </button>
      </form>
    </div>
  );
}