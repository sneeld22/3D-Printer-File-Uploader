// src/components/verifie/PendingFilesTable.tsx
import type { FC } from "react";
import {
    Box,
    CircularProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";
import type { ModelFile } from "../../common/models.ts";

interface PendingFilesTableProps {
    files: ModelFile[];
    selectedFileId: string | null;
    loading: boolean;
    onSelect: (file: ModelFile) => void;
}

const PendingFilesTable: FC<PendingFilesTableProps> = ({
                                                           files,
                                                           selectedFileId,
                                                           loading,
                                                           onSelect,
                                                       }) => {
    return (
        <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
                Pending files
            </Typography>

            {loading ? (
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        py: 4,
                    }}
                >
                    <CircularProgress />
                </Box>
            ) : files.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                    There are currently no files waiting for verification.
                </Typography>
            ) : (
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Filename</TableCell>
                            <TableCell>Uploaded</TableCell>
                            <TableCell>Owner</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {files.map((file) => (
                            <TableRow
                                key={file.id}
                                hover
                                selected={selectedFileId === file.id}
                                sx={{ cursor: "pointer" }}
                                onClick={() => onSelect(file)}
                            >
                                <TableCell>{file.filename}</TableCell>
                                <TableCell>
                                    {/* assumes createdAt is an ISO string; adjust if needed */}
                                    {"createdAt" in file
                                        ? new Date(
                                            (file as any).createdAt as string
                                        ).toLocaleString()
                                        : "–"}
                                </TableCell>
                                <TableCell>
                                    {"ownerName" in file
                                        ? ((file as any).ownerName as string)
                                        : "–"}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            )}
        </Paper>
    );
};

export default PendingFilesTable;
