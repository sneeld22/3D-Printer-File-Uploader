CREATE TYPE "role" AS ENUM (
  'uploader',
  'verifier',
  'downloader',
  'admin'
);

CREATE TYPE "verification_status" AS ENUM (
  'approved',
  'rejected'
);

CREATE TYPE "print_status" AS ENUM (
  'queued',
  'printing',
  'completed',
  'failed'
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "username" varchar(255) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL
);

CREATE TABLE "user_roles" (
  "user_id" uuid NOT NULL,
  "role_id" role,
  PRIMARY KEY ("user_id", "role_id")
);

CREATE TABLE "model_files" (
  "id" uuid PRIMARY KEY,
  "minio_path" varchar(255) NOT NULL,
  "filename" varchar(255) NOT NULL,
  "uploader_id" uuid NOT NULL,
  "created_at" timestamp
);

CREATE TABLE "model_verifications" (
  "id" serial PRIMARY KEY,
  "model_file_id" uuid NOT NULL,
  "verifier_id" uuid NOT NULL,
  "status" verification_status,
  "comments" text,
  "created_at" timestamp
);

CREATE TABLE "print_jobs" (
  "id" uuid PRIMARY KEY,
  "model_file_id" uuid NOT NULL,
  "requested_by" uuid NOT NULL,
  "status" print_status,
  "started_at" timestamp,
  "completed_at" timestamp,
  "created_at" timestamp
);

ALTER TABLE "user_roles" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "model_files" ADD FOREIGN KEY ("uploader_id") REFERENCES "users" ("id");

ALTER TABLE "model_verifications" ADD FOREIGN KEY ("model_file_id") REFERENCES "model_files" ("id");

ALTER TABLE "model_verifications" ADD FOREIGN KEY ("verifier_id") REFERENCES "users" ("id");

ALTER TABLE "print_jobs" ADD FOREIGN KEY ("model_file_id") REFERENCES "model_files" ("id");

ALTER TABLE "print_jobs" ADD FOREIGN KEY ("requested_by") REFERENCES "users" ("id");
