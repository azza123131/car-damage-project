import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import App from './App.jsx'
import Model from './model.jsx'
import Graphs from './Graph.jsx'

import { BrowserRouter, Routes, Route } from "react-router-dom"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/Graph" element={<Graphs />} />
        <Route path="/model" element={<Model />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
)