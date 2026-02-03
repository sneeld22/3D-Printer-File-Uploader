# 3D Printer File Uploader

## Overview

This project is a web-based portal designed for school students to upload 3D model files and send them automatically to a 3D printer for printing. It provides a streamlined, secure, and automated workflow to manage 3D printing requests within a school environment.

## Features

- User authentication via the school's LDAP server  
- Role-based access control for uploaders and verifiers  
- Upload and storage of 3D model files (e.g., STL format)  
- Verification workflow before printing  
- Printer queue management
- Responsive frontend built with React and Material UI  
- Backend API implemented using Python FastAPI  
- Fully containerized with Docker for easy deployment  

## Technologies Used

- **Frontend:** React, Material UI  
- **Backend:** Python, FastAPI  
- **Authentication:** LDAP integration for single sign-on  
- **Deployment:** Docker containers for frontend, backend, and services  

## Getting Started

### Prerequisites

- Docker installed on your system  
- Access to the school’s LDAP server credentials  

### Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/3d-printer-file-uploader.git
   cd 3d-printer-file-uploader
