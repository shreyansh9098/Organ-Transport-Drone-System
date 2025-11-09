import { useState, useEffect } from 'react';
import { drones, hospitals, users } from '../services/api';

function Admin() {
  const [allDrones, setAllDrones] = useState([]);
  const [allHospitals, setAllHospitals] = useState([]);
  const [allUsers, setAllUsers] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [dronesRes, hospitalsRes, usersRes] = await Promise.all([
        drones.getAll(),
        hospitals.getAll(),
        users.getAll(),
      ]);
      setAllDrones(dronesRes.data);
      setAllHospitals(hospitalsRes.data);
      setAllUsers(usersRes.data);
    } catch (error) {
      console.error('Error loading admin data:', error);
    }
  };

  return (
    <div className="container">
      <h2 style={{ marginBottom: '2rem', color: '#1e3a8a' }}>Admin Panel</h2>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3>Drones Management</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Serial Number</th>
              <th>Model</th>
              <th>Max Range</th>
              <th>Battery</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {allDrones.map(drone => (
              <tr key={drone.id}>
                <td><strong>{drone.serial_number}</strong></td>
                <td>{drone.model}</td>
                <td>{drone.max_range_km} km</td>
                <td>{drone.current_battery}%</td>
                <td><span className={`badge ${drone.is_active ? 'badge-success' : 'badge-danger'}`}>
                  {drone.is_active ? 'Active' : 'Inactive'}
                </span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3>Hospitals</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Address</th>
              <th>Contact</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {allHospitals.map(hospital => (
              <tr key={hospital.id}>
                <td><strong>{hospital.name}</strong></td>
                <td>{hospital.address}</td>
                <td>{hospital.contact_phone}</td>
                <td><span className={`badge ${hospital.is_active ? 'badge-success' : 'badge-danger'}`}>
                  {hospital.is_active ? 'Active' : 'Inactive'}
                </span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Users</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {allUsers.map(user => (
              <tr key={user.id}>
                <td><strong>{user.username}</strong></td>
                <td>{user.full_name}</td>
                <td>{user.email}</td>
                <td><span className="badge badge-info">{user.role}</span></td>
                <td><span className={`badge ${user.is_active ? 'badge-success' : 'badge-danger'}`}>
                  {user.is_active ? 'Active' : 'Inactive'}
                </span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Admin;
