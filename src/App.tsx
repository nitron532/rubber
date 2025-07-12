import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import InputFileUpload from "./Components/InputFileUpload.tsx"
import Status from "./Components/Status.tsx"
import './App.css'


function App() {
  const [statusData, setStatusData] = useState<any>(null);
  // const [count, setCount] = useState(0)

  return (
    <>
    <InputFileUpload onResponse= {setStatusData}></InputFileUpload>
    <Status data = {statusData}></Status>
    </>
  )
}

export default App
