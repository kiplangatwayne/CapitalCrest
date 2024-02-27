import React, { useState } from "react";
import "../css/Signup.css";

function SignUp() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNo, setPhoneNo] = useState("");
  const [password, setPassword] = useState("");

  // Function to format phone number as user types
  const handlePhoneChange = (e) => {
    const formattedPhoneNumber = e.target.value
      .replace(/\D/g, "") // Remove non-numeric characters
      .replace(/(\d{3})(\d{3})(\d{4})/, "$1-$2-$3"); // Add dashes
    setPhoneNo(formattedPhoneNumber);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('/sign-up', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        email: email,
        number: phoneNo,
        password: password
      })
    });

    const data = await response.json();
    if (response.ok) {
      // Handle successful sign-up
      console.log(data.message); // or redirect user
    } else {
      // Handle sign-up error
      console.error(data.message);
    }
  };

  return (
    <>
      <div className="sign-up-container">
        <h2 className="sign-up-heading">Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="User Name"
            className="my-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
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
            value={phoneNo}
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
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </>
  );
}

export default SignUp;
