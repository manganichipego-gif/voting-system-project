import React, { useState } from 'react';

const Register = () => {
  const [firstName, setFirstName] = useState('');
  const [middleName, setMiddleName] = useState('');
  const [lastName, setLastName] = useState('');
  const [studentId, setStudentId] = useState('');
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  
  
  const firstInitial = firstName ? firstName.charAt(0).toLowerCase() : '';
  const middleInitial = middleName ? middleName.charAt(0).toLowerCase() : '';
  const lastInitial = lastName ? lastName.charAt(0).toLowerCase() : '';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch('https://Chipego.pythonanywhere.com/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          student_id: studentId,
          email: email,
        }),
      });

      const data = await response.json();
      if (response.ok){
        setIsSubmitted(true);
      }
      else{
        setErrorMessage('error: ' + (data.error || 'Registration failed.'));
      }
      
    } catch (error) {
      console.error('Fetch Error:', error);
      setErrorMessage('error: Could not connect to the server.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted){
    return(
      <div style={{ textAlign: 'center', padding:'50px', marginTop:'50px'}}>
        <h2 style={{ color: "#28a745"}}> Request Successful!</h2>
        <p style={{ fontSize: '18px', marginTop: '10px'}}>
          Please wait for approval. You will receive an Email once your account has been Approved.
          </p>
          </div>
    );
  }

  return (
    <div className="registration-container">
      <h2>VOTER REGISTRATION</h2>
      
      <form onSubmit={handleSubmit}>
        {errorMessage && (
          <div style={{ color: "#ff4d4d", marginBottom: "15px", fontWeight: "bold" }}>
            {errorMessage}
          </div>
        )}

        <div className="input-group">
          <label>First Name</label>
          <input 
            type="text" 
            value={firstName} 
            onChange={(e) => setFirstName(e.target.value)} 
            required 
          />
        </div>

        <div className="input-group">
          <label>Middle Name (Optional)</label>
          <input 
            type="text" 
            value={middleName} 
            onChange={(e) => setMiddleName(e.target.value)} 
            placeholder='Enter middle name'
          />
        </div>

        <div className="input-group">
          <label>Last Name</label>
          <input 
            type="text" 
            value={lastName} 
            onChange={(e) => setLastName(e.target.value)} 
            required 
          />
        </div>

        <div className="input-group">
          <label>Student ID</label>
          <input 
            type="text" 
            value={studentId} 
            onChange={(e) => setStudentId(e.target.value)} 
            required 
          />
        </div>

        <div className="input-group">
          <label>Personal Email</label>
          <input 
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ 
              backgroundColor: "rgba(255, 255, 255, 0.1)",  
              cursor: "not-allowed",
              color: "#aaa"
            }} 
          />
        </div>

        <button type="submit" disabled={isLoading} style={{ marginTop: "20px", width: "100%" }}>
          {isLoading ? "PROCESSING..." : "REQUEST ACCESS"}
        </button>
      </form>
    </div>
  );
};

export default Register;