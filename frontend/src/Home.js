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
    <div className="home-page">
      <nav className="navbar">
        <div className="brand">
          💳 Subscription Billing
        </div>

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </nav>

      <main className="dashboard">
        {user && (
          <>
            <div className="welcome-section">
              <p className="small-title">DASHBOARD</p>
              <h1>Welcome back! 👋</h1>
              <p>Manage your subscriptions and billing information.</p>
            </div>

            <div className="user-card">
              <div className="profile-icon">👤</div>

              <div>
                <h2>{user.message}</h2>
                <p>
                  <strong>User ID:</strong> {user.user_id}
                </p>
                <p>
                  <strong>Email:</strong> {user.email}
                </p>
              </div>
            </div>

            <div className="feature-grid">
              <div className="feature-card">
                <div className="feature-icon">📋</div>
                <h3>My Subscription</h3>
                <p>View and manage your current subscription.</p>
                <button>View Subscription</button>
              </div>

              <div className="feature-card">
                <div className="feature-icon">💰</div>
                <h3>Billing</h3>
                <p>Check your billing and payment information.</p>
                <button>View Billing</button>
              </div>

              <div className="feature-card">
                <div className="feature-icon">⭐</div>
                <h3>Plans</h3>
                <p>Explore available subscription plans.</p>
                <button>View Plans</button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default Home;