import React, { useState, useRef } from 'react';
import styled from 'styled-components';


function Card() {

    const [results, setResults] = useState('');
    const [commands, setCommands] = useState('');
    const [isPaused, setIsPaused] = useState(false);
    const [commands_list, setCommands_list] = useState([]);
    const textAreaRef = useRef(null);
    const apiUrl = process.env.REACT_APP_API_URL;

  
    const handleFileChange = (e) => {
      const file = e.target.files[0];
      const reader = new FileReader();
  
      reader.onload = (event) => {
        setCommands(event.target.result);
      };
  
      if (file) {
        reader.readAsText(file);
      }
    };

    const handleTextAreaKeyPress = (event) => {
        if (event.key === 'Enter') {
            if(isPaused){
                sendCommands(commands_list);
            }
        }
    };

    const sendCommands = async (commands) => {
        console.log(`funciona`)
        for (let i = 0; i < commands.length; i++) {
            
            const command = commands[i].trim();
            console.log(command)
            if (command) { // Evita enviar líneas en blanco
                setCommands_list(commands.slice(i+1, commands.length));
                if(command === 'pause'){
                    setIsPaused(true);
                    console.log(commands_list);
                    setResults(prevResults => prevResults + `[Pause] => Presiona Enter para continuar\n`);
                    break;
                }
                try {
                   // console.log("funciona1")
                   console.log(command)
                   const response = await fetch(apiUrl +'/execute', {
                        
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ command }),
                    });
            
                    const data = await response.json();
                   // const data = {mensaje:"232"}
                    console.log(data)
                    setResults(prevResults => prevResults + `${data.mensaje}\n`);
                } catch (error) {
                    console.error(`Error en la solicitudd ${i + 1}: ${error}`);
                }
            }
        }
    };

    const handleSubmit = () => {
        //Para enfocar el textarea
        textAreaRef.current.focus();
        //Para limpiar el textarea
        setResults('');
        //Para dividir los comandos por salto de línea
        const commandLines = commands.split('\n');
        //Actualizamos la lista de comandos y enviamos los comandos
        setCommands_list(commandLines);
        sendCommands(commandLines);
    };


  return (
    <> 
    <NavContainer>
    <div className="card mt-4">
      <h1 className="card-header">
        <div className='d-flex justify-content-between'>
            <p>Subir Archivo</p>
            <div>
                <input className="form-control" type="file" id="formFile" onChange={handleFileChange}></input>
            </div>
        </div>
      </h1>
      
      <div className="container-fluid mt-5 mb-3" id="123">
      <div className="row" id = "salidaconsola">
        <div className="col">
        <center> 
            <h3>
            <font color="#ffffff" face="Calibri">
                Salida
                </font>
                </h3>
                </center>
            <textarea 
                className="form-control" 
                placeholder="Escribe aquí tus comandos" 
               
                style={{height: 250}}
                value={commands}
                onChange={(e) => setCommands(e.target.value)}
            ></textarea>
        </div>
        <div className="col">
        <center> 
            <h3>
            <font color="#ffffff" face="Calibri">
                Entrada
                </font>
                </h3>
                </center>
            <textarea 
                className="form-control" 
                placeholder="Aquí aparecerán los resultados" 
                readOnly
                ref={textAreaRef}
                style={{height: 200}} 
                
                value={results}
                onKeyDown={handleTextAreaKeyPress}
            ></textarea>
        </div>
        <button className="btn btn-primary mt-5" onClick={handleSubmit}>Enviar</button>
        </div>
      </div>
      
    </div>
    </NavContainer>  
    </>
  );
}

export default Card;

const NavContainer = styled.nav`

*{
margin: 0;
padding: 0;
box-sizing: border-box;
font-family: "Poppins", sans-serif;
}
123{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #000000;
}
h1{
    font-weight: 200;
   
    color: white;
    background-color: #000000;
}
 textarea{
width: 100%;
height: 59px;
padding: 15px;
outline: none;
background-color:#151515;
color: white;
}


`