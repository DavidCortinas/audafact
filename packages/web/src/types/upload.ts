export interface UploadData {
  file?: File;
  url?: string;
}

export type UploadMethod = "file" | "url" | null;
