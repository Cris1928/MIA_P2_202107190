import React from 'react';
import styled from 'styled-components';

function Navbar() {
  return (
    <> 
    <NavContainer>
    <h2>
        MIA-202107190
    </h2>  
    <div>
    <a href='/'>Home</a>
    <a class="nav-link" href="/reports">Reportes</a>
    <a class="nav-link" href="/login">iniciar sesiòn</a>
    

    </div>


    </NavContainer>  
    </>
  );
}

export default Navbar

const NavContainer = styled.nav`
h2{
    font-weight: 550;
    color: blue;
}
padding: .4rem;
background-color: #000000;
display: flex;
align-items: center;
justify-content: space-between;
a{
    text-decoration: none;
    margin-right: 1rem;
    color: yellow;
}

`