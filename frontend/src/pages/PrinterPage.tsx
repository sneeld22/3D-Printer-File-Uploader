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
import { useEffect, useState } from "react";
import apiClient from "../api/api-client";
import { VerificationStatus } from "../common/models";
import type { ModelFile } from "../common/models";

/**
 * API shape (created_at comes as string)
 */
type ModelFileApi = Omit<ModelFile, "created_at"> & {
  created_at: string;
};

/**
 * Temporary printer status derived from verification status.
 */
type PrinterJobStatus = "printing" | "queued" | "blocked";

const mapToPrinterStatus = (file: ModelFile): PrinterJobStatus => {
  if (file.verification_status === VerificationStatus.Approved) return "queued";
  if (file.verification_status === VerificationStatus.Pending) return "blocked";
  return "blocked";
};

const statusColor: Record<PrinterJobStatus, "success" | "warning" | "error"> = {
  printing: "success",
  queued: "warning",
  blocked: "error",
};

const PrinterPage = () => {
  const [files, setFiles] = useState<ModelFile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const res = await apiClient.get<ModelFileApi[]>("/files");

        const converted: ModelFile[] = res.data.map((file) => ({
          ...file,
          created_at: new Date(file.created_at),
        }));

        setFiles(converted);
      } catch (err) {
        console.error("Failed to load printer queue", err);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  const jobs = files.map((file) => ({
    ...file,
    printerStatus: mapToPrinterStatus(file),
  }));

  return (
    <Box sx={{ p: 4 }}>
      <Stack spacing={3}>
        {/* Header */}
        <Box>
          <Typography variant="h4" fontWeight={600}>
            Printer Queue
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Models approved for printing and their current queue status
          </Typography>
        </Box>

        {/* Summary Card (Queued only) */}
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Typography variant="h6">Queued</Typography>
              <Typography variant="h4">
                {jobs.filter((j) => j.printerStatus === "queued").length}
              </Typography>
            </CardContent>
          </Card>
        </Stack>

        {/* Table */}
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
                      <TableCell>Filename</TableCell>
                      <TableCell>Size (MB)</TableCell>
                      <TableCell>Uploaded</TableCell>
                      <TableCell>Verification</TableCell>
                      <TableCell>Printer Status</TableCell>
                    </TableRow>
                  </TableHead>

                  <TableBody>
                    {jobs.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={5} align="center">
                          No models in queue
                        </TableCell>
                      </TableRow>
                    ) : (
                      jobs.map((job) => (
                        <TableRow key={job.id}>
                          <TableCell>{job.filename}</TableCell>
                          <TableCell>
                            {(job.size / 1024 / 1024).toFixed(2)}
                          </TableCell>
                          <TableCell>
                            {job.created_at.toLocaleString()}
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={job.verification_status}
                              size="small"
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
                              label={job.printerStatus}
                              size="small"
                              color={statusColor[job.printerStatus]}
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
};

export default PrinterPage;
