// import React, { useState } from "react";
import { Link } from "react-router-dom";

function Register() {
    return (
        <div>
            <h1>Register</h1>
            <p>Already have an account? <Link to="/login">Login</Link></p>
        </div>
    );
}

export default Register