// src/components/verifie/File3dPreview.tsx
import { Component } from "react";
import type { FC, ReactNode } from "react";
import { useEffect, useState } from "react";
import { Box, CircularProgress, Typography } from "@mui/material";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
import { ThreeMFLoader } from "three/examples/jsm/loaders/3MFLoader.js";
import { downloadFile } from "../../services/fileService.ts";

interface File3dPreviewProps {
    fileId: string | null;
    filename: string | null;
}

class PreviewErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
    state = { failed: false };

    static getDerivedStateFromError() {
        return { failed: true };
    }

    componentDidCatch(error: Error) {
        console.error("3D preview failed", error);
    }

    render() {
        if (this.state.failed) {
            return (
                <Box sx={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <Typography color="error">Preview unavailable for this file.</Typography>
                </Box>
            );
        }
        return this.props.children;
    }
}

const STLModel: FC<{ url: string }> = ({ url }) => {
    const geometry = useLoader(STLLoader, url);

    return (
        <mesh geometry={geometry}>
            <meshStandardMaterial />
        </mesh>
    );
};

const ThreeMFModel: FC<{ url: string }> = ({ url }) => {
    const model = useLoader(ThreeMFLoader, url);
    return <primitive object={model} />;
};

const File3dPreview: FC<File3dPreviewProps> = ({ fileId, filename }) => {
    const [fileUrl, setFileUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let objectUrl: string | null = null;
        let cancelled = false;

        const load = async () => {
            if (!fileId) {
                setFileUrl(null);
                return;
            }

            setLoading(true);
            setError(null);

            try {
                const blob = await downloadFile(fileId);
                if (cancelled) return;

                objectUrl = URL.createObjectURL(blob);
                setFileUrl(objectUrl);
            } catch (err) {
                console.error(err);
                if (!cancelled) {
                    setError("Could not load 3D file.");
                    setFileUrl(null);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };

        void load();

        return () => {
            cancelled = true;
            if (objectUrl) {
                URL.revokeObjectURL(objectUrl);
            }
        };
    }, [fileId]);

    if (!fileId) {
        return (
            <Box
                sx={{
                    width: "100%",
                    height: 400,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    borderRadius: 1,
                    bgcolor: "background.paper",
                    border: "1px solid",
                    borderColor: "divider",
                }}
            >
                <Typography variant="body2" color="text.secondary">
                    Select a file from the table to view it here.
                </Typography>
            </Box>
        );
    }

    return (
        <Box
            sx={{
                width: "100%",
                height: 400,
                position: "relative",
                borderRadius: 1,
                overflow: "hidden",
                border: "1px solid",
                borderColor: "divider",
            }}
        >
            {loading && (
                <Box
                    sx={{
                        position: "absolute",
                        inset: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        zIndex: 1,
                        bgcolor: "rgba(0,0,0,0.25)",
                    }}
                >
                    <CircularProgress />
                </Box>
            )}

            {error && (
                <Box
                    sx={{
                        position: "absolute",
                        inset: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        zIndex: 1,
                        bgcolor: "rgba(0,0,0,0.25)",
                    }}
                >
                    <Typography variant="body2" color="error">
                        {error}
                    </Typography>
                </Box>
            )}

            {fileUrl && (
                <PreviewErrorBoundary key={fileId}>
                    <Canvas camera={{ position: [3, 3, 3] }}>
                        <ambientLight intensity={0.5} />
                        <directionalLight position={[5, 5, 5]} />
                        {filename?.toLowerCase().endsWith(".3mf")
                            ? <ThreeMFModel url={fileUrl} />
                            : <STLModel url={fileUrl} />}
                        <OrbitControls />
                    </Canvas>
                </PreviewErrorBoundary>
            )}
        </Box>
    );
};

export default File3dPreview;
