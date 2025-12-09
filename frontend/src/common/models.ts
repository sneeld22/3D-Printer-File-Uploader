export type ModelFile = {
    id: string,
    filename: string,
    size:number,
    created_at: Date,
    user_id: string,
    verification_status: "pending" | "verified" | "rejected" | "queued" | "printing",
}
