import Box from '@mui/material/Box';
export default function Header(){

    return(
        <>
            <Box sx={{ pb: 7,position: 'fixed', top: 0, left: 0, right: 0}}>
                    <h2 className="css-tffarb">EQUAL Guideline Checker</h2>
                    <p>Upload your weekly questions or other latex files to see if they follow the formatting guidelines.</p>
            </Box>
        </>
    )


}