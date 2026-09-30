# Projektdokumentation

## 3D Printer File Uploader

**Technologien:** React, Material UI, FastAPI, Docker, LDAP, PostgreSQL, MinIO

---

## 1. Einleitung

Der 3D-Druck spielt im schulischen Umfeld eine immer größere Rolle, insbesondere in technischen und kreativen Fächern. Dabei entstehen häufig organisatorische Probleme, da 3D-Modelle manuell abgegeben, geprüft und gedruckt werden müssen. Dies führt zu Unübersichtlichkeit, Fehlern und erhöhtem Aufwand für Lehrkräfte und Schüler.

Ziel dieses Projekts war es, ein zentrales Web-Portal zu entwickeln, über das Schüler ihre 3D-Modelle hochladen können. Die Modelle werden überprüft; freigegebene Dateien landen in einer Warteschlange. Ein Drucker-Worker und die Anbindung an einen physischen Drucker sind nicht enthalten.

---

## 2. Zielsetzung des Projekts

Das Ziel des Projekts ist die Entwicklung eines sicheren, benutzerfreundlichen und wartbaren Systems zur Verwaltung von 3D-Druckaufträgen innerhalb der Schule.

Konkret sollen:

* Schüler 3D-Dateien hochladen können
* bestehende Schul-Accounts zur Anmeldung genutzt werden
* Druckaufträge überprüft und freigegeben werden
* eine automatische Druck-Warteschlange existieren

---

## 3. Projektbeschreibung

Das Projekt ist ein webbasiertes 3D-Printer-Management-System. Es besteht aus einem Frontend für die Benutzerinteraktion und einem Backend für die Geschäftslogik, Datei- und Benutzerverwaltung.

Der typische Ablauf eines Druckauftrags ist:

1. Schüler meldet sich mit Schulaccount an
2. Upload eines 3D-Modells (z. B. STL-Datei)
3. Verifikation durch berechtigte Nutzer
4. Einreihung in die Printer Queue
5. Druck durch einen separaten Prozess (hier nicht implementiert)

---

## 4. Anforderungen

### 4.1 Funktionale Anforderungen

* Upload von 3D-Dateien
* Benutzeranmeldung über LDAP
* Rollen- und Rechtesystem
* Verifikation von Druckaufträgen
* Verwaltung einer Druck-Warteschlange
* Statusanzeige der Druckaufträge

### 4.2 Nicht-funktionale Anforderungen

* Sicherheit und Zugriffskontrolle
* Benutzerfreundliche Oberfläche
* Wartbarkeit und Erweiterbarkeit
* Plattformunabhängigkeit

---

## 5. Technologiewahl

### Frontend – React

React wurde gewählt, da es eine moderne und weit verbreitete JavaScript-Bibliothek ist, die eine reaktive und modulare Benutzeroberfläche ermöglicht. Die komponentenbasierte Struktur erleichtert Wartung und Erweiterung.

### UI – Material UI

Material UI bietet vorgefertigte, konsistente UI-Komponenten und ermöglicht eine schnelle Entwicklung einer professionellen Oberfläche ohne eigenen Designaufwand.

### Backend – FastAPI (Python)

FastAPI ist ein modernes, performantes Python-Framework für APIs. Es bietet automatische Validierung und Dokumentation, was die Entwicklung beschleunigt und Fehler reduziert.

### Authentifizierung – LDAP

Durch die Nutzung des schulischen LDAP-Servers können bestehende Schul-Accounts verwendet werden. Dies erhöht die Sicherheit und vereinfacht die Benutzerverwaltung.

### Datenbank – PostgreSQL

PostgreSQL wird zur Speicherung von Benutzerdaten, Rollen und Druckaufträgen verwendet. Es ist stabil, leistungsfähig und weit verbreitet.

### Dateispeicher – MinIO

MinIO dient als S3-kompatibler Objektspeicher für die 3D-Dateien. Dadurch können große Dateien effizient und sicher gespeichert werden.

### Containerisierung – Docker

Docker ermöglicht es, alle Komponenten isoliert in Containern zu betreiben. Das gesamte System kann mit einem einzigen Befehl gestartet werden.

