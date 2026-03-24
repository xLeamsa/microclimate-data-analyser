import React from 'react';
import { ArrowBigDown } from 'lucide-react';
import { AirVent } from 'lucide-react'
import "../css/Header.css"

const Header = () => {
    return (
        <header className="main-header">
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <a className="navbar-brand" href="#"><AirVent size={35} color="#a8dadc" /> Microclimate data</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item active">
                            <a className="nav-link" href="#">Home </a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="#">Charts</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="#">Info</a>
                        </li>
                    </ul>
                </div>
            </nav>
        </header>

    );
};

export default Header;