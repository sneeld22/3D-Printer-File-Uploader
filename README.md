# 3D Printer File Uploader

## Overview

This project is a web portal for school students to upload 3D models for review. Approved files are placed in a print queue. Physical printer integration is not implemented.

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
* **Deployment:** Docker Compose and Traefik

---

## Getting Started

### Prerequisites

* Docker and Docker Compose installed
* Access to the school's LDAP server for authentication

---

## Local development

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

Edit `.env` for your local database, MinIO, and LDAP settings. LDAP is required for login. The development stack publishes ports for local testing.

---

### 3. Start the application

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

---

### 4. Access the application

* Frontend: http://localhost:3000
* Backend API: http://localhost:8000
* MinIO Console: http://localhost:9001

---

## ⚙️ Environment Variables

All configuration is handled via `.env`. Fill in every blank required value in `.env.example` before starting. The username, password, and database name in `DATABASE_URL` must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` (URL-encode special characters in the URL). `JWT_SECRET` must be at least 32 characters.

`ADMIN_USER` must be the username of an existing LDAP account. That account receives the admin role on backend startup. `VERIFIER_USERS` is an optional comma-separated list of LDAP usernames; admins can also verify files. There is no separate local admin password or local login fallback.
---

## Production deployment with Traefik

The production stack serves the app at `https://sc.htl-kaindorf.at/3DPrint/`. Traefik routes `/3DPrint/api/` and the FastAPI documentation URLs (`/3DPrint/docs`, `/3DPrint/redoc`, `/3DPrint/openapi.json`) to the backend, and the rest of `/3DPrint/` to the React frontend. Both routes remove `/3DPrint` before forwarding. FastAPI is configured with that public root path for generated URLs. The browser uses `/3DPrint` for assets, navigation, and API calls. PostgreSQL, MinIO, and the app containers have no published host ports.

Run one Traefik instance for the whole server. The supplied `docker-compose.traefik.yml` is a separate stack so other applications such as Moodle can keep working when this app is restarted. It listens on ports 80 and 443, redirects HTTP to HTTPS, and requests a Let's Encrypt certificate with the HTTP challenge. The public DNS record for `sc.htl-kaindorf.at` must point to this server, port 80 must be reachable for certificate issuance, and ports 80/443 must be available to Traefik. If the server already has a Traefik instance, use that instance instead of starting this file; its Docker network, HTTPS entry point, and certificate resolver must match the labels in `docker-compose.yml`.

1. Copy `.env.example` to `.env`. Set `TRAEFIK_ACME_EMAIL` to a real address, fill in the database and MinIO credentials, choose a strong JWT secret, and set the LDAP server, domain, and administrator username. Keep `.env` private.
2. Create the shared network once and start Traefik:

   ```bash
   docker network create traefik_proxy
   docker compose -f docker-compose.traefik.yml up -d
   ```

3. Build and start this application:

   ```bash
   docker compose up --build -d
   ```

4. Open `https://sc.htl-kaindorf.at/3DPrint/`. A direct visit to `/3DPrint/upload` should load the frontend, and an unauthenticated request to `/3DPrint/api/v1/auth/me` should return `401` from FastAPI.

The frontend image must be rebuilt after changing the public base path because Vite writes `/3DPrint/` into the built assets. The `image:` entries can still be used for published GHCR images, provided those images were built from this version of the project.

### Routing another application

Attach the other application's container to the same external `traefik_proxy` network and add its own Traefik router. For a Moodle container listening on port 80, the relevant labels would be:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.docker.network=traefik_proxy"
  - "traefik.http.routers.moodle.rule=Host(`sc.htl-kaindorf.at`) && PathPrefix(`/moodle/`)"
  - "traefik.http.routers.moodle.entrypoints=websecure"
  - "traefik.http.routers.moodle.tls=true"
  - "traefik.http.routers.moodle.tls.certresolver=letsencrypt"
  - "traefik.http.routers.moodle.middlewares=moodle-strip"
  - "traefik.http.middlewares.moodle-strip.stripprefix.prefixes=/moodle"
  - "traefik.http.services.moodle.loadbalancer.server.port=80"
```

The Moodle application must also be configured with its public URL under `https://sc.htl-kaindorf.at/moodle` so its links and assets use that prefix. Add an exact `/moodle` to `/moodle/` redirect if needed, as this project's `print-root` router does for `/3DPrint`.

---

## 🔄 Updating the Application

To rebuild from the latest project source:

```bash
git pull
docker compose up --build -d
```

---

## Usage

* Log in using your LDAP account
* Upload 3D model files via the web interface
* Verifiers can review and approve uploaded files
* Approved files are added to the printer queue
* View queued print jobs in the portal; no printer worker is included

---

## Checks

```bash
cd backend
python -m unittest discover -s tests -v

cd ../frontend
npm ci
npm run lint
npm run build
npm audit
```

Test the real LDAP login, HTTPS routing, and certificate issuance on the target server before release.

---

## Project Structure

```
/frontend   → React frontend (Material UI)
/backend    → FastAPI backend
docker-compose.yml → Service orchestration
docker-compose.traefik.yml → Shared HTTPS reverse proxy
.env.example → Environment variable template
```