---

## 6. Systemarchitektur

Das System besteht aus folgenden Containern:

* Frontend (React)
* Backend (FastAPI)
* PostgreSQL-Datenbank
* MinIO Objektspeicher

Das Frontend kommuniziert über HTTP mit dem Backend. Das Backend greift auf die Datenbank und den Dateispeicher zu und verwaltet die Druckaufträge.

---

## 7. Docker-Setup

Die Anwendung wird über Docker Compose orchestriert. Im Produktivbetrieb stellt ein separater Traefik-Stack den gemeinsamen HTTPS-Zugang bereit.

### Verwendete Services

* **Backend:** FastAPI-Anwendung auf internem Port 8000
* **Frontend:** React-Anwendung auf internem Port 3000
* **Datenbank:** PostgreSQL 15
* **Objektspeicher:** MinIO auf den internen Ports 9000 und 9001
* **Reverse Proxy:** Traefik auf den öffentlichen Ports 80 und 443

Persistente Daten werden über Docker Volumes gespeichert.

---

## 8. Implementierung

### Frontend

* Login über LDAP
* Datei-Upload
* Statusanzeige der Druckaufträge
* Rollenbasierte Benutzeroberfläche

### Backend

* REST-API mit FastAPI
* LDAP-Authentifizierung
* Rollen- und Rechteprüfung
* Verwaltung der Printer Queue
* Speicherung von Metadaten in PostgreSQL
* Speicherung von Dateien in MinIO

---

## 9. Rollen- und Rechtesystem

Zur Zugriffskontrolle verwendet das System ein rollenbasiertes Berechtigungskonzept. Jeder Benutzer kann eine oder mehrere Rollen besitzen, welche festlegen, welche Aktionen im System erlaubt sind.

Die verfügbaren Rollen sind:

* **uploader**
  Darf 3D-Modelle hochladen und eigene Dateien einsehen.

* **verifier**
  Darf hochgeladene Modelle überprüfen und freigeben oder ablehnen.

* **downloader**
  Darf Dateien einsehen und herunterladen.

* **printer**
  Ist für den Druckprozess vorgesehen und kann Druckaufträge verarbeiten (z. B. für zukünftige Automatisierung).

* **admin**
  Hat Vollzugriff auf das System, inklusive Benutzer-, Datei- und Druckverwaltung.

Die Zuordnung der Rollen erfolgt über die Tabelle `user_roles`, welche Benutzer und Rollen miteinander verknüpft.

---

## 10. Sicherheitsaspekte

* Authentifizierung über LDAP
* Autorisierung über Rollen
* Geschützte API-Endpunkte
* Speicherung sensibler Konfigurationen über Umgebungsvariablen
* Zentrales Logging aller API-Requests

Alle eingehenden API-Anfragen werden serverseitig mitgeloggt und in eine Logdatei geschrieben. Dieses Logging dient der Fehleranalyse, Nachvollziehbarkeit von Aktionen sowie der allgemeinen Systemsicherheit.

---

## 11. Tests

Automatisierte Prüfungen decken Rollenzuweisung, Upload-Beschränkungen, Dateizugriffsrechte und die Konsistenz zwischen Freigabe und Warteschlange ab. Frontend-Lint und Produktions-Build sind erfolgreich; die Compose-Dateien werden erfolgreich validiert. Ein Live-Test mit dem LDAP-Server der Schule, PostgreSQL, MinIO und Traefik ist auf dem Zielserver noch erforderlich.

---

## 12. Herausforderungen

* LDAP-Integration
* Synchronisation zwischen Frontend und Backend
* Verwaltung der Druck-Warteschlange
* Docker-Netzwerk und Umgebungsvariablen

Die verbleibenden Bereitstellungsprüfungen benötigen die Zielinfrastruktur.

---

## 13. Fazit und Ausblick

Das Projekt zeigt eine praxisnahe Lösung für die Organisation von 3D-Druckaufträgen im schulischen Umfeld. Moderne Technologien wurden sinnvoll kombiniert.

Mögliche Erweiterungen:

* Drucker Anbindung
* Unterstützung mehrerer Drucker
* Benachrichtigungen per E-Mail
* Druckzeitberechnung
* Rollenverwaltung über das Dashboard

