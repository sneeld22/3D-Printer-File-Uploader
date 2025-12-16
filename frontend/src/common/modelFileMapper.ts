import type { ModelFile } from "../common/models";

type ModelFileApi = Omit<ModelFile, "created_at"> & {
  created_at: string;
};

export function mapModelFile(api: ModelFileApi): ModelFile {
  return {
    ...api,
    created_at: new Date(api.created_at),
  };
}
