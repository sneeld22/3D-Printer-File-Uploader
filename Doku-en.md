# Project Documentation

## 3D Printer File Uploader

**Technologies:** React, Material UI, FastAPI, Docker, LDAP, PostgreSQL, MinIO

---

## 1. Introduction

3D printing is playing an increasingly important role in the school environment, especially in technical and creative subjects. This often leads to organizational challenges, as 3D models have to be submitted, reviewed, and printed manually. This results in a lack of clarity, errors, and increased workload for teachers and students.

The goal of this project was to develop a central web portal through which students can upload their 3D models. These models are then reviewed, managed, and automatically forwarded to a 3D printer.

---

## 2. Project Objectives

The objective of the project is to develop a secure, user-friendly, and maintainable system for managing 3D printing jobs within the school.

Specifically, the system should allow:

* Students to upload 3D files
* Existing school accounts to be used for authentication
* Print jobs to be reviewed and approved
* An automatic print queue to exist

---

## 3. Project Description

The project is a web-based 3D printer management system. It consists of a frontend for user interaction and a backend for business logic, file management, and user management.

The typical workflow of a print job is:

1. Student logs in using a school account
2. Upload of a 3D model (e.g. STL file)
3. Verification by authorized users
4. Placement in the printer queue
5. Automatic printing

---

## 4. Requirements

### 4.1 Functional Requirements

* Upload of 3D files
* User authentication via LDAP
* Role and permission system
* Verification of print jobs
* Management of a print queue
* Status display of print jobs

### 4.2 Non-Functional Requirements

* Security and access control
* User-friendly interface
* Maintainability and extensibility
* Platform independence

---

## 5. Technology Selection

### Frontend – React

React was chosen because it is a modern and widely used JavaScript library that enables a reactive and modular user interface. The component-based structure simplifies maintenance and extension.

### UI – Material UI

Material UI provides prebuilt, consistent UI components and enables rapid development of a professional interface without requiring custom design work.

### Backend – FastAPI (Python)

FastAPI is a modern, high-performance Python framework for APIs. It provides automatic validation and documentation, which accelerates development and reduces errors.

### Authentication – LDAP

By using the school’s LDAP server, existing school accounts can be reused. This increases security and simplifies user management.

### Database – PostgreSQL

PostgreSQL is used to store user data, roles, and print jobs. It is stable, powerful, and widely used.

### File Storage – MinIO

MinIO serves as an S3-compatible object storage for 3D files. This allows large files to be stored efficiently and securely.

### Containerization – Docker

Docker makes it possible to run all components in isolated containers. The entire system can be started with a single command.

---

## 6. System Architecture

The system consists of the following containers:

* Frontend (React)
* Backend (FastAPI)
* PostgreSQL database
* MinIO object storage

The frontend communicates with the backend via HTTP. The backend accesses the database and file storage and manages the print jobs.

---

## 7. Docker Setup

The project is orchestrated using Docker Compose. All required services are started together.

### Services Used

* **Backend:** FastAPI application on port 8000
* **Frontend:** React application on port 3000
* **Database:** PostgreSQL 15
* **Object Storage:** MinIO (ports 9000 and 9001)

Persistent data is stored using Docker volumes.

---

## 8. Implementation

### Frontend

* LDAP login
* File upload
* Status display of print jobs
* Role-based user interface

### Backend

* REST API with FastAPI
* LDAP authentication
* Role and permission checks
* Management of the printer queue
* Storage of metadata in PostgreSQL
* Storage of files in MinIO

---

## 9. Role and Permission System

To control access, the system uses a role-based authorization concept. Each user can have one or more roles, which define which actions are permitted within the system.

The available roles are:

* **uploader** – May upload 3D models and view their own files.
* **verifier** – May review uploaded models and approve or reject them.
* **downloader** – May view and download files.
* **printer** – Intended for the printing process and can process print jobs.
* **admin** – Has full access to the system, including user, file, and print management.

Role assignment is handled via the `user_roles` table, which links users and roles.

---

## 10. Security Aspects

* Authentication via LDAP
* Authorization via roles
* Protected API endpoints
* Storage of sensitive configuration via environment variables
* Centralized logging of all API requests

All incoming API requests are logged server-side and written to a log file. This logging supports error analysis, traceability of actions, and overall system security.

---

## 11. Testing

