//import { initializeApp } from "firebase/app";
//import { getPerformance } from "firebase/performance";
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.esm.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Router from "./Router";

/*const firebaseConfig = {
   apiKey: "",
   authDomain: "",
   projectId: "",
   storageBucket: "",
   messagingSenderId: "",
   appId: "",
   measurementId: ""
};*/

// Initialize Firebase
//const app = initializeApp(firebaseConfig);
// Initialize Performance Monitoring and get a reference to the service
//getPerformance(app);
// init aos
AOS.init();

ReactDOM.createRoot(document.getElementById('root')!).render(
   <React.StrictMode>
      <Router />
   </React.StrictMode>
)
