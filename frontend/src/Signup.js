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
          name: name,
          email: email,
          password: password
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
    <div>
      <h1>Create Account</h1>

      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <br /><br />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br /><br />

        <button type="submit">Sign Up</button>
      </form>

      <p>
        Already have an account?{" "}
        <a href="/">Sign In</a>
      </p>
    </div>
  );
}

export default Signup;