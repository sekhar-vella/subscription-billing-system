import { useState } from "react";
import axios from "axios";

function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/signup",
        {
          name,
          email,
          password
        }
      );

      alert(response.data.message || "Signup successful!");
      window.location.href = "/";
    } catch (error) {
      console.log(error.response);
      alert(error.response?.data?.detail || "Signup failed");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="logo-circle">💳</div>

        <h1>Create Account</h1>
        <p className="subtitle">
          Create your Subscription Billing account
        </p>

        <form onSubmit={handleSignup}>
          <label>Name</label>
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Create a password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button className="primary-btn" type="submit">
            Create Account
          </button>
        </form>

        <p className="switch-text">
          Already have an account?{" "}
          <a href="/">Sign In</a>
        </p>
      </div>
    </div>
  );
}

export default Signup;