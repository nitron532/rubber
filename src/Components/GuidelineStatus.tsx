
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import type React from 'react';
interface Props {
    data: any
}
const GuidelineStatus: React.FC<Props> = ({data}) => {
    if(data){
        let message;
        if(data.status == 200){
            let name = data.data.name
            let severity = data.data.followsFormat === true ? "success" : "error"
            if(severity === "success"){
                message = `${name} follows formatting guidelines!`
            }
            else{
                message = `${name} does not follow formatting guidelines!`
            }
            return (
                <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity={severity as 'success' | 'error'}>
                {message}
                </Alert>
            );
        }
        // else{
        //     message = "Something went wrong."
        //     return (
        //         <Alert id = "alert" icon={<CheckIcon fontSize="inherit" />} severity="error">
        //         {message}
        //         </Alert>
        //     );
        // }
    }
}


export default GuidelineStatus;