---

## 14. API-Dokumentation

Die API ist als REST-API mit FastAPI umgesetzt. Ihr interner Basis-Pfad ist `/api/v1`; über Traefik ist sie unter `https://sc.htl-kaindorf.at/3DPrint/api/v1` erreichbar. Die Authentifizierung erfolgt über JWT-Tokens, die nach erfolgreichem Login im Authorization-Header (`Bearer Token`) mitgesendet werden müssen.

---

### 14.1 Authentifizierung (`/auth`)

#### POST `/api/v1/auth/login`

**Beschreibung:**
Authentifiziert einen Benutzer über den LDAP-Server der Schule und gibt ein JWT-Access-Token zurück.

**Request Body:**

* `username` (string): Schulbenutzername
* `password` (string): Passwort

**Response:**

* `access_token` (string): JWT Token
* `token_type` (string): `bearer`

---

#### GET `/api/v1/auth/me`

**Beschreibung:**
Gibt Informationen über den aktuell eingeloggten Benutzer zurück.

**Authentifizierung:** erforderlich

**Response:**

* Benutzer-ID
* Benutzername
* Rollen

---

### 14.2 Dateien (`/files`)

#### POST `/api/v1/files/upload`

**Beschreibung:**
Upload einer `.stl`- oder `.3mf`-Datei bis 50 MiB. Die Datei wird im Objektspeicher gespeichert und Metadaten werden in der Datenbank abgelegt.

**Rollen:** `uploader`, `admin`

**Request:**

* Multipart File Upload

**Response:**

* Datei-ID
* Dateiname
* Erfolgsmeldung

---

#### GET `/api/v1/files/all`

**Beschreibung:**
Gibt eine Liste aller hochgeladenen Dateien zurück.

**Rollen:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/unverified`

**Beschreibung:**
Listet alle Dateien, die noch nicht verifiziert wurden.

**Rollen:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/queued`

**Beschreibung:**
Gibt alle Dateien zurück, die sich in der Druck-Warteschlange befinden.

**Rollen:** `admin`, `downloader`, `verifier`

---

#### GET `/api/v1/files/me`

**Beschreibung:**
Gibt alle Dateien des aktuell eingeloggten Benutzers zurück.

**Rollen:** `uploader`, `admin`

---

#### GET `/api/v1/files/user/{user_id}`

**Beschreibung:**
Listet alle Dateien eines bestimmten Benutzers.

**Rollen:** `admin`

---

#### GET `/api/v1/files/{file_id}`

**Beschreibung:**
Gibt Metadaten einer einzelnen Datei zurück.

**Zugriff:** Dateieigentümer, `admin`, `verifier` oder `downloader`

**Parameter:**

* `file_id` (UUID)

---

#### GET `/api/v1/files/{file_id}/download`

**Beschreibung:**
Download der Originaldatei aus dem Objektspeicher.

**Zugriff:** Dateieigentümer, `admin`, `verifier` oder `downloader`

**Parameter:**

* `file_id` (UUID)

---

#### DELETE `/api/v1/files/{file_id}`

**Beschreibung:**
Löscht eine Datei inklusive Metadaten und gespeicherter Datei.

**Rollen:** `admin`

---

### 14.3 Verifikation (`/verifications`)

#### POST `/api/v1/verifications`

**Beschreibung:**
Gibt eine hochgeladene Datei frei oder lehnt sie ab. Die Freigabe erzeugt einen Auftrag in der Warteschlange; ein physischer Druck wird nicht gestartet.

**Rollen:** `verifier`, `admin`

**Request Body:**

* `file_id` (UUID)
* `status` (`approved` oder `rejected`)
* `comments` (optional)

---

### 14.4 Druckaufträge (`/prints`)

#### POST `/api/v1/prints`

**Beschreibung:**
Erstellt einen Auftrag in der Warteschlange für eine bereits freigegebene Datei ohne aktiven Auftrag.

**Rollen:** `admin`

**Request Body:**

* `model_file_id` (UUID)

---

#### GET `/api/v1/prints`

