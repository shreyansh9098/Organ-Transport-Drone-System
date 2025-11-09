# Autonomous Organ Transportation Drone System

## Overview
A full-stack, real-time monitoring and management platform designed for autonomous drones transporting medical organs. The system offers live telemetry, AI-powered route optimization, IoT sensor integration, automated critical condition alerts, and a mock blockchain-based audit trail for immutable logging. It supports role-based access control for Admin, Hospital User, Drone Operator, and Emergency Controller roles. The platform is fully implemented and operational, with both backend and frontend running successfully.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Authentication & Authorization
Uses JWT-based authentication with `python-jose` (HS256) and `Bcrypt` for password hashing. Role-based access control (RBAC) is implemented for four distinct roles. Authentication tokens are stored in `localStorage` on the frontend and managed via Axios interceptors.

### Backend Architecture
Built with `FastAPI` for high-performance async APIs, `SQLAlchemy` with `PostgreSQL` for data persistence, and `Uvicorn` for deployment. Features WebSocket support for real-time communication and a modular service layer for concerns like authentication, mock blockchain, and AI route optimization.

### Frontend Architecture
Developed with `React`, `Vite` for fast development, `React Router` for navigation, and `Axios` for HTTP requests. It uses a component-based architecture with dedicated services for API and WebSocket interactions. `Vite` is configured to proxy API and WebSocket requests to the backend. Key pages include Login, Dashboard, Missions, MissionDetail, Alerts, and Admin.

### Real-Time Communication
A `WebSocket` connection, managed by a singleton `WebSocketService`, provides real-time updates. It uses an event listener pattern, automatic reconnection, and a backend broadcast mechanism for pushing data to connected clients via a JSON-based message protocol.

### Data Visualization
`Leaflet maps` (via `react-leaflet`) are used for interactive GPS tracking and route visualization. `Recharts` provides historical telemetry charts (altitude, speed, battery, temperature), with all widgets updating in real-time from WebSocket data.

### Mock AI Route Optimization
Utilizes the `Haversine formula` for distance calculations, includes `no-fly zone detection` via geofencing, and incorporates `weather condition scoring` for route desirability. This modular design allows for future integration with advanced ML-based optimization.

### Mock Blockchain Ledger
Implements `SHA-256 hash chaining` for immutable telemetry log entries, creating a verifiable audit trail for each mission without reliance on external blockchain networks.

### Alert System
Automated alerts are generated for deviations in temperature, low battery, route drift, and geofence violations. Alerts have severity levels (Low, Medium, High, Critical) and are broadcast in real-time via WebSocket, also being logged to the blockchain.

### Database Schema Design
A normalized `PostgreSQL` schema includes tables for Users, Hospitals, Drones, Missions, Telemetry, Alerts, BlockchainLedger, and SystemSettings, with foreign key relationships ensuring data integrity.

## External Dependencies

### Backend Dependencies (Python)
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `sqlalchemy`: ORM for PostgreSQL
- `psycopg2-binary`: PostgreSQL adapter
- `pydantic`, `pydantic-settings`: Data validation and settings
- `python-jose`: JWT handling
- `passlib`: Password hashing
- `websockets`: WebSocket protocol
- `python-dotenv`: Environment variables
- `email-validator`: Email validation

### Frontend Dependencies (Node.js)
- `react`, `react-dom`: UI library
- `react-router-dom`: Client-side routing
- `axios`: HTTP client
- `leaflet`, `react-leaflet`: Mapping libraries
- `recharts`: Charting library
- `socket.io-client`: WebSocket client
- `vite`, `@vitejs/plugin-react`: Build tool

### Database
- `PostgreSQL`: Primary relational database, configured via `DATABASE_URL` and other environment variables.

### Third-Party Service Integration Points (Future/Mocked)
- **Weather API**: For real-time meteorological data.
- **FAA API**: For official no-fly zone boundaries.
- **SMS/Email gateway**: For alert notifications.
- **Blockchain network**: For production audit trails.
- **IoT platform**: For scalable drone telemetry ingestion.