import '@styles/Navbar.scss';

function Navbar() {
   return (
      <header className="Header">
         <span className="header fw-bold" >
            PEBEKOC Compiler
         </span>
         <div className='theme-switch-btn'>
            <i className='bi-cloud-moon'></i>
            Dark mode
         </div>
      </header >
   )
}

export default Navbar