**Beschreibung:**
Gibt alle Druckaufträge im System zurück.

**Rollen:** `admin`

---

#### GET `/api/v1/prints/{job_id}`

**Beschreibung:**
Gibt Details zu einem bestimmten Druckauftrag zurück.

**Rollen:** `admin`

---

# 15 Umgebungsvariablen (.env Datei)

Zur Konfiguration des Systems wird eine .env-Datei verwendet. Diese enthält alle wichtigen Umgebungsvariablen für Datenbank, Backend, Authentifizierung und Dateispeicher. Sensible Informationen wie Passwörter oder Secrets werden dadurch nicht direkt im Quellcode gespeichert, was die Sicherheit und Wartbarkeit erhöht.

## 15.1 Datenbank-Konfiguration (PostgreSQL)

POSTGRES_USER\
Benutzername, mit dem sich das Backend bei der PostgreSQL-Datenbank anmeldet.

POSTGRES_PASSWORD\
Passwort für den Datenbankbenutzer.

POSTGRES_DB\
Name der Datenbank, in der alle Metadaten wie Benutzer, Rollen, Dateien und Druckaufträge gespeichert werden.

## 15.2 Backend-Konfiguration

DATABASE_URL\
Verbindungs-URL zur PostgreSQL-Datenbank. Sie enthält Benutzername, Passwort, Host, Port und Datenbankname und wird vom Backend für den Datenbankzugriff verwendet.

ADMIN_USER\
Bestehender LDAP-Benutzername, der beim Start die Administratorrolle erhält. Für die Anmeldung ist weiterhin dessen LDAP-Passwort nötig.

VERIFIER_USERS\
Optionale, durch Kommas getrennte Liste bestehender LDAP-Benutzernamen, die die Prüferrolle erhalten.

JWT_SECRET\
Geheimschlüssel zur Signierung und Validierung der JSON Web Tokens (JWT). Dieser Schlüssel stellt sicher, dass Authentifizierungs-Tokens nicht manipuliert werden können.

## 15.3 LDAP-Konfiguration

LDAP_SERVER\
IP-Adresse oder Hostname des schulischen LDAP-Servers, über den die Benutzer authentifiziert werden.

LDAP_DOMAIN\
Domäne der Schule, die für den Login mit Schulaccounts verwendet wird.

BASE_DN\
Optionale LDAP-Einstellung für Kompatibilität; die aktuelle Anmeldung verwendet sie nicht.

## 15.4 MinIO-Konfiguration (Dateispeicher)

MINIO_ENDPOINT\
Adresse des MinIO-Servers, über den die 3D-Modelldateien gespeichert und abgerufen werden.

MINIO_ACCESS_KEY\
Zugriffsschlüssel (Benutzername) für den MinIO-Objektspeicher.

MINIO_SECRET_KEY\
Geheimer Schlüssel (Passwort) für den Zugriff auf MinIO.

MINIO_BUCKET\
Name des Buckets, in dem alle hochgeladenen 3D-Modelldateien gespeichert werden.

MINIO_SECURE\
Gibt an, ob die Verbindung zu MinIO verschlüsselt (HTTPS) oder unverschlüsselt (HTTP) erfolgt. Im Entwicklungsbetrieb ist dies häufig auf False gesetzt.


# 16. Rollen-Bootstrap-Konfiguration

`ADMIN_USER` enthält einen bestehenden LDAP-Benutzernamen. `VERIFIER_USERS` kann weitere, durch Kommas getrennte LDAP-Benutzernamen enthalten. Das Backend weist diese Rollen beim Start zu. Es legt keine lokalen Passwörter an und verwendet `backend/role_bootstrap.yaml` nicht.




# 17. Docker-Setup – Entwicklungs- und Produktivumgebung

Für das Projekt werden **drei Docker-Compose-Dateien** verwendet:

* `docker-compose.yml` → **Produktiv-/Standardbetrieb**
* `docker-compose.dev.yml` → **Entwicklungsbetrieb mit Hot Reload**
* `docker-compose.traefik.yml` → **Gemeinsamer HTTPS-Reverse-Proxy**

