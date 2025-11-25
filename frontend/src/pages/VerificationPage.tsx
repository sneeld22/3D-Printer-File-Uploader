import { Box, Typography } from "@mui/material";

const VerificationPage = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Verify Models
      </Typography>
      <Typography variant="body1">
        Here students can review uploaded models and mark them as valid/invalid.
      </Typography>
    </Box>
  );
};

export default VerificationPage;
