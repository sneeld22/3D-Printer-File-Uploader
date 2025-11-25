// src/api/files.ts
import axios from "axios";
import type { AxiosError } from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3000/api";

export interface UploadedFileResponse {
    id: string;
    filename: string;
    status: "pending" | "verified" | "rejected" | "queued" | "printing";
}

// New: full model file type for lists
export interface ModelFile {
    id: string;
    filename: string;
    status: "pending" | "verified" | "rejected" | "queued" | "printing";
    ownerName: string;
    createdAt: string; // ISO string
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
    const response = await axios.get(`${API_URL}/files/mine`);
    return response.data;
}

// 🔹 Delete one of my files
export async function deleteMyFile(fileId: string): Promise<void> {
    await axios.delete(`${API_URL}/files/${fileId}`);
}

// Optional helper if you want typed errors later
export function isAxiosError(err: unknown): err is AxiosError {
    return typeof err === "object" && err !== null && "isAxiosError" in err;
}
