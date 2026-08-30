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

      // Get JWT token from backend
      const token = response.data.access_token;

      // Save token in browser
      localStorage.setItem("token", token);

      alert("Signin successful!");

      // Go to Home page
      window.location.href = "/home";
    } catch (error) {
      alert(
        error.response?.data?.detail || "Signin failed"
      );
    }
  };

  return (
    <div>
      <h1>Sign In</h1>

      <form onSubmit={handleSignin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br />
        <br />

        <button type="submit">Sign In</button>
      </form>

      <p>
        Don't have an account?{" "}
        <a href="/signup">Create Account</a>
      </p>
    </div>
  );
}

export default Signin;