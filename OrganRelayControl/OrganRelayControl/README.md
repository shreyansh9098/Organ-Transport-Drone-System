# Autonomous Organ Transportation Drone System

A full-stack application for monitoring and managing autonomous drones transporting medical organs with real-time telemetry tracking, IoT integration, AI route optimization, and blockchain-based audit logs.

## Features

### Core Functionality
- **JWT Authentication** with role-based access control (Admin, Hospital User, Drone Operator, Emergency Controller)
- **Real-time Mission Dashboard** with live GPS tracking using Leaflet maps
- **WebSocket Integration** for real-time telemetry updates (GPS, altitude, speed, battery, temperature)
- **IoT Telemetry Ingestion APIs** for drone sensor data and temperature logs
- **Automated Alert System** for temperature deviation, low battery, route drift, and geofence violations
- **Mock AI Route Optimization** considering weather conditions, no-fly zones, and emergency priority
- **Mock Blockchain Ledger** with hash chaining for immutable telemetry and alert log storage

### Admin Panel
- Manage drones, users, hospitals, missions
- Configure temperature threshold settings
- View mission history, violations, and alerts
- Monitor system-wide statistics

### Dashboard Features
- **Live Map**: Interactive map showing drone positions and mission routes
- **Telemetry Widgets**: Real-time display of altitude, speed, battery, temperature
- **Interactive Charts**: Historical telemetry data visualization using Recharts
- **Alert Center**: Real-time alerts for critical conditions
- **Mission Management**: Create, monitor, and track missions

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for PostgreSQL
- **PostgreSQL** - Primary database
- **PyJWT** - JWT authentication
- **WebSockets** - Real-time communication
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Navigation
- **Leaflet** - Interactive maps
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **WebSocket API** - Real-time updates

## Prerequisites

- Python 3.11
- Node.js 20
- PostgreSQL database (provided by Replit)

## Local Setup Instructions

### 1. Environment Setup

The following environment variables are already configured in the Replit environment:

**Database Connection:**
- `DATABASE_URL` - PostgreSQL connection string
- `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` - Database credentials

**Security:**
- `SESSION_SECRET` - JWT signing secret (already configured for security)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (already installed via uv)
# Dependencies are managed in the project's virtual environment

# Seed the database with sample data
python seed_data.py

# The backend will automatically start via the configured workflow
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (already installed)
# npm install

# The frontend will automatically start via the configured workflow
```

## Running the Application

The application uses configured workflows that automatically start both backend and frontend:

- **Backend**: Runs on `http://localhost:8000`
- **Frontend**: Runs on `http://localhost:5000`

Both services start automatically when you open the project.

### Manual Start (if needed)

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Default User Credentials

The system comes with pre-seeded user accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Hospital User | hospital1 | hospital123 |
| Drone Operator | operator1 | operator123 |
| Emergency Controller | emergency | emergency123 |

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Key API Endpoints

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user

**Missions:**
- `GET /api/missions` - List all missions
- `POST /api/missions` - Create new mission
- `GET /api/missions/{id}` - Get mission details
- `PUT /api/missions/{id}/start` - Start a mission
- `GET /api/missions/{id}/telemetry` - Get mission telemetry
- `GET /api/missions/{id}/alerts` - Get mission alerts

**Drones:**
- `GET /api/drones` - List all drones
- `POST /api/drones` - Create new drone (Admin only)
- `PUT /api/drones/{id}` - Update drone

**Telemetry (IoT):**
- `POST /api/telemetry` - Ingest telemetry data from drones

**Real-time:**
- `WS /ws` - WebSocket endpoint for real-time updates

**Route Optimization:**
- `POST /api/route/optimize` - Optimize route using AI module

