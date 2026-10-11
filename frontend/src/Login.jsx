import React, { useState } from 'react';

const Login = () => {
  const [studentId, setStudentId] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setIsLoading(true);

    try {
      const response = await fetch("https://Chipego.pythonanywhere.com/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          // We send the Student ID, but label it 'username' for Django
          username: studentId, 
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        // Displays error if they type the wrong ID or password
        setErrorMessage(data.error || "Invalid Student ID or Password.");
      } else {
        setErrorMessage("");
        alert("Login successful! Welcome to the Voting System.");
        
        // FUTURE STEP: 
        // This is where you will redirect the student to the actual voting page 
        // after they successfully log in (e.g., using window.location.href or React Router)
      }
    } catch (error) {
      setErrorMessage("Network error. Please check your connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="registration-container">
      <h2>VOTER LOGIN</h2>
      
      <form onSubmit={handleSubmit}>
        {errorMessage && (
          <div style={{ color: "#ff4d4d", marginBottom: "15px", fontWeight: "bold" }}>
            {errorMessage}
          </div>
        )}

        <div className="input-group">
          <label>Student ID</label>
          <input 
            type="text" 
            value={studentId} 
            onChange={(e) => setStudentId(e.target.value)} 
            placeholder="e.g. 12345"
            required 
          />
        </div>

        <div className="input-group">
          <label>Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            placeholder="Enter your password"
            required 
          />
        </div>

        <button type="submit" disabled={isLoading} style={{ marginTop: "20px", width: "100%" }}>
          {isLoading ? "VERIFYING..." : "SECURE LOGIN"}
        </button>
      </form>
    </div>
  );
};

export default Login;