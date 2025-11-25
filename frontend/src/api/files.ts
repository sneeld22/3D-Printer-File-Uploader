// src/api/files.ts
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3000/api";

export interface UploadedFileResponse {
    id: string;
    filename: string;
    status: "pending" | "verified" | "rejected" | "queued" | "printing";
}

export async function uploadModelFile(
    file: File,
    onProgress?: (percent: number) => void
): Promise<UploadedFileResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${API_URL}/files/upload`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (event) => {
            if (!onProgress || !event.total) return;
            const percent = Math.round((event.loaded * 100) / event.total);
            onProgress(percent);
        },
    });

    return response.data;
}
