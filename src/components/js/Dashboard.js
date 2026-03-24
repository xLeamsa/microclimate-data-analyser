import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Thermometer, Droplets, Wind } from 'lucide-react';
import "../css/Dashboard.css"

function Dashboard() {
    const [data, setData] = useState([]);

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

    const latest = data[0] || { temperature: '--', humidity: '--', co2: '--' };

    return (
        <div className="dashboard-content">
            <h1>Latest microclimate data</h1>
            <p>
                Status: {data.length > 0 ? "Connected" : "Waiting for data..."}
            </p>

            <div>
                <div>
                    <Thermometer size={32} color="#e63946" />
                    <h3>Temperature</h3>
                    <div className="value">{latest.temperature} °C</div>
                </div>

                <div>
                    <Droplets size={32} color="#457b9d" />
                    <h3>Humidity</h3>
                    <div className="value">{latest.humidity} %</div>
                </div>

                <div>
                    <Wind size={32} color="#2a9d8f" />
                    <h3>CO2 Level</h3>
                    <div className="value">{latest.co2} ppm</div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;