The following were tested:

* User authentication
* File upload
* Role and permission checks
* Printer queue workflow
* Docker setup

The system operates stably in the local Docker setup.

---

## 12. Challenges

* LDAP integration
* Synchronization between frontend and backend
* Management of the print queue
* Docker networking and environment variables

All issues were resolved through research and iterative development.

---

## 13. Conclusion and Outlook

The project demonstrates a practical solution for organizing 3D print jobs in a school environment. Modern technologies were combined effectively.

Possible extensions:

* Printer integration
* Support for multiple printers
* Email notifications
* Print time calculation
* Role management via the dashboard

---
## 14. API Documentation

The API is implemented as a REST API using FastAPI and is available under the base path `/api/v1`. Authentication is handled via JWT tokens, which must be sent in the Authorization header (`Bearer Token`) after a successful login.

---

### 14.1 Authentication (`/auth`)

#### POST `/api/v1/auth/login`

**Description:**
Authenticates a user via the school’s LDAP server and returns a JWT access token.

**Request Body:**

* `username` (string): School username
* `password` (string): Password

**Response:**

* `access_token` (string): JWT token
* `token_type` (string): `bearer`

---

#### GET `/api/v1/auth/me`

**Description:**
Returns information about the currently logged-in user.

**Authentication:** required

**Response:**

* User ID
* Username
* Roles

---

### 14.2 Files (`/files`)

#### POST `/api/v1/files/upload`

**Description:**
Uploads a 3D model file (e.g. STL). The file is stored in object storage and metadata is saved in the database.

**Roles:** `uploader`, `admin`

**Request:**

* Multipart file upload

**Response:**

* File ID
* File name
* Upload timestamp

---

#### GET `/api/v1/files/all`

**Description:**
Returns a list of all uploaded files.

**Roles:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/unverified`

**Description:**
Lists all files that have not yet been verified.

**Roles:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/queued`

**Description:**
Returns all files that are currently in the print queue.

**Roles:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/me`

**Description:**
Returns all files belonging to the currently logged-in user.

**Roles:** `uploader`, `admin`

---

#### GET `/api/v1/files/user/{user_id}`

**Description:**
Lists all files of a specific user.

**Roles:** `admin`

---

#### GET `/api/v1/files/{file_id}`

**Description:**
Returns metadata for a single file.

**Parameters:**

* `file_id` (UUID)

---

#### GET `/api/v1/files/{file_id}/download`

**Description:**
Downloads the original file from object storage.

**Parameters:**

* `file_id` (UUID)

---

#### DELETE `/api/v1/files/{file_id}`

**Description:**
Deletes a file including its metadata and stored file.

**Roles:** `admin`

---

### 14.3 Verification (`/verifications`)

#### POST `/api/v1/verifications`

**Description:**
Verifies or rejects an uploaded file. After successful verification, the file can be added to the print queue.

**Roles:** `uploader`, `admin`

**Request Body:**

* `file_id` (UUID)
* `approved` (boolean)
* `comment` (optional)

---

### 14.4 Print Jobs (`/prints`)

#### POST `/api/v1/prints`

**Description:**
Creates a new print job and adds it to the printer queue.

**Roles:** `uploader`, `admin`

**Request Body:**

* `model_file_id` (UUID)

---

#### GET `/api/v1/prints`

**Description:**
Returns all print jobs in the system.

**Roles:** `admin`

---

#### GET `/api/v1/prints/{job_id}`

**Description:**
Returns details for a specific print job.

**Roles:** `admin`

---

# 15 Environment Variables (.env File)

A `.env` file is used to configure the system. It contains all important environment variables for the database, backend, authentication, and file storage. Sensitive information such as passwords or secrets is therefore not stored directly in the source code, improving security and maintainability.

## 15.1 Database Configuration (PostgreSQL)

POSTGRES_USER
Username used by the backend to authenticate with the PostgreSQL database.

POSTGRES_PASSWORD
Password for the database user.

POSTGRES_DB
Name of the database in which all metadata such as users, roles, files, and print jobs are stored.

---

## 15.2 Backend Configuration

DATABASE_URL
Connection URL to the PostgreSQL database. It contains the username, password, host, port, and database name and is used by the backend for database access.

ADMIN_USER
Username of the initial administrator, which is automatically created when the system is started for the first time.

ADMIN_PASSWORD
Password for the administrator account.

JWT_SECRET
Secret key used to sign and validate JSON Web Tokens (JWT). This key ensures that authentication tokens cannot be tampered with.

---

## 15.3 LDAP Configuration

LDAP_SERVER
IP address or hostname of the school’s LDAP server used for user authentication.

LDAP_DOMAIN
School domain used for login with school accounts.

BASE_DN
Base Distinguished Name of the LDAP directory. It defines the search scope in which user accounts are located.

---

## 15.4 MinIO Configuration (File Storage)

MINIO_ENDPOINT
Address of the MinIO server used to store and retrieve 3D model files.

MINIO_ACCESS_KEY
Access key (username) for the MinIO object storage.

MINIO_SECRET_KEY
Secret key (password) for accessing MinIO.

MINIO_BUCKET
Name of the bucket in which all uploaded 3D model files are stored.

MINIO_SECURE
Indicates whether the connection to MinIO is encrypted (HTTPS) or unencrypted (HTTP). In development environments, this is often set to `False`.

---

# 16 Role Bootstrap Configuration (`backend/role_bootstrap.yaml`)

To initialize the system, a configuration file named `role_bootstrap.yaml` is used. This file defines which users automatically receive specific roles when the backend is started for the first time.

## 16.1 File Structure

The file is structured in YAML format. Each role is defined as a key and contains a list of usernames to which this role is assigned.

Example:

```
admin:
  - user1
  - user2
