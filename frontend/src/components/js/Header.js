import React from 'react';
import { AirVent } from 'lucide-react';
import "../css/Header.css";

const Header = ({ setActivePage, activePage }) => {
    return (
        <header className="main-header border-0 shadow-none">
            <nav className="navbar navbar-expand-lg navbar-light border-0 shadow-none p-0">
                <a
                    className="navbar-brand"
                    href="#home"
                    onClick={(e) => { e.preventDefault(); setActivePage('home'); }}
                >
                    <AirVent size={35} color="#a8dadc" /> Microclimate data
                </a>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className={`nav-item ${activePage === 'home' ? 'active' : ''}`}>
                            <a
                                className="nav-link"
                                href="#home"
                                onClick={(e) => { e.preventDefault(); setActivePage('home'); }}
                            >
                                Home
                            </a>
                        </li>

                        <li className={`nav-item ${activePage === 'charts' ? 'active' : ''}`}>
                            <a
                                className="nav-link"
                                href="#charts"
                                onClick={(e) => { e.preventDefault(); setActivePage('charts'); }}
                            >
                                Charts
                            </a>
                        </li>

                        <li className={`nav-item ${activePage === 'info' ? 'active' : ''}`}>
                            <a
                                className="nav-link"
                                href="#info"
                                onClick={(e) => { e.preventDefault(); setActivePage('info'); }}
                            >
                                Info
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </header>
    );
};

export default Header;