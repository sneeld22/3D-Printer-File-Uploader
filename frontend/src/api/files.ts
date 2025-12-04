// src/api/files.ts
import axios from "axios";
import type { AxiosError } from "axios";
import type {ModelFile} from "../common/models.ts";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export interface UploadedFileResponse {
    id: string;
    filename: string;
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

// 🔹 Get all files of the currently logged-in user
export async function getMyFiles(): Promise<ModelFile[]> {
    const response = await axios.get(`${API_URL}/files/all`);
    return response.data;
}

// 🔹 Delete one of my files
export async function deleteMyFile(fileId: string): Promise<void> {
    await axios.delete(`${API_URL}/files/${fileId}`);
}

// 🔹 Download one of my files as a Blob
export async function downloadFile(fileId: string): Promise<Blob> {
    const response = await axios.get(`${API_URL}/files/${fileId}/download`, {
        responseType: "blob",
    });
    return response.data;
}

// Optional helper if you want typed errors later
export function isAxiosError(err: unknown): err is AxiosError {
    return typeof err === "object" && err !== null && "isAxiosError" in err;
}
