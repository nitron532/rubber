import * as React from 'react';
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

//handling for submitting multiple files needed?
const sendFile = async (event) =>{
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://127.0.0.1:5000/submit', formData)
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
}

export default function InputFileUpload() {
  return (
    <Button
      component="label"
      role={undefined}
      variant="contained"
      tabIndex={-1}
      startIcon={<CloudUploadIcon />}
    >
      Upload files
      <VisuallyHiddenInput
        type="file"
        onChange={(event) => sendFile(event)}
        multiple
      />
    </Button>
  );
}
