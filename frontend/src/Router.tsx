import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Playground from '@pages/Playground'
import Navbar from '@components/Navbar'
import PageNotFound from '@pages/PageNotFound'

function Router() {
   return (
      <BrowserRouter>
         <Navbar />
         <Routes>
            <Route path="/" element={<Playground />} />
            <Route path="*" element={<PageNotFound />} />
         </Routes>
      </BrowserRouter>
   )
}

export default Router