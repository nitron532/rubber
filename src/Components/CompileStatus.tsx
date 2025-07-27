
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import type React from 'react';
interface Props {
    data: any
}
const CompileStatus: React.FC<Props> = ({data}) => {
    if(data){
        let message;
        if(data.status == 200){
            let name = data.data.name
            let severity = data.data.compiled === true ? "success" : "error"
            if(severity === "success"){
                message = `${name} compiled succesfully!`
            }
            else if(data.data.err != "this isn't a latex file..."){
                message = `Could not compile ${name}`
            }
            else{
                message = `${name} isn't a latex file and can't be compiled!`
            }
            return (
                <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                {message}
                </Alert>
            );
        }
        else if(data.status == 413){
            message = "File uploaded was too big, there is a 16 MB limit."
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