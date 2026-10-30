import React from 'react'
import { createRoot } from 'react-dom/client'
import Portal from './Portal.jsx'
import Admin from './Admin.jsx'
import './styles.css'

const isAdmin = location.pathname.replace(/\/+$/, '') === '/admin'
createRoot(document.getElementById('root')).render(isAdmin ? <Admin /> : <Portal />)
