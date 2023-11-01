import React, { useState } from 'react';

function Modal({setUser}) {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [disco, setDisco] = useState('');
const [isLoggedIn, setIsLoggedIn] = useState(false);

const handleSubmit = (e) => {
    e.preventDefault();
  
    // Realiza la validación de credenciales (puedes hacerlo aquí o en el servidor)
    if (username === "usuario" && password === "contraseña") {
      
      setIsLoggedIn(true);
    }
    
  };

  
  return (
    <div>
    <h2>Login</h2>
    <input
      type="text"
      placeholder="Nombre de usuario"
      value={username}
      onChange={(e) => setUsername(e.target.value)}
    />
    <input
      type="password"
      placeholder="Contraseña"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
    />
     <input
      type="disco"
      placeholder="Disco"
      value={disco}
      onChange={(e) => setDisco(e.target.value)}
    />
    <button onClick={handleSubmit}>Iniciar sesión</button>
  </div>
  );
};

export default Modal;
