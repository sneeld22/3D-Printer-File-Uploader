import { Box, Typography } from "@mui/material";

const PrinterPage = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Printer Queue
      </Typography>
      <Typography variant="body1">
        This will show which models are currently printing or waiting to be printed.
      </Typography>
    </Box>
  );
};

export default PrinterPage;
