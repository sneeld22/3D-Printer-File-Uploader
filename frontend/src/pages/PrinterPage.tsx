import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Stack,
  CircularProgress,
} from "@mui/material";

import {
  PrinterJobStatus,
  VerificationStatus,
} from "../common/models";
import { usePrinterQueue } from "../hooks/usePrinterQueue";
import { formatFileSize } from "../utils/utils";

const printStatusColor: Record<PrinterJobStatus, "success" | "warning" | "error" | "info" | "primary"> = {
  pending: "warning",
  queued: "info",
  printing: "success",
  completed: "primary",
  failed: "error",
};

export default function PrinterPage() {
  const { jobs: unsortedJobs, loading } = usePrinterQueue();

  // Sort jobs by created_at ascending (FIFO)
  const jobs = [...unsortedJobs].sort(
    (a, b) => a.created_at.getTime() - b.created_at.getTime()
  );

  return (
    <Box sx={{ p: 4 }}>
      <Stack spacing={3}>
        <Box>
          <Typography variant="h4" fontWeight={600}>
            Printer Queue
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Files waiting to be printed
          </Typography>
        </Box>

        <Card>
          <CardContent>
            <Typography variant="h6">Queued</Typography>
            <Typography variant="h4">{jobs.length}</Typography>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Queue Details
            </Typography>

            {loading ? (
              <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Position</TableCell>
                      <TableCell>Filename</TableCell>
                      <TableCell>Size</TableCell>
                      <TableCell>Uploaded</TableCell>
                      <TableCell>Verification</TableCell>
                      <TableCell>Print Status</TableCell>
                    </TableRow>
                  </TableHead>

                  <TableBody>
                    {jobs.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={6} align="center">
                          No queued jobs
                        </TableCell>
                      </TableRow>
                    ) : (
                      jobs.map((job, index) => (
                        <TableRow key={job.id}>
                          <TableCell>{index + 1}</TableCell>
                          <TableCell>{job.filename}</TableCell>
                          <TableCell>{formatFileSize(job.size)}</TableCell>
                          <TableCell>{job.created_at.toLocaleString()}</TableCell>
                          <TableCell>
                            <Chip
                              size="small"
                              label={job.verification_status}
                              color={
                                job.verification_status === VerificationStatus.Approved
                                  ? "success"
                                  : job.verification_status === VerificationStatus.Pending
                                  ? "warning"
                                  : "error"
                              }
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              size="small"
                              label={job.print_status}
                              color={printStatusColor[job.print_status]}
                            />
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      </Stack>
    </Box>
  );
}