Diese Trennung ermöglicht eine stabile Produktionsumgebung sowie eine komfortable Entwicklungsumgebung, in der Änderungen am Code automatisch übernommen werden.

---

## 17.1 Docker Compose – Produktivbetrieb (`docker-compose.yml`)

Die Datei `docker-compose.yml` definiert die Anwendungsdienste. Sie sind mit dem externen Netzwerk `traefik_proxy` verbunden; die Schritte zur Bereitstellung stehen in `README.md`.

### Backend

* FastAPI-Anwendung
* Build über ein Multi-Stage Dockerfile
* Interner Port **8000**; öffentliche API unter `/3DPrint/api/v1`
* Konfiguration über Umgebungsvariablen aus der `.env` Datei
* Abhängigkeiten:

  * PostgreSQL-Datenbank
  * MinIO-Objektspeicher

In dieser Variante wird **kein Hot Reload** verwendet, da sie für Stabilität und Performance optimiert ist.

---

### Frontend

* React-Anwendung mit Vite
* Build-Prozess erzeugt statische Dateien
* Auslieferung über **Nginx**
* Interner Port **3000**; öffentliches Frontend unter `/3DPrint/`

Diese Variante eignet sich für den Produktivbetrieb, da kein Entwicklungsserver läuft.

---

### PostgreSQL (Datenbank)

* Verwendet das offizielle Image `postgres:15`
* Persistente Speicherung über Docker Volume `pgdata`
* Zugangsdaten werden über Umgebungsvariablen gesetzt

---

### MinIO (Objektspeicher)

* S3-kompatibler Objektspeicher für 3D-Modelldateien
* Interne Ports (im Produktivbetrieb nicht auf dem Host veröffentlicht):

  * `9000` → API-Zugriff
  * `9001` → Web-Konsole
* Persistente Daten über Docker Volume `minio_data`

---

### Volumes

* `pgdata` → PostgreSQL-Daten
* `minio_data` → gespeicherte Dateien

---

## 17.2 Docker Compose – Entwicklungsbetrieb (`docker-compose.dev.yml`)

Die Datei `docker-compose.dev.yml` ist für die Entwicklung vorgesehen und aktiviert **Hot Reload** für Backend und Frontend.

---

### Backend (Development)

Unterschiede zum Produktivbetrieb:

* Verwendung von `Dockerfile.dev`
* Quellcode wird als Volume gemountet (`./backend:/app`)
* Start von `uvicorn` mit `--reload`
* Änderungen am Code führen zu einem automatischen Neustart des Servers

Dies ermöglicht eine schnelle Entwicklung ohne manuelles Neustarten.

---

### Frontend (Development)

* Verwendung von `Dockerfile.dev`
* Quellcode wird als Volume gemountet (`./frontend:/app`)
* Start des Vite Dev Servers
* Interner Port **5173**, nach außen weitergeleitet auf **3000**
* `CHOKIDAR_USEPOLLING=true` stellt sicher, dass Dateisystemänderungen erkannt werden

Änderungen im Frontend sind sofort im Browser sichtbar.

---

### Gemeinsame Services

PostgreSQL und MinIO verwenden in beiden Umgebungen dieselben Images und persistenten Volumes. Nur die Entwicklungsumgebung veröffentlicht die MinIO-Ports auf dem Host.

---

## 17.3 Dockerfiles – Übersicht

### Frontend (`Dockerfile`)

* Multi-Stage Build
* Node.js zum Bauen der Anwendung
* Nginx zur Auslieferung der statischen Dateien
* Optimiert für geringe Image-Größe und Performance

---

### Frontend (`Dockerfile.dev`)

* Node.js Image
* Startet den Vite Dev Server
* Code wird über Volume vom Host eingebunden
* Unterstützt Hot Reload

---

### Backend (`Dockerfile`)

* Multi-Stage Build
* Python-Abhängigkeiten werden vorinstalliert
* Start der FastAPI-Anwendung ohne Reload-Modus
* Geeignet für den Produktivbetrieb

---

### Backend (`Dockerfile.dev`)

* Einfaches Python-Image
* Quellcode wird über Volume eingebunden
* Start von `uvicorn` mit `--reload`
* Ideal für die Entwicklung

---
