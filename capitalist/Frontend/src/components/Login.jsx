import React, { useState } from "react";
import "../css/Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [number, setNumber] = useState("");
  const [password, setPassword] = useState("");

  // Function to format phone number as user types
  const handlePhoneChange = (e) => {
    const formattedPhoneNumber = e.target.value
      .replace(/\D/g, "") // Remove non-numeric characters
      .replace(/(\d{3})(\d{3})(\d{4})/, "$1-$2-$3"); // Add dashes
    setNumber(formattedPhoneNumber);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        number: number,
        password: password
      })
    });

    const data = await response.json();
    if (response.ok) {
      console.log(data.message); 
    } else {
      console.error(data.message);
    }
  };

  return (
    <>
      <div className="login-div">
        <div className="login-container">
          <h3 className="center-aligned">Account Login</h3>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Email"
              className="my-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="tel"
              placeholder="Phone Number"
              pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
              className="my-input"
              value={number}
              onChange={handlePhoneChange}
              required
            />
            <input
              type="text"
              placeholder="Password"
              className="my-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          <hr />
          <p className="center-aligned">Don't have an account? <a href="/sign-up">Sign up</a></p>
        </div>
      </div>
    </>
  );
}

export default Login;
