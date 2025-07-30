
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import type React from 'react';
interface Props {
    data: any
}
const CompileStatus: React.FC<Props> = ({data}) => {
    if(data){
        const alerts: React.JSX.Element[] = [];
        let message;
        if(data.status == 200){
            for(let i = 0; i < data.data.fileNames.length; i++){ //assign key to each element to avoid console error
                let name = data.data.fileNames[i]
                let severity = data.data.compiledFiles[i] === true ? "success" : "error"
                if(severity === "success"){
                    message = `${name} compiled succesfully!`
                }
                else if(data.data.err != "this isn't a latex file..."){
                    message = `Could not compile ${name}`
                }
                // else{ err was removed from response object, i'll add it back later
                //     message = `${name} isn't a latex file and can't be compiled!`
                // }
                alerts.push(
                    <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                        {message}
                    </Alert>
                )
                severity = data.data.passedFiles[i] === true ? "success" : "error"
                if(severity === "success" && data.data.compiledFiles[i]){
                    message = `${name} follows formatting guidelines!`
                }
                else{
                    message = `${name} does not follow formatting guidelines!`
                    severity = "error"
                }
                alerts.push(
                    <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                        {message}
                    </Alert>
                )
            }
            
            return <>{alerts}</>
        }
        else if(data.status == 413){
            message = "File(s) uploaded was too big, there is a 16 MB limit."
            return (
                <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity="error">
                {message}
                </Alert>
            );
        }
        else{
            message = "Something went wrong."
            return (
                <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity="error">
                {message}
                </Alert>
            );
        }
    }
}


export default CompileStatus;