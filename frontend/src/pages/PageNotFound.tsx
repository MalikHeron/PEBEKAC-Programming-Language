import '@styles/LandingPage.scss'
import { useEffect } from 'react';
import { Link } from 'react-router-dom'

function PageNotFound() {

   useEffect(() => {
      window.scrollTo(0, 0);
   }, []);

   return (
      <div
         className='PageNotFound'
         style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '90vh',
         }}
      >
         <img
            className='sophie'
            src='/icon.png'
            alt="sophie malfunctioning"
            data-aos="fade-down"
            data-aos-delay="100"
            style={{
               width: '10em',
               height: 'auto',
               transform: 'rotate(35deg)',
            }}
         />
         <h1
            style={{
               fontSize: '4rem',
               marginBottom: '1rem',
            }}
            data-aos="fade-down"
            data-aos-delay="100"
         >
            4 0 4
         </h1>
         <h3>Page not found</h3>

         <p style={{ color: 'gray' }} data-aos="fade-down" data-aos-delay="300">
            The page you are looking for does not exist.
         </p>

         <Link to='/' data-aos="fade-down" data-aos-delay="500">
            <button className='btn btn-primary'>
               Go Home
            </button>
         </Link>
      </div>
   )
}

export default PageNotFound