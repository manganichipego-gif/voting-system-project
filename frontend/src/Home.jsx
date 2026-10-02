import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h1 style={styles.heading}>Welcome to the University Voting Portal</h1>
                <p style={styles.text}>
                    Thank you for successfully logging in. Your voice matters in shaping the future of our university.
                </p>
                
                <div style={styles.infoBox}>
                    <h3 style={styles.subHeading}>Before you vote:</h3>
                    <ul style={styles.list}>
                        <li>Review the candidate manifestos carefully.</li>
                        <li>You can only cast your ballot once.</li>
                        <li>Ensure your network connection is stable before submitting.</li>
                    </ul>
                </div>

                <button 
                    onClick={() => navigate('/ballot')} 
                    style={styles.button}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#004494'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#0056b3'}
                >
                    Proceed to Ballot
                </button>
            </div>
        </div>
    );
}

// Basic inline styling for a clean, academic look
const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#1a1a2e', // A dark background to match your Vercel theme
        padding: '20px',
        fontFamily: 'Arial, sans-serif'
    },
    card: {
        backgroundColor: '#ffffff',
        padding: '40px',
        borderRadius: '10px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
        maxWidth: '600px',
        width: '100%',
        textAlign: 'center'
    },
    heading: {
        color: '#2c3e50',
        marginBottom: '15px'
    },
    text: {
        color: '#555',
        lineHeight: '1.6',
        marginBottom: '20px'
    },
    infoBox: {
        backgroundColor: '#eef2f5',
        padding: '20px',
        borderRadius: '8px',
        textAlign: 'left',
        marginBottom: '30px'
    },
    subHeading: {
        color: '#333',
        marginTop: '0',
        marginBottom: '10px'
    },
    list: {
        color: '#555',
        margin: '0',
        paddingLeft: '20px',
        lineHeight: '1.6'
    },
    button: {
        backgroundColor: '#0056b3', // A strong blue for the primary action
        color: 'white',
        border: 'none',
        padding: '14px 30px',
        fontSize: '16px',
        fontWeight: 'bold',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
        width: '100%'
    }
};

export default Home;