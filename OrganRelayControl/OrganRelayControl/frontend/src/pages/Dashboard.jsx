import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import { missions, drones } from '../services/api';
import wsService from '../services/websocket';
import 'leaflet/dist/leaflet.css';

function Dashboard() {
  const [activeMissions, setActiveMissions] = useState([]);
  const [allDrones, setAllDrones] = useState([]);
  const [realtimeTelemetry, setRealtimeTelemetry] = useState({});
  const [realtimeAlerts, setRealtimeAlerts] = useState([]);

  useEffect(() => {
    loadData();
    wsService.connect();
    wsService.addListener(handleWebSocketMessage);
    
    return () => {
      wsService.removeListener(handleWebSocketMessage);
    };
  }, []);

  const loadData = async () => {
    try {
      const [missionsRes, dronesRes] = await Promise.all([
        missions.getAll('in_progress'),
        drones.getAll(),
      ]);
      setActiveMissions(missionsRes.data);
      setAllDrones(dronesRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleWebSocketMessage = (data) => {
    if (data.type === 'telemetry') {
      setRealtimeTelemetry(prev => ({
        ...prev,
        [data.mission_id]: data
      }));
    } else if (data.type === 'alert') {
      setRealtimeAlerts(prev => [data, ...prev].slice(0, 10));
    }
  };

  const center = [40.7589, -73.9851];

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem', color: '#1e3a8a' }}>Mission Dashboard</h2>
      
      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-label">Active Missions</div>
          <div className="stat-value">{activeMissions.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Drones</div>
          <div className="stat-value">{allDrones.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Recent Alerts</div>
          <div className="stat-value" style={{ color: realtimeAlerts.length > 0 ? '#ef4444' : '#10b981' }}>
            {realtimeAlerts.length}
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">System Status</div>
          <div className="stat-value" style={{ color: '#10b981', fontSize: '1.5rem' }}>
            Operational
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Live Mission Map</h3>
        <div className="map-container">
          <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {allDrones.map(drone => (
              drone.current_latitude && drone.current_longitude && (
                <Marker 
                  key={drone.id} 
                  position={[drone.current_latitude, drone.current_longitude]}
                >
                  <Popup>
                    <strong>{drone.serial_number}</strong><br />
                    Status: {drone.current_status}<br />
                    Battery: {drone.current_battery}%
                  </Popup>
                </Marker>
              )
            ))}
            {activeMissions.map(mission => {
              try {
                const route = JSON.parse(mission.planned_route);
                return (
                  <Polyline 
                    key={mission.id}
                    positions={route}
                    color="blue"
                    weight={3}
                  />
                );
              } catch (e) {
                return null;
              }
            })}
          </MapContainer>
        </div>
      </div>

      {realtimeAlerts.length > 0 && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h3>Recent Alerts</h3>
          <div className="alert-list">
            {realtimeAlerts.map((alert, idx) => (
              <div key={idx} className={`alert-item ${alert.severity}`}>
                <strong>{alert.alert_type}</strong> - {alert.message}
                <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
                  {new Date(alert.timestamp).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
