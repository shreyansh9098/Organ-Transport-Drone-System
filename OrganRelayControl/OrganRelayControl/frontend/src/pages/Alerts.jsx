import { useState, useEffect } from 'react';
import { alerts } from '../services/api';

function Alerts() {
  const [allAlerts, setAllAlerts] = useState([]);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const response = await alerts.getAll();
      setAllAlerts(response.data);
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem', color: '#1e3a8a' }}>Alert Center</h2>

      <div className="card">
        <h3>All Alerts</h3>
        <div className="alert-list">
          {allAlerts.map((alert) => (
            <div key={alert.id} className={`alert-item ${alert.severity}`}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <strong>{alert.alert_type}</strong> - {alert.message}
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
                    Mission ID: {alert.mission_id} | {new Date(alert.created_at).toLocaleString()}
                  </div>
                </div>
                {alert.is_resolved && (
                  <span className="badge badge-success">Resolved</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Alerts;
