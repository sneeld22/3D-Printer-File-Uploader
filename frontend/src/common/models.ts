export type ModelFile = {
    id: string,
    filename: string,
    size:number,
    last_modified: string
    status: "pending" | "verified" | "rejected" | "queued" | "printing";
}
