import { Link } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  return (
    <div className="navbar">
      <h1>Organ Transport Drone System</h1>
      <nav>
        <Link to="/">Dashboard</Link>
        <Link to="/missions">Missions</Link>
        <Link to="/alerts">Alerts</Link>
        {user.role === 'admin' && <Link to="/admin">Admin</Link>}
      </nav>
      <div>
        <span style={{ marginRight: '1rem' }}>{user.full_name} ({user.role})</span>
        <button onClick={onLogout}>Logout</button>
      </div>
    </div>
  );
}

export default Navbar;
