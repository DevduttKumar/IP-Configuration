import React, { useState } from 'react'
import DataViewer from './components/DataViewer'
import './App.css'
import NetworkDashboard from './components/NetworkDashboard'

export default function App() {
  const [showModal, setShowModal] = useState(false)
  const [hasData, setHasData] = useState(false)

  return (
    // <DataViewer/>
    <NetworkDashboard/>
  )
}
