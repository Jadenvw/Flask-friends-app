import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const API_BASE = import.meta.env.VITE_API_BASE;

    async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
        e.preventDefault()
        setError(null);
        console.log("1. Submit before fetch", { username, password });

        try {
            const res = await fetch(`${API_BASE}/api/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            console.log("status", res.status, "ok", res.ok);

            if (!res.ok) {
                setError("Invalid credentials");
                return;
            }

            navigate("/friends");

        } catch (error) {
            console.error("Error logging in:", error);
        }
    }

    return (
        <div>
            <h1>Login</h1>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Username
                        <input
                            value={username}
                            onChange={(e) => { setUsername(e.target.value) }}
                            placeholder="username"
                        />
                    </label>
                    <p>State: {username}</p>
                </div>
                <div>
                    <label>
                        Password
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => { setPassword(e.target.value) }}
                            placeholder="password"
                        />
                    </label>
                    <p>State: {password}</p>
                </div>
                <button type="submit">Log in</button>
                <p>New Here? <Link to="/register">Register</Link></p>
            </form>
        </div>
    );
}

export default Login