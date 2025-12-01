import { Box, Typography } from "@mui/material";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js"; // IMPORTANT

const STLModel = ({ url }: { url: string }) => {
    const geometry = useLoader(STLLoader, url);

    return (
        <mesh geometry={geometry}>
            <meshStandardMaterial color="orange" />
        </mesh>
    );
};

export default function VerificationPage() {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Verify Models
            </Typography>

            <div style={{ width: "100%", height: "400px" }}>
                <Canvas camera={{ position: [3, 3, 3] }}>
                    <ambientLight intensity={0.5} />
                    <directionalLight position={[5, 5, 5]} />

                    <STLModel url="/3DBenchy.stl" />
                    <OrbitControls />
                </Canvas>
            </div>
        </Box>
    );
}
