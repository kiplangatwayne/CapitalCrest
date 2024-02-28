import React, { useState, useEffect } from "react";
import "../css/Signup.css";

function SignUp() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNo, setPhoneNo] = useState("");
  const [password, setPassword] = useState("");

  const handlePhoneChange = (e) => {
    const formattedPhoneNumber = e.target.value
      .replace(/\D/g, "")
      .replace(/(\d{3})(\d{3})(\d{4})/, "$1-$2-$3");
    setPhoneNo(formattedPhoneNumber);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("/sign-up", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        number: phoneNo,
        password: password,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      console.log(data.message);
    } else {
      console.error(data.message);
    }
  };

  useEffect(() => {
    document.body.classList.add("body-with-background");

    return () => {
      document.body.classList.remove("body-with-background");
    };
  }, []);

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
            type="password"
            placeholder="Password"
            className="my-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
        <hr />
        <p className="center-aligned">
          Already have an account? <a href="/login">Login</a>
        </p>
      </div>
    </>
  );
}

export default SignUp;
