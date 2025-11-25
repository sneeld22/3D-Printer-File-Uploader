// src/components/upload/MyUploadsTable.tsx
import { useEffect, useState } from "react";
import type { MouseEvent } from "react";
import {
    Alert,
    Box,
    CircularProgress,
    IconButton,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Typography,
    Tooltip,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import RefreshIcon from "@mui/icons-material/Refresh";
import {
    getMyFiles,
    deleteMyFile,
} from "../../api/files";
import type { ModelFile } from "../../api/files";
import { useAuth } from "../../auth/AuthContext";

const statusLabel: Record<ModelFile["status"], string> = {
    pending: "Pending verification",
    verified: "Verified",
    rejected: "Rejected",
    queued: "Queued for printing",
    printing: "Printing",
};

const MyUploadsTable = () => {
    const { user } = useAuth();
    const [files, setFiles] = useState<ModelFile[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [deletingId, setDeletingId] = useState<string | null>(null);

    const loadFiles = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getMyFiles();
            setFiles(data);
        } catch (err: unknown) {
            console.error(err);
            setError("Could not load your files. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        void loadFiles();
    }, []);

    const handleDeleteClick = async (
        e: MouseEvent<HTMLButtonElement>,
        id: string
    ) => {
        e.stopPropagation();
        setDeletingId(id);
        setError(null);
        try {
            await deleteMyFile(id);
            setFiles((prev) => prev.filter((f) => f.id !== id));
        } catch (err: unknown) {
            console.error(err);
            setError("Could not delete the file. Please try again.");
        } finally {
            setDeletingId(null);
        }
    };

    return (
        <Paper sx={{ mt: 4, p: 2 }}>
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    mb: 2,
                    gap: 1,
                }}
            >
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    My uploads
                </Typography>
                <Tooltip title="Reload">
                    <IconButton onClick={() => void loadFiles()} disabled={loading}>
                        <RefreshIcon />
                    </IconButton>
                </Tooltip>
            </Box>

            {loading && (
                <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
                    <CircularProgress />
                </Box>
            )}

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {!loading && files.length === 0 && !error && (
                <Typography variant="body2" color="text.secondary">
                    You haven’t uploaded any files yet.
                </Typography>
            )}

            {!loading && files.length > 0 && (
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Filename</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Uploaded</TableCell>
                            <TableCell>Owner</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {files.map((file) => (
                            <TableRow key={file.id} hover>
                                <TableCell>{file.filename}</TableCell>
                                <TableCell>{statusLabel[file.status]}</TableCell>
                                <TableCell>
                                    {new Date(file.createdAt).toLocaleString()}
                                </TableCell>
                                <TableCell>{file.ownerName}</TableCell>
                                <TableCell align="right">
                                    {/* Students, verifiers and admins can delete their OWN files.
                      Backend should enforce this; here we just show the button
                      when the logged-in user is the owner. */}
                                    {user && user.name === file.ownerName && (
                                        <Tooltip title="Delete file">
                      <span>
                        <IconButton
                            size="small"
                            color="error"
                            onClick={(e) => void handleDeleteClick(e, file.id)}
                            disabled={deletingId === file.id}
                        >
                          {deletingId === file.id ? (
                              <CircularProgress size={18} />
                          ) : (
                              <DeleteIcon fontSize="small" />
                          )}
                        </IconButton>
                      </span>
                                        </Tooltip>
                                    )}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            )}
        </Paper>
    );
};

export default MyUploadsTable;
