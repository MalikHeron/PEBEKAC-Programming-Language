import { initializeApp } from "firebase/app";
import { getPerformance } from "firebase/performance";
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.esm.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Router from "./Router";

const firebaseConfig = {
   apiKey: "AIzaSyDVMo4d8CcEZz3kHR2syadxEAqOj6GO1Ps",
   authDomain: "utechchatbot.web.app",
   projectId: "utech-academic-advisor-chatbot",
   storageBucket: "utech-academic-advisor-chatbot.appspot.com",
   messagingSenderId: "803326633273",
   appId: "1:803326633273:web:019e81902b7ef1b85df4e8",
   measurementId: "G-RWF8SZ8MWB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Performance Monitoring and get a reference to the service
getPerformance(app);
// init aos
AOS.init();

ReactDOM.createRoot(document.getElementById('root')!).render(
   <React.StrictMode>
      <Router />
   </React.StrictMode>
)
