import React, { useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [number, setNumber] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = () => {
    const registerData = { name, email, number, password };

    fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(registerData)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle response here
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error here
    });
  };

  const handleLogin = () => {
    const loginData = { email, number, password };

    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle response here
      localStorage.setItem('token', data.token);
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error here
    });
  };

  const handleDeposit = (amount) => {
    const depositData = { amount };

    fetch('/deposit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(depositData)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle response here
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error here
    });
  };

  return (
    <div>
      <h1>App Component</h1>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="text" placeholder="Number" value={number} onChange={(e) => setNumber(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <button onClick={() => handleDeposit(100)}>Deposit</button>
    </div>
  );
}

export default App;
