# 3D Printer File Uploader

## Overview

This project is a web-based portal designed for school students to upload 3D model files and send them automatically to a 3D printer for printing. It provides a streamlined, secure, and automated workflow to manage 3D printing requests within a school environment.

---

## Features

* User authentication via the school's LDAP server
* Role-based access control for uploaders and verifiers
* Upload and storage of 3D model files (e.g., STL format)
* Verification workflow before printing
* Printer queue management
* Responsive frontend built with React and Material UI
* Backend API implemented using Python FastAPI
* Fully containerized with Docker and Docker Compose
* Prebuilt images available via GitHub Container Registry (GHCR)

---

## Technologies Used

* **Frontend:** React, Material UI
* **Backend:** Python, FastAPI
* **Database:** PostgreSQL
* **Object Storage:** MinIO
* **Authentication:** LDAP integration
* **Deployment:** Docker & Docker Compose

---

## Getting Started

### Prerequisites

* Docker and Docker Compose installed
* (Optional) Access to an LDAP server for authentication

---

## 🚀 Quick Start (Recommended)

### 1. Clone the repository

```bash
git clone https://github.com/sneeld22/3D-Printer-File-Uploader.git
cd 3D-Printer-File-Uploader
```

---

### 2. Create environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` if needed (or use defaults for local development).

---

### 3. Start the application

```bash
docker compose up -d
```

---

### 4. Access the application

* Frontend: http://localhost:3000
* Backend API: http://localhost:8000
* MinIO Console: http://localhost:9001

---

## ⚙️ Environment Variables

All configuration is handled via a `.env` file.

Example variables:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app
DATABASE_URL=postgresql://postgres:postgres@db:5432/app

# MinIO
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=my-bucket
MINIO_ENDPOINT=minio:9000
MINIO_SECURE=false

# Auth
JWT_SECRET=change-me

# Admin
ADMIN_USER=admin
ADMIN_PASSWORD=admin

# LDAP (optional)
LDAP_SERVER=
LDAP_DOMAIN=
BASE_DN=
```
---

## 🐳 Docker & Deployment

This project uses prebuilt Docker images hosted on GitHub Container Registry (GHCR).

When running:

```bash
docker compose up -d
```

Docker will automatically:

* Pull the latest backend and frontend images
* Start all required services (PostgreSQL, MinIO, etc.)
* Inject environment variables from `.env`

---

## 🔄 Updating the Application

To pull the latest version:

```bash
docker compose pull
docker compose up -d
```

---

## Usage

* Log in using your LDAP account (if configured)
* Upload 3D model files via the web interface
* Verifiers can review and approve uploaded files
* Approved files are added to the printer queue
* Monitor print job status directly in the portal

---

## Project Structure

```
/frontend   → React frontend (Material UI)
/backend    → FastAPI backend
docker-compose.yml → Service orchestration
.env.example → Environment variable template
```