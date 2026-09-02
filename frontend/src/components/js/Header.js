import React from 'react';
import { AirVent } from 'lucide-react';
import '../css/Header.css';

const NAV_ITEMS = [
  { key: 'home', label: 'Home' },
  { key: 'charts', label: 'Charts' },
  { key: 'info', label: 'Info' },
];

const Header = ({ setActivePage, activePage }) => {
  return (
    <header className="main-header border-0 shadow-none">
      <nav className="navbar navbar-expand-lg navbar-light border-0 shadow-none p-0">
        <a
          className="navbar-brand"
          href="#home"
          onClick={(e) => { e.preventDefault(); setActivePage('home'); }}
        >
          <AirVent size={35} color="#a8dadc" /> Microclimate Data
        </a>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            {NAV_ITEMS.map((item) => (
              <li key={item.key} className={`nav-item ${activePage === item.key ? 'active' : ''}`}>
                <a
                  className="nav-link"
                  href={`#${item.key}`}
                  onClick={(e) => { e.preventDefault(); setActivePage(item.key); }}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    </header>
  );
};

export default Header;
