import { useState } from "react";
import axios from "axios";

function Signin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/signin",
        {
          email,
          password
        }
      );

      const token = response.data.access_token;
      localStorage.setItem("token", token);

      alert("Signin successful!");
      window.location.href = "/home";
    } catch (error) {
      alert(error.response?.data?.detail || "Signin failed");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="logo-circle">💳</div>

        <h1>Welcome Back</h1>
        <p className="subtitle">Sign in to your Subscription Billing account</p>

        <form onSubmit={handleSignin}>
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
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button className="primary-btn" type="submit">
            Sign In
          </button>
        </form>

        <p className="switch-text">
          Don't have an account?{" "}
          <a href="/signup">Create Account</a>
        </p>
      </div>
    </div>
  );
}

export default Signin;