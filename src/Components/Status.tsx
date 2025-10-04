
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import type React from 'react';
interface Props {
    data: any
}
const Status: React.FC<Props> = ({data}) => {
    if(data){
        const alerts: React.JSX.Element[] = [];
        let message;
        if(data.status == 200){
            for(let i = 0; i < data.data.fileNames.length; i++){ //assign key to each element to avoid console error
                let isTex = true
                let name = data.data.fileNames[i]
                let severity = data.data.compiledFiles[i] === true ? "success" : "error"
                let id = `${name}${i}Compile`
                if(severity === "success"){
                    message = `${name} compiled succesfully!`
                }
                else if(data.data.errors[i] != `${name} isn't a latex file.`){
                    message = `Could not compile ${name}`
                }
                else{ 
                    message = `${name} isn't a latex file and can't be compiled!`
                    isTex = false
                }
                alerts.push(
                    <Alert key = {id} id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                        {message}
                    </Alert>
                )
                if(isTex && data.data.compiledFiles[i]){
                    id = `${name}${i}Guideline`
                    severity = data.data.passedFiles[i] === true ? "success" : "error"
                    if(severity === "success"){
                        message = `${name} follows formatting guidelines!`
                    }
                    else{
                        message = `${name} does not follow formatting guidelines!`
                        severity = "error"
                    }
                    alerts.push(
                        <Alert key = {id} id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                            {message}
                        </Alert>
                    )
                }
            }
            
            return <>{alerts}</>
        }
        else if(data.status == 413){
            message = "File(s) uploaded was too big, there is a 16 MB limit."
            return (
                <Alert key = "FileTooLarge" id = "alert" icon={<CheckIcon fontSize="inherit" />} severity="error">
                {message}
                </Alert>
            );
        }
        else{
            message = "Something went wrong. If the file compiles on old repo, TexSoup had trouble parsing it."
            return (
                <Alert key = "SomeError" id = "alert" icon={<CheckIcon fontSize="inherit" />} severity="error">
                {message}
                </Alert>
            );
        }
    }
}


export default Status;