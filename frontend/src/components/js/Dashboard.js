import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Thermometer, Droplets, Wind, Calendar, Smile, Meh, Frown } from 'lucide-react';
import "../css/Dashboard.css";

function Dashboard() {
    const [data, setData] = useState([]);

    const getComfortLabel = (score) => {
        if (score === undefined || score === null) return '--';
        if (score < 20) return "Very low";
        if (score < 40) return "Low";
        if (score < 60) return "Medium";
        if (score < 75) return "High";
        return "Very high";
    };

    const getComfortStyle = (score) => {
        const label = getComfortLabel(score);

        switch (label) {
            case "Very low":
                return {
                    label: "Very low",
                    color: "#e63946",
                    Icon: Frown
                };
            case "Low":
                return {
                    label: "Low",
                    color: "#f4a261",
                    Icon: Frown
                };
            case "Medium":
                return {
                    label: "Medium",
                    color: "#ffb703",
                    Icon: Meh
                };
            case "High":
                return {
                    label: "High",
                    color: "#96ad20",
                    Icon: Smile
                };
            case "Very high":
                return {
                    label: "Very high",
                    color: "#2a9d8f",
                    Icon: Smile
                };
            default:
                return {
                    label: "--",
                    color: "#ffffff",
                    Icon: Smile
                };
        }
    };

    const formatDate = (timestamp) => {
        if (!timestamp) return '--';
        const date = new Date(timestamp);

        const datePart = date.toLocaleDateString('pl-PL', {
            day: '2-digit',
            month: '2-digit'
        });

        const timePart = date.toLocaleTimeString('pl-PL', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        return `${datePart}, ${timePart}`;
    };

    const fetchData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/measurements');
            setData(response.data);
        } catch (error) {
            console.error("Can not connect to backend: ", error);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, []);

    const recentReadings = data.slice(0, 3);

    return (
        <div className='dashboard-content m-5'>
            <div className="dashboard-container container my-5">
                <h1 className="text-center mb-2">Latest Microclimate Data</h1>
                <p className="text-center text-muted mb-5">
                    Status: <span className={data.length > 0 ? "text-success fw-bold" : "text-warning"}>
                        {data.length > 0 ? "Connected" : "Waiting for data..."}
                    </span>
                </p>

                <div className="row g-4 justify-content-center">
                    {recentReadings.map((reading, index) => {
                        const comfortStyle = getComfortStyle(reading.comfort_score);
                        const ComfortIcon = comfortStyle.Icon;

                        return (
                            <div key={reading.id || index} className="col-12 col-md-4">
                                <div className={`card h-100 shadow-sm p-4 border-2 ${index === 0 ? 'border-primary' : 'border-light'}`}>

                                    <div className="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
                                        <span className="badge bg-secondary">
                                            {index === 0 ? "Latest" : index === 1 ? "Previous" : "Older"}
                                        </span>
                                        <div className="d-flex align-items-center text-muted gap-1" style={{ fontSize: '0.9rem' }}>
                                            <Calendar size={16} />
                                            <span>{formatDate(reading.timestamp)}</span>
                                        </div>
                                    </div>

                                    <div className="d-flex flex-column gap-3">
                                        <div className="d-flex align-items-center justify-content-between bg-light p-2 rounded">
                                            <div className="d-flex align-items-center gap-2">
                                                <Thermometer size={24} color="#e63946" />
                                                <span className="fw-semibold">Temperature</span>
                                            </div>
                                            <span className="fs-5 fw-bold">{reading.temperature} °C</span>
                                        </div>

                                        <div className="d-flex align-items-center justify-content-between bg-light p-2 rounded">
                                            <div className="d-flex align-items-center gap-2">
                                                <Droplets size={24} color="#457b9d" />
                                                <span className="fw-semibold">Humidity</span>
                                            </div>
                                            <span className="fs-5 fw-bold">{reading.humidity} %</span>
                                        </div>

                                        <div className="d-flex align-items-center justify-content-between bg-light p-2 rounded">
                                            <div className="d-flex align-items-center gap-2">
                                                <Wind size={24} color="#2a9d8f" />
                                                <span className="fw-semibold">CO2 Level</span>
                                            </div>
                                            <span className="fs-5 fw-bold">{reading.co2} ppm</span>
                                        </div>

                                        <div className="d-flex align-items-center justify-content-between bg-dark text-white p-3 rounded mt-2">
                                            <div className="d-flex align-items-center gap-2">
                                                <ComfortIcon size={24} color={comfortStyle.color} />
                                                <span className="fw-semibold">Comfort</span>
                                            </div>
                                            <div className="text-end">
                                                <div className="fs-5 fw-bold">{reading.comfort_score} %</div>
                                                <small className="fw-bold" style={{ fontSize: '0.75rem', color: comfortStyle.color }}>
                                                    {comfortStyle.label}
                                                </small>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>
                        );
                    })}

                    {recentReadings.length === 0 && (
                        <div className="text-center col-12 py-5 text-muted">
                            No measurements found in database.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;