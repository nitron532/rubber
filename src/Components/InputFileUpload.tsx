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
//handling for submitting multiple files needed?

const InputFileUpload: React.FC<Props> = ({onResponse}) => {
  const sendFile = async (event: any) =>{
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://127.0.0.1:5000/submit', formData)
    .then(response => {
      console.log(response);
      onResponse(response)
    })
    .catch(error => {
      console.error(error);
      onResponse(error)
    });
}
  return (
    <Button
      component="label"
      role={undefined}
      variant="contained"
      tabIndex={-1}
      startIcon={<CloudUploadIcon />}
    >
      Upload Latex File
      <VisuallyHiddenInput
        type="file"
        onChange={(event) => sendFile(event)}
      />
    </Button>
  );
}

export default InputFileUpload;