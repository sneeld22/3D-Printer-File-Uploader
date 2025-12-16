export function formatFileSize(sizeBytes: number): string {
    if (sizeBytes < 1024 * 1024) {
        // less than 1MB, show KB
        return (sizeBytes / 1024).toFixed(2) + " KB";
    } else {
        // 1MB or more, show MB
        return (sizeBytes / 1024 / 1024).toFixed(2) + " MB";
    }
}