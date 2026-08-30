import { useEffect, useState } from "react";
import axios from "axios";

function Home() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/";
      return;
    }

    axios
      .get("http://localhost:8000/home", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((response) => {
        setUser(response.data);
      })
      .catch((error) => {
        console.log(error);
        localStorage.removeItem("token");
        window.location.href = "/";
      });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div>
      <h1>Subscription Billing System</h1>

      {user && (
        <div>
          <h2>{user.message}</h2>
          <p>User ID: {user.user_id}</p>
          <p>Email: {user.email}</p>
        </div>
      )}

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Home;