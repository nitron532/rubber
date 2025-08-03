import axios from "axios"
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});
interface Props {
  onResponse: (data: any) => void; // ideally type the data better
}

const cleanFile = async() =>{
  try{
    const cleanResponse = await axios.get('http://127.0.0.1:5000/clean')
    return cleanResponse
  }
  catch (error){
    return error
  }
}
const InputFileUpload: React.FC<Props> = ({onResponse}) => {
  const sendFile = async (event: any) =>{
    const inputtedFiles = event.target.files
    const formData = new FormData();
      for (let i = 0; i < inputtedFiles.length; i++) {
        formData.append(`filesList[${i}]`, inputtedFiles[i]);
      }
      try{
        const response = await axios.post('http://127.0.0.1:5000/submit', formData);
        console.log(response);
        onResponse(response);
        const cleanResult = await cleanFile();
        console.log(cleanResult);
      }
      catch (error){
        console.error(error);
        onResponse(error);
        const cleanResult = await cleanFile();
        console.log(cleanResult);
      }
}
  return (
    <Button
      sx = {{mb:3}}
      component="label"
      role={undefined}
      variant="contained"
      tabIndex={-1}
      startIcon={<CloudUploadIcon />}
    >
      Upload Latex File(s)
      <VisuallyHiddenInput
        type="file"
        onChange={(event) => sendFile(event)}
        multiple
      />
    </Button>
  );
}

export default InputFileUpload;