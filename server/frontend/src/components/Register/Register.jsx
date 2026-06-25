import React, { useState } from "react";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async (event) => {
    event.preventDefault();

    const registerUrl = window.location.origin + "/djangoapp/register";

    const response = await fetch(registerUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName: userName,
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (data.status) {
      sessionStorage.setItem("username", data.userName);
      window.location.href = window.location.origin;
    } else {
      alert(data.message || "Registration failed");
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form onSubmit={register}>
        <input
          type="text"
          placeholder="Username"
          value={userName}
          onChange={(event) => setUserName(event.target.value)}
        />

        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(event) => setFirstName(event.target.value)}
        />

        <input
          type="text"
          placeholder="Last Name"
          value={lastName}
          onChange={(event) => setLastName(event.target.value)}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
