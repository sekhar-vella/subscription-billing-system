import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from "./Signup";
import Signin from "./Signin";
import Home from "./Home";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
