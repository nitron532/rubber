import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

export default function Footer(){
    return (
        <>
        <Box sx={{ pb: 7 }}>
            <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, bgcolor: "#212121", color: "#EDEDED", pb:1, pt:1}} elevation={3}>
                <p>Developed by Alvin Lee, 2025.</p>
            </Paper>
        </Box>
        </>
    );
}