import { useState } from 'react'
import InputFileUpload from "./Components/InputFileUpload.tsx"
import CompileStatus from "./Components/CompileStatus.tsx"
import GuidelineStatus from "./Components/GuidelineStatus.tsx"
import './App.css'


function App() {
  const [statusData, setStatusData] = useState<any>(null);
  // const [count, setCount] = useState(0)

  return (
    <>
    <InputFileUpload onResponse= {setStatusData}></InputFileUpload>
    <CompileStatus data = {statusData}></CompileStatus>
    <GuidelineStatus data = {statusData}></GuidelineStatus>
    </>
  )
}

export default App
