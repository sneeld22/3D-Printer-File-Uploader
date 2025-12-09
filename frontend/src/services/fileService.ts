import apiClient from "../api/api-client.ts";
import type {ModelFile} from "../common/models.ts";

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

    const response = await apiClient.post(`/files/upload`, formData, {
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
    const response = await apiClient.get(`/files/me`);
    console.log(response.data);
    return response.data;
}

// 🔹 Delete one of my files
export async function deleteMyFile(fileId: string): Promise<void> {
    await apiClient.delete(`/files/${fileId}`);
}

// 🔹 Download one of my files as a Blob
export async function downloadFile(fileId: string): Promise<Blob> {
    const response = await apiClient.get(`/files/${fileId}/download`, {
        responseType: "blob",
    });
    return response.data;
}

// 🔹 Get all files that are not verified yet (for verifier/admin)
export async function getPendingFiles(): Promise<ModelFile[]> {
    const response = await apiClient.get(`/files/unverified`);
    console.log(response)
    return response.data;
}

// 🔹 Set verification decision for a file (approve / reject)
export async function setVerificationDecision(
    fileId: string,
    decision: "approve" | "reject"
): Promise<void> {
    await apiClient.post(`/files/${fileId}/verify`, { decision });
}