**Blockchain:**
- `GET /api/missions/{id}/blockchain` - Get blockchain ledger for mission
- `GET /api/missions/{id}/blockchain/verify` - Verify blockchain integrity

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── auth.py              # JWT authentication and authorization
│   ├── database.py          # Database connection and session
│   ├── blockchain.py        # Mock blockchain implementation
│   ├── ai_optimizer.py      # Mock AI route optimization
│   ├── seed_data.py         # Database seeding script
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   │   └── Navbar.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Missions.jsx
│   │   │   ├── MissionDetail.jsx
│   │   │   ├── Alerts.jsx
│   │   │   └── Admin.jsx
│   │   ├── services/        # API and WebSocket services
│   │   │   ├── api.js
│   │   │   └── websocket.js
│   │   ├── App.jsx          # Main application component
│   │   ├── main.jsx         # Application entry point
│   │   └── index.css        # Global styles
│   ├── index.html
│   ├── vite.config.js       # Vite configuration
│   └── package.json
│
└── README.md
```

## Features in Detail

### 1. Authentication & Authorization
- JWT-based authentication
- Four user roles with different permissions
- Secure password hashing with bcrypt
- Protected API endpoints

### 2. Real-time Telemetry
- WebSocket connection for live updates
- Automatic alert generation on threshold violations
- Real-time dashboard updates
- Historical telemetry data storage

### 3. Alert System
Monitors and alerts for:
- **Temperature Deviation**: Organ temperature outside safe range (2-8°C)
- **Low Battery**: Battery below 20% (critical if below 10%)
- **Route Drift**: Deviation from planned route
- **Geofence Violation**: Entry into restricted airspace

### 4. AI Route Optimization
Mock AI module that considers:
- Weather conditions (clear, cloudy, rain, storm, fog)
- No-fly zones (restricted airspace)
- Emergency priority levels
- Distance optimization
- Safety scoring

### 5. Blockchain Ledger
- Immutable audit trail for telemetry data
- Hash chaining for data integrity
- Verification system for blockchain validity
- Stores both telemetry and alert events

### 6. Mission Management
- Create missions with organ type, priority, and schedule
- Automatic route optimization
- Real-time mission tracking
- Mission history and analytics

## Database Schema

### Main Tables
- **users** - User accounts with roles
- **hospitals** - Hospital locations and contact info
- **drones** - Drone specifications and current status
- **missions** - Mission details and status
- **telemetry** - Real-time drone sensor data
- **alerts** - System-generated alerts
- **blockchain_ledger** - Immutable audit logs
- **system_settings** - System configuration

## Sample Data

The system includes pre-seeded data:
- **4 Users** (one for each role)
- **4 Hospitals** in New York area
- **3 Drones** with different capabilities
- **3 Missions** (completed, in-progress, pending)
- **Sample telemetry data**
- **Sample alerts**

## Development Notes

### No Deployment Configuration
This application is configured for **local development only**. No deployment settings or production configurations are included.

### Testing the System

1. **Login** with any of the default credentials
2. **View Dashboard** to see live map and statistics
3. **Check Missions** to view mission history and details
4. **Monitor Alerts** in the alert center
5. **Admin Panel** (admin user only) to manage system resources

### Mock Components

The following are mock implementations for demonstration:
- **AI Route Optimizer**: Uses algorithms to simulate route optimization
- **Blockchain**: Implements hash chaining but is not a distributed ledger
- **Weather Data**: Uses predefined weather conditions

### WebSocket Real-time Updates

The system broadcasts real-time updates for:
- New telemetry data points
- Alert generation
- Mission status changes

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- Role-based access control for sensitive operations
- Environment variables for sensitive configuration
- `.gitignore` configured to exclude `.env` files

## Browser Compatibility

The frontend is optimized for modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Backend won't start
- Check PostgreSQL connection via `DATABASE_URL` environment variable
- Verify all Python dependencies are installed
- Check backend logs for specific errors

### Frontend won't start
- Ensure Node.js 20 is installed
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and run `npm install`

### WebSocket connection fails
- Ensure backend is running on port 8000
- Check browser console for WebSocket errors
- Verify proxy configuration in `vite.config.js`

### Map not displaying
- Check browser console for Leaflet errors
- Ensure Leaflet CSS is loaded
- Verify hospital/drone coordinates are valid

## License

This is a demonstration project created for educational purposes.

## Support

For issues or questions about running this application locally, please check:
1. Environment variable configuration
2. Database connection status
3. Backend and frontend logs
4. Browser developer console

---

**Note**: This application is designed to run locally and does not include deployment configuration, production optimizations, or external service integrations.
