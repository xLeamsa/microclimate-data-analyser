import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { Calendar } from 'lucide-react';
import { API_BASE_URL, apiRequestConfig } from './apiConfig';
import '../css/Charts.css';

const COLORS = {
  temperature: '#e63946',
  humidity: '#457b9d',
  co2: '#2a9d8f',
  comfort: '#9a2fff',
};

function Charts() {
  const [historyData, setHistoryData] = useState([]);
  const [timeRange, setTimeRange] = useState('1d');

  const fetchHistory = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/measurements/history?range=${timeRange}`,
        apiRequestConfig
      );
      const formattedData = response.data.map((item) => ({
        ...item,
        displayTime: new Date(item.timestamp).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }),
      }));
      setHistoryData(formattedData);
    } catch (error) {
      console.error('Error fetching history data:', error);
    }
  };

  useEffect(() => {
    fetchHistory();
    const interval = setInterval(fetchHistory, 60000);
    return () => clearInterval(interval);
  }, [timeRange]);

  return (
    <div className="container-fluid px-4 my-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Microclimate History Charts</h2>

        <div className="d-flex align-items-center gap-2">
          <Calendar size={20} className="text-muted" />
          <select
            className="form-select time-range-select"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>

      <div className="row g-4 mb-4">
        <div className="col-12 col-md-4">
          <div className="card shadow-sm p-3 border-0 h-100">
            <h5 className="mb-3 text-muted">Temperature (°C)</h5>
            <div className="chart-container-small">
              <ResponsiveContainer>
                <AreaChart data={historyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" className="gradient-temp-stop-top" stopOpacity={0.2} />
                      <stop offset="95%" className="gradient-temp-stop-bottom" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="displayTime" />
                  <YAxis
                    stroke={COLORS.temperature}
                    domain={[
                      (dataMin) => Math.min(20, Math.floor(dataMin)),
                      (dataMax) => Math.max(40, Math.ceil(dataMax)),
                    ]}
                  />
                  <Tooltip />
                  <Area type="monotone" dataKey="temperature" name="Temp" stroke={COLORS.temperature} fillOpacity={1} fill="url(#colorTemp)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card shadow-sm p-3 border-0 h-100">
            <h5 className="mb-3 text-muted">Humidity (%)</h5>
            <div className="chart-container-small">
              <ResponsiveContainer>
                <AreaChart data={historyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorHum" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" className="gradient-hum-stop-top" stopOpacity={0.2} />
                      <stop offset="95%" className="gradient-hum-stop-bottom" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="displayTime" />
                  <YAxis stroke={COLORS.humidity} domain={[0, 100]} />
                  <Tooltip />
                  <Area type="monotone" dataKey="humidity" name="Hum" stroke={COLORS.humidity} fillOpacity={1} fill="url(#colorHum)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card shadow-sm p-3 border-0 h-100">
            <h5 className="mb-3 text-muted">CO2 Level (ppm)</h5>
            <div className="chart-container-small">
              <ResponsiveContainer>
                <AreaChart data={historyData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorCo2" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" className="gradient-co2-stop-top" stopOpacity={0.2} />
                      <stop offset="95%" className="gradient-co2-stop-bottom" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="displayTime" />
                  <YAxis stroke={COLORS.co2} domain={['auto', 'auto']} />
                  <Tooltip />
                  <Area type="monotone" dataKey="co2" name="CO2" stroke={COLORS.co2} fillOpacity={1} fill="url(#colorCo2)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm p-4 border-0">
        <h4 className="mb-3 text-muted">Comfort Level Index</h4>
        <div className="chart-container-large">
          <ResponsiveContainer>
            <AreaChart data={historyData}>
              <defs>
                <linearGradient id="colorComfort" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" className="gradient-comfort-stop-top" stopOpacity={0.3} />
                  <stop offset="95%" className="gradient-comfort-stop-bottom" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="displayTime" />
              <YAxis domain={[0, 100]} stroke={COLORS.comfort} />
              <Tooltip />
              <Area type="monotone" dataKey="comfort_score" name="Comfort Score (%)" stroke={COLORS.comfort} fillOpacity={1} fill="url(#colorComfort)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default Charts;
