import React, { useState } from "react";
import "./Register.css";

import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";


const Register = () => {
    // State variables for form inputs
    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    // Redirect to home page
    const gohome = () => {
        window.location.href = window.location.origin;
    };


    // Handle registration form submission
    const register = async (e) => {
        e.preventDefault();

        setError("");

        // Validate the form
        if (
            !userName.trim() ||
            !password ||
            !email.trim() ||
            !firstName.trim() ||
            !lastName.trim()
        ) {
            setError("Please fill in all fields.");
            return;
        }

        setLoading(true);

        try {
            // Registration API URL
            const register_url =
                window.location.origin + "/djangoapp/register";

            // Send POST request to Django
            const res = await fetch(register_url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    userName: userName.trim(),
                    password: password,
                    firstName: firstName.trim(),
                    lastName: lastName.trim(),
                    email: email.trim(),
                }),
            });

            const json = await res.json();

            // Registration successful
            if (res.ok && json.status === "Authenticated") {
                // Save username in session storage
                sessionStorage.setItem("username", json.userName);

                // Redirect to home page
                window.location.href = window.location.origin;
            }

            // Username already exists
            else if (json.error === "Already Registered") {
                setError(
                    "This username is already registered. Please choose another."
                );
            }

            // Email already exists
            else if (json.error === "Email already registered") {
                setError(
                    "This email address is already registered."
                );
            }

            // Other errors
            else {
                setError(
                    json.error || "Registration failed. Please try again."
                );
            }

        } catch (err) {
            console.error("Registration error:", err);

            setError(
                "Unable to connect to the server. Please try again."
            );

        } finally {
            setLoading(false);
        }
    };


    return (
        <div
            className="register_container"
            style={{ width: "50%" }}
        >
            <div
                className="header"
                style={{
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "space-between",
                }}
            >
                <span
                    className="text"
                    style={{ flexGrow: "1" }}
                >
                    Sign Up
                </span>

                <div
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        justifySelf: "end",
                        alignSelf: "start",
                    }}
                >
                    <a
                        href="/"
                        onClick={(e) => {
                            e.preventDefault();
                            gohome();
                        }}
                        aria-label="Close registration"
                    >
                        <img
                            style={{ width: "1cm" }}
                            src={close_icon}
                            alt="Close"
                        />
                    </a>
                </div>
            </div>

            <hr />

            <form onSubmit={register}>
                <div className="inputs">

                    {/* Username */}
                    <div className="input">
                        <img
                            src={user_icon}
                            className="img_icon"
                            alt=""
                        />

                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                            className="input_field"
                            value={userName}
                            onChange={(e) =>
                                setUserName(e.target.value)
                            }
                            autoComplete="username"
                            required
                        />
                    </div>


                    {/* First name */}
                    <div className="input">
                        <img
                            src={user_icon}
                            className="img_icon"
                            alt=""
                        />

                        <input
                            type="text"
                            name="first_name"
                            placeholder="First Name"
                            className="input_field"
                            value={firstName}
                            onChange={(e) =>
                                setFirstName(e.target.value)
                            }
                            autoComplete="given-name"
                            required
                        />
                    </div>


                    {/* Last name */}
                    <div className="input">
                        <img
                            src={user_icon}
                            className="img_icon"
                            alt=""
                        />

                        <input
                            type="text"
                            name="last_name"
                            placeholder="Last Name"
                            className="input_field"
                            value={lastName}
                            onChange={(e) =>
                                setLastName(e.target.value)
                            }
                            autoComplete="family-name"
                            required
                        />
                    </div>


                    {/* Email */}
                    <div className="input">
                        <img
                            src={email_icon}
                            className="img_icon"
                            alt=""
                        />

                        <input
                            type="email"
                            name="email"
                            placeholder="Email Address"
                            className="input_field"
                            value={email}
                            onChange={(e) =>
                                setEmail(e.target.value)
                            }
                            autoComplete="email"
                            required
                        />
                    </div>


                    {/* Password */}
                    <div className="input">
                        <img
                            src={password_icon}
                            className="img_icon"
                            alt=""
                        />

                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            className="input_field"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)
                            }
                            autoComplete="new-password"
                            required
                        />
                    </div>

                </div>


                {/* Error message */}
                {error && (
                    <p
                        role="alert"
                        style={{
                            color: "red",
                            textAlign: "center",
                            marginTop: "15px",
                        }}
                    >
                        {error}
                    </p>
                )}


                {/* Submit button */}
                <div className="submit_panel">
                    <input
                        className="submit"
                        type="submit"
                        value={
                            loading
                                ? "Registering..."
                                : "Register"
                        }
                        disabled={loading}
                    />
                </div>

            </form>
        </div>
    );
};

export default Register;
