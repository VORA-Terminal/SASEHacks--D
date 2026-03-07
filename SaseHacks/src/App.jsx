import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './src/components/Header'
import { motion } from 'framer-motion'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Header />
      <div className="arcade-room">
        <motion.div 
          className="arcade-cabinet"
          initial={{ scale: 0.7, y: 50, opacity: 0 }}
          animate={{ scale: 1, y: 0, opacity: 1 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
        >
          {/* CRT Screen inside the cabinet */}
          <div className="crt-screen">
            {/* The actual game or content will go inside here! */}
            <motion.button 
              whileHover={{ scale: 1.05, textShadow: "0px 0px 8px rgb(0, 255, 0)" }}
              whileTap={{ scale: 0.95 }}
              style={{ 
                color: '#0f0', 
                background: 'none',
                border: 'none',
                width: '100%',
                textAlign: 'center', 
                /* marginTop removed so Flexbox can center it perfectly! */
                fontFamily: '"VT323", monospace',
                fontSize: '4rem',
                cursor: 'pointer',
                textShadow: '0px 0px 4px #0f0',
                zIndex: 20, /* ensure it sits above scanlines if needed */
                position: 'relative'
              }}
            >
              START
            </motion.button>
          </div>
        </motion.div>
      </div>
    </>
  )
}

export default App

