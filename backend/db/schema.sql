-- Enum Types
CREATE TYPE RoleEnum AS ENUM ('uploader', 'verifier', 'downloader', 'printer', 'admin');

CREATE TYPE VerificationStatus AS ENUM ('approved', 'rejected');

CREATE TYPE PrintStatus AS ENUM ('queued', 'printing', 'completed', 'failed');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL
);

-- User Roles Table (Composite Primary Key)
CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id RoleEnum NOT NULL,
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Model Files Table
CREATE TABLE model_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    minio_path VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    size BIGINT NOT NULL,
    uploader_id UUID NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_uploader FOREIGN KEY (uploader_id) REFERENCES users(id)
);

-- Model Verifications Table
CREATE TABLE model_verifications (
    id SERIAL PRIMARY KEY,
    model_file_id UUID NOT NULL,
    verifier_id UUID NOT NULL,
    status VerificationStatus NOT NULL,
    comments TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_model_file FOREIGN KEY (model_file_id) REFERENCES model_files(id),
    CONSTRAINT fk_verifier FOREIGN KEY (verifier_id) REFERENCES users(id)
);

-- Print Jobs Table
CREATE TABLE print_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_file_id UUID NOT NULL,
    requested_by UUID NOT NULL,
    status PrintStatus NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_model_file_print FOREIGN KEY (model_file_id) REFERENCES model_files(id),
    CONSTRAINT fk_requester FOREIGN KEY (requested_by) REFERENCES users(id)
);
