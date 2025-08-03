import { useState } from 'react'
import InputFileUpload from "./Components/InputFileUpload.tsx"
import Header from "./Components/Header.tsx"
import Status from "./Components/Status.tsx"
import Footer from "./Components/Footer.tsx"
import './App.css'


function App() {
  const [statusData, setStatusData] = useState<any>(null);

  return (
    <>
    <Header></Header>
    <InputFileUpload onResponse= {setStatusData}></InputFileUpload>
    <Status data = {statusData}></Status>
    <Footer></Footer>
    </>
  )
}

export default App
