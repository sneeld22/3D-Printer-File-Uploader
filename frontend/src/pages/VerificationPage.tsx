// src/pages/VerificationPage.tsx
import { useEffect, useState } from "react";
import type { FC } from "react";

import {
    Alert,
    Box,
    Button,
    Grid,
    Paper,
    Typography,
} from "@mui/material";

import File3dPreview from "../components/verifie/File3dPreview.tsx";
import PendingFilesTable from "../components/verifie/PendingFilesTable.tsx";

import {setVerificationDecision} from "../services/fileService.ts";
 import {getPendingFiles} from "../services/fileService.ts";
import type { ModelFile } from "../common/models.ts";

const VerificationPage: FC = () => {
    const [files, setFiles] = useState<ModelFile[]>([]);
    const [selectedFile, setSelectedFile] = useState<ModelFile | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [updatingDecision, setUpdatingDecision] = useState<"approve" | "reject" | null>(null);

    const loadPendingFiles = async () => {
        setLoading(true);
        setError(null);
        try {
            //for now only my files
            const data = await getPendingFiles();
            //const data = await getMyFiles();
            setFiles(data);
            if (!selectedFile && data.length > 0) {
                setSelectedFile(data[0]);
            }
        } catch (err) {
            console.error(err);
            setError("Could not load pending files. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        void loadPendingFiles();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleSelectFile = (file: ModelFile) => {
        setSelectedFile(file);
    };

    const handleDecision = async (decision: "approve" | "reject") => {
        if (!selectedFile) return;
        setUpdatingDecision(decision);
        setError(null);

        try {
            await setVerificationDecision(selectedFile.id, decision);

            // remove decided file from list
            setFiles((prev) => prev.filter((f) => f.id !== selectedFile.id));

            // pick next file automatically
            setSelectedFile((prevSelected) => {
                const remaining = files.filter(
                    (f) => f.id !== prevSelected?.id
                );
                return remaining.length > 0 ? remaining[0] : null;
            });
        } catch (err) {
            console.error(err);
            setError("Could not update file status. Please try again.");
        } finally {
            setUpdatingDecision(null);
        }
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Verify Models
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            <Grid container spacing={3}>
                {/* LEFT: Table of pending files */}
                <Grid>
                    <PendingFilesTable
                        files={files}
                        selectedFileId={selectedFile?.id ?? null}
                        loading={loading}
                        onSelect={handleSelectFile}
                    />
                </Grid>

                {/* RIGHT: 3D preview + approve/reject */}
                <Grid>
                    <Paper
                        sx={{
                            p: 2,
                            height: "100%",
                            display: "flex",
                            flexDirection: "column",
                        }}
                    >
                        <Typography variant="h6" gutterBottom>
                            Preview &amp; decision
                        </Typography>

                        {selectedFile ? (
                            <>
                                <Box sx={{ mb: 2 }}>
                                    <Typography variant="subtitle1">
                                        {selectedFile.filename}
                                    </Typography>
                                    {"ownerName" in selectedFile && (
                                        <Typography
                                            variant="body2"
                                            color="text.secondary"
                                        >
                                            Uploaded by{" "}
                                            {
                                                (selectedFile)
                                                    .ownerName as string
                                            }
                                        </Typography>
                                    )}
                                </Box>

                                <Box
                                    sx={{
                                        flexGrow: 1,
                                        mb: 2,
                                        minHeight: 300,
                                        width: 700
                                    }}
                                >
                                    <File3dPreview fileId={selectedFile?.id ?? null} />
                                </Box>

                                <Box
                                    sx={{
                                        display: "flex",
                                        gap: 2,
                                        justifyContent: "flex-end",
                                    }}
                                >
                                    <Button
                                        variant="outlined"
                                        color="error"
                                        disabled={updatingDecision !== null}
                                        onClick={() =>
                                            void handleDecision("reject")
                                        }
                                    >
                                        {updatingDecision === "reject"
                                            ? "Rejecting…"
                                            : "Reject"}
                                    </Button>
                                    <Button
                                        variant="contained"
                                        color="primary"
                                        disabled={updatingDecision !== null}
                                        onClick={() =>
                                            void handleDecision("approve")
                                        }
                                    >
                                        {updatingDecision === "approve"
                                            ? "Approving…"
                                            : "Approve"}
                                    </Button>
                                </Box>
                            </>
                        ) : (
                            <Typography
                                variant="body2"
                                color="text.secondary"
                            >
                                Select a file from the table to view it and make
                                a decision.
                            </Typography>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default VerificationPage;
