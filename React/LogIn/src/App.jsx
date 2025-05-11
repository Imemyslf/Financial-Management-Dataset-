import { useState } from "react";
import axios from "axios";
import { auth, provider, signInWithPopup } from "./firebase";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [message, setMessage] = useState("");
  const [displayName, setDisplayName] = useState("");

  const toggleForm = () => {
    setIsLogin((prev) => !prev);
    setMessage("");
  };

  const handleSubmit = async () => {
    const endpoint = isLogin ? "/api/auth/login" : "/api/auth/signup";

    try {
      const res = await axios.post(`http://localhost:5000${endpoint}`, {
        username,
        password,
      });

      setMessage(res.data.message);

      if (
        res.data.message === "Login successful" ||
        res.data.message === "User registered successfully"
      ) {
        // Successful login/signup, now redirect to Streamlit dashboard
        window.location.href = "http://localhost:8501"; // Redirect to the Streamlit app
      }
    } catch (err) {
      setMessage(err.response?.data?.error || "Something went wrong");
    }

    setUsername("");
    setPassword("");
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const token = await result.user.getIdToken();
      const displayName = result.user.displayName;

      const res = await axios.post("http://localhost:5000/api/auth/google", {
        idToken: token,
        displayName, // 👈 sending display name to backend
      });

      setDisplayName(res.data.name || displayName);
      setMessage(`Welcome, ${res.data.name || displayName}!`);
      localStorage.setItem("userName", res.data.name || displayName); // optional storage
    } catch (err) {
      console.error(err);
      setMessage("Google login failed");
    }
  };

  const SocialLogos = () => (
    <div className="otherMethods">
      <img
        className="google"
        src="https://developers.google.com/identity/images/g-logo.png"
        alt="Google"
        width="40"
        height="40"
        onClick={handleGoogleLogin}
      />
    </div>
  );

  return (
    <div className="main-container">
      {isLogin ? (
        <div className="login-container">
          <div className="login-semiContainer">
            <h2>Login</h2>
            <div className="login">
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleSubmit}>Login</button>
              <p onClick={toggleForm}>Don't have an account? Sign up</p>
              {message && <p className="response-message">{message}</p>}
              {displayName && (
                <p className="welcome-message">Welcome, {displayName}</p>
              )}
              <SocialLogos />
            </div>
          </div>
        </div>
      ) : (
        <div className="signin-container">
          <div className="signin-semiContainer">
            <h2>Sign Up</h2>
            <div className="signin">
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleSubmit}>Sign Up</button>
              <p onClick={toggleForm}>Already have an account? Login</p>
              {message && <p className="response-message">{message}</p>}
              {displayName && (
                <p className="welcome-message">Welcome, {displayName}</p>
              )}
              <SocialLogos />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
