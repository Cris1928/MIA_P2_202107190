import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider, Route } from "react-router-dom";
import "./index.css";
import Nav from './componentes/navbar';
import Card from './componentes/card';
import Reports_Card from './componentes/reports';
import No_Access from './componentes/no_access';
import Modal from './componentes/modal';
import { global }  from './componentes/modal';

function Home() {
  return (
    <div>
      <Nav />
      <div className='container'>
        <Card />
      </div>
     
    </div>
  );
}

function Reports() {
  console.log("window.isLoggedIn")
  console.log(global)
  if(global){
    return (
      <div>
        <Nav />
        <div className='container'>
          <Reports_Card />
        </div>
       
      </div>
    );
  } else {
    return (
      <div>
        <Nav />
        <div className='container'>
          <No_Access />
        </div>
     
      </div>
    );
  }
}
function Loginn() {
  return (
    <div>
   
      <Modal />
    </div>
  );
}



const router = createBrowserRouter([
  {
    path: "/",
    element:<Home/>,
  },
  {
    path: "/reports",
    element:<Reports/>,
  },
  {
    path: "/login",
    element:<Loginn/>,
  },

]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

export default router;