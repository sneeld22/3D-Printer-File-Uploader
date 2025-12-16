import { useEffect, useState } from "react";
import type { ModelFile } from "../common/models";
import { getQueuedPrinterJobs } from "../services/printerService";

export function usePrinterQueue() {
  const [jobs, setJobs] = useState<ModelFile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getQueuedPrinterJobs()
      .then(setJobs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return { jobs, loading };
}
