import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { missions } from '../services/api';

function Missions() {
  const [allMissions, setAllMissions] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadMissions();
  }, [filter]);

  const loadMissions = async () => {
    try {
      const response = await missions.getAll(filter || undefined);
      setAllMissions(response.data);
    } catch (error) {
      console.error('Error loading missions:', error);
    }
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      pending: 'badge-warning',
      in_progress: 'badge-info',
      completed: 'badge-success',
      aborted: 'badge-danger',
    };
    return `badge ${statusColors[status] || 'badge-info'}`;
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 style={{ color: '#1e3a8a' }}>Missions</h2>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="btn btn-primary">
          <option value="">All Missions</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Mission Code</th>
              <th>Organ Type</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Distance</th>
              <th>Scheduled Start</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {allMissions.map(mission => (
              <tr key={mission.id}>
                <td><strong>{mission.mission_code}</strong></td>
                <td>{mission.organ_type}</td>
                <td>{mission.priority_level}</td>
                <td><span className={getStatusBadge(mission.status)}>{mission.status}</span></td>
                <td>{mission.distance_km} km</td>
                <td>{new Date(mission.scheduled_start).toLocaleString()}</td>
                <td>
                  <Link to={`/missions/${mission.id}`} className="btn btn-primary" style={{ fontSize: '0.875rem', padding: '0.25rem 0.75rem' }}>
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Missions;
