import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'

function PrivateRoute({ children }: { children: JSX.Element }) {
   const [loggedIn, setLoggedIn] = useState(false);
   const [loading, setLoading] = useState(true);
   const auth = getAuth()

   useEffect(() => {
      const unsubscribe = onAuthStateChanged(auth, async user => {
         if (user) {
            setLoggedIn(true)
         }
         else
            setLoggedIn(false)

         setLoading(false)
      })

      return unsubscribe
   }, [auth])

   return (
      <>
         {loading
            ? <div id='route-loading' style={{
               display: 'flex',
               justifyContent: 'center',
               alignItems: 'center',
               height: '90vh',
            }}>
               <div className="spinner-border text-info" role="status">
                  <span className="visually-hidden"></span>
               </div>
            </div>
            : loggedIn ? children : <Navigate to="/login" replace={true} />
         }
      </>
   )
}

export default PrivateRoute