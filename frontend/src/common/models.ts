export type ModelFile = {
    object_name:string,
    size:number,
    last_modified: string
    id: string;
    filename: string;
    status: "pending" | "verified" | "rejected" | "queued" | "printing";
    ownerName: string;
}
