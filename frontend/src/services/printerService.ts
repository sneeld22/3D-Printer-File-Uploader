import apiClient from "../api/api-client";
import type { ModelFile } from "../common/models";
import { mapModelFile } from "../common/modelFileMapper";

/**
 * Fetch only queued files from backend.
 */
export async function getQueuedPrinterJobs(): Promise<ModelFile[]> {
  const res = await apiClient.get("/files/queued");
  return res.data.map(mapModelFile);
}
