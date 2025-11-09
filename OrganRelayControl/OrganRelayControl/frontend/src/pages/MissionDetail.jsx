import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { missions } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function MissionDetail() {
  const { id } = useParams();
  const [mission, setMission] = useState(null);
  const [telemetry, setTelemetry] = useState([]);
  const [missionAlerts, setMissionAlerts] = useState([]);

  useEffect(() => {
    loadMissionData();
  }, [id]);

  const loadMissionData = async () => {
    try {
      const [missionRes, telemetryRes, alertsRes] = await Promise.all([
        missions.getById(id),
        missions.getTelemetry(id),
        missions.getAlerts(id),
      ]);
      setMission(missionRes.data);
      setTelemetry(telemetryRes.data.reverse());
      setMissionAlerts(alertsRes.data);
    } catch (error) {
      console.error('Error loading mission data:', error);
    }
  };

  if (!mission) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem', color: '#1e3a8a' }}>Mission Details: {mission.mission_code}</h2>

      <div className="dashboard-grid">
        <div className="card">
          <h3>Mission Info</h3>
          <p><strong>Organ Type:</strong> {mission.organ_type}</p>
          <p><strong>Priority:</strong> {mission.priority_level}</p>
          <p><strong>Status:</strong> {mission.status}</p>
          <p><strong>Distance:</strong> {mission.distance_km} km</p>
        </div>

        <div className="card">
          <h3>Temperature Range</h3>
          <p><strong>Min:</strong> {mission.temperature_min}°C</p>
          <p><strong>Max:</strong> {mission.temperature_max}°C</p>
        </div>

        <div className="card">
          <h3>Schedule</h3>
          <p><strong>Scheduled:</strong> {new Date(mission.scheduled_start).toLocaleString()}</p>
          {mission.actual_start && (
            <p><strong>Started:</strong> {new Date(mission.actual_start).toLocaleString()}</p>
          )}
        </div>

        <div className="card">
          <h3>Alerts</h3>
          <div className="stat-value" style={{ color: missionAlerts.length > 0 ? '#ef4444' : '#10b981' }}>
            {missionAlerts.length}
          </div>
        </div>
      </div>

      {telemetry.length > 0 && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h3>Telemetry Charts</h3>
          <div style={{ height: 300, marginBottom: '2rem' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetry}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" tickFormatter={(time) => new Date(time).toLocaleTimeString()} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="temperature_celsius" stroke="#ef4444" name="Temperature (°C)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetry}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" tickFormatter={(time) => new Date(time).toLocaleTimeString()} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="battery_percentage" stroke="#10b981" name="Battery %" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {missionAlerts.length > 0 && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h3>Mission Alerts</h3>
          <div className="alert-list">
            {missionAlerts.map((alert) => (
              <div key={alert.id} className={`alert-item ${alert.severity}`}>
                <strong>{alert.alert_type}</strong> - {alert.message}
                <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
                  {new Date(alert.created_at).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default MissionDetail;
