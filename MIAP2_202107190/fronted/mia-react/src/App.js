
import './App.css';
import React from 'react';
import Nav from './componentes/navbar';
import Card from './componentes/card';
function App() {
  return (
    <div>
      <Nav />
      <div className='container'>
        <Card />
      </div>
    </div>
  );
}

export default App;