```

---

# 17 Docker Setup – Development and Production Environments

The project uses **two Docker Compose files**:

* `docker-compose.yml` → **Production / standard operation**
* `docker-compose.dev.yml` → **Development mode with hot reload**

This separation enables a stable production environment as well as a comfortable development environment in which code changes are applied automatically.

---

## 17.1 Docker Compose – Production (`docker-compose.yml`)

The `docker-compose.yml` file defines the complete system architecture for regular operation of the application.

### Backend

* FastAPI application
* Built using a multi-stage Dockerfile
* API accessible on port **8000**
* Configuration via environment variables from the `.env` file
* Dependencies:

  * PostgreSQL database
  * MinIO object storage

In this variant, **no hot reload** is used, as it is optimized for stability and performance.

---

### Frontend

* React application with Vite
* Build process generates static files
* Served via **Nginx**
* Accessible on port **3000**

---

### PostgreSQL (Database)

* Uses the official `postgres:15` image
* Persistent storage via Docker volume `pgdata`
* Credentials are set via environment variables

---

### MinIO (Object Storage)

* S3-compatible object storage for 3D model files
* Ports:

  * `9000` → API access
  * `9001` → Web console
* Persistent data via Docker volume `minio_data`

---

### Volumes

* `pgdata` → PostgreSQL data
* `minio_data` → stored files

---

## 17.2 Docker Compose – Development (`docker-compose.dev.yml`)

The `docker-compose.dev.yml` file is intended for development and enables **hot reload** for both backend and frontend.

---

### Backend (Development)

* Uses `Dockerfile.dev`
* Source code is mounted as a volume (`./backend:/app`)
* Starts `uvicorn` with `--reload`
* Code changes trigger an automatic server restart

---

### Frontend (Development)

* Uses `Dockerfile.dev`
* Source code is mounted as a volume (`./frontend:/app`)
* Starts the Vite development server
* Internal port **5173**, forwarded externally to **3000**
* `CHOKIDAR_USEPOLLING=true` ensures file system changes are detected

---

### Shared Services

PostgreSQL and MinIO are defined identically in both Docker Compose files to keep development and production environments as consistent as possible.

---

## 17.3 Dockerfiles – Overview

### Frontend (`Dockerfile`)

* Multi-stage build
* Node.js for building the application
* Nginx for serving static files
* Optimized for small image size and performance

---

### Frontend (`Dockerfile.dev`)

* Node.js image
* Starts the Vite development server
* Code is mounted from the host via a volume
* Supports hot reload

---

### Backend (`Dockerfile`)

* Multi-stage build
* Python dependencies are preinstalled
* Starts the FastAPI application without reload mode
* Suitable for production use

---

### Backend (`Dockerfile.dev`)

* Simple Python image
* Source code mounted via volume
* Starts `uvicorn` with `--reload`
* Ideal for development

---