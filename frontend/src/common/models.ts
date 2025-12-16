export const VerificationStatus = {
  Pending: 'pending',
  Approved: 'approved',
  Rejected: 'rejected',
} as const;

export type VerificationStatus = typeof VerificationStatus[keyof typeof VerificationStatus];


export const PrinterJobStatus = {
  Pending: 'pending',
  Queued: 'queued',
  Printing: 'printing',
  Completed: 'completed',
  Failed: 'failed'
} as const;

export type PrinterJobStatus = typeof PrinterJobStatus[keyof typeof PrinterJobStatus];


export type ModelFile = {
    id: string,
    filename: string,
    size: number,
    created_at: Date,
    user_id: string,
    verification_status: VerificationStatus,
    print_status: PrinterJobStatus
}
