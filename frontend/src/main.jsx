// frontend/src/main.jsx sirve para:
// iniciar la aplicación React y montar el componente principal en el DOM.

// Dependencias del frontend
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Imports internos del frontend
import App from './App.jsx'
// Estilos del frontend
import './index.css'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
