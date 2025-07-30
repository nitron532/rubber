import { useState } from 'react'
import InputFileUpload from "./Components/InputFileUpload.tsx"
import Status from "./Components/Status.tsx"
import './App.css'


function App() {
  const [statusData, setStatusData] = useState<any>(null);

  return (
    <>
    <InputFileUpload onResponse= {setStatusData}></InputFileUpload>
    <Status data = {statusData}></Status>
    </>
  )
}

export default App
