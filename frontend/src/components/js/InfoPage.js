import React from 'react';
import { Cpu, Wifi, Gauge, Thermometer, Droplets, Wind } from 'lucide-react';
import '../css/Dashboard.css';

function InfoPage() {
  return (
    <div className="dashboard-content m-5">
      <div className="dashboard-container container my-5">
        <h1 className="text-center mb-2">About This System</h1>
        <p className="text-center text-muted mb-5">
          A quick guide to what you're looking at and how it works.
        </p>

        <div className="card shadow-sm p-4 border-0 mb-4">
          <h4 className="mb-3">What is this?</h4>
          <p className="mb-0">
            This dashboard shows the temperature, humidity and air quality of a monitored room in
            real time. A small sensor device in the room measures the conditions automatically and
            sends new readings roughly every minute, so what you see here is always up to date.
          </p>
        </div>

        <div className="card shadow-sm p-4 border-0 mb-4">
          <h4 className="mb-3">Understanding the Comfort Score</h4>
          <p className="mb-0">
            Instead of checking three separate numbers, the Comfort Score combines temperature,
            humidity and CO2 level into a single, easy-to-read rating — from Very Low to Very
            High — so you can tell at a glance whether the room is pleasant to be in.
          </p>
        </div>

        <div className="row g-4 mb-4">
          <div className="col-12 col-md-4">
            <div className="card shadow-sm p-4 border-0 h-100">
              <div className="d-flex align-items-center gap-2 mb-2">
                <Thermometer size={24} color="#e63946" />
                <h5 className="mb-0">Temperature</h5>
              </div>
              <p className="mb-0 text-muted">Most people feel comfortable between roughly 20-24°C.</p>
            </div>
          </div>

          <div className="col-12 col-md-4">
            <div className="card shadow-sm p-4 border-0 h-100">
              <div className="d-flex align-items-center gap-2 mb-2">
                <Droplets size={24} color="#457b9d" />
                <h5 className="mb-0">Humidity</h5>
              </div>
              <p className="mb-0 text-muted">A healthy range is around 40-60%. Too dry or too humid both feel uncomfortable.</p>
            </div>
          </div>

          <div className="col-12 col-md-4">
            <div className="card shadow-sm p-4 border-0 h-100">
              <div className="d-flex align-items-center gap-2 mb-2">
                <Wind size={24} color="#2a9d8f" />
                <h5 className="mb-0">CO2 Level</h5>
              </div>
              <p className="mb-0 text-muted">Below ~800 ppm means the room is well ventilated. Above ~1500 ppm, it's time to open a window.</p>
            </div>
          </div>
        </div>

        <div className="card shadow-sm p-4 border-0">
          <h4 className="mb-3">How it works</h4>
          <div className="d-flex flex-column gap-3">
            <div className="d-flex align-items-center gap-3">
              <Cpu size={22} color="#a8dadc" />
              <span>A small sensor device in the room measures temperature, humidity and CO2.</span>
            </div>
            <div className="d-flex align-items-center gap-3">
              <Wifi size={22} color="#a8dadc" />
              <span>Readings are sent securely over the internet to this application every minute.</span>
            </div>
            <div className="d-flex align-items-center gap-3">
              <Gauge size={22} color="#a8dadc" />
              <span>The app calculates the Comfort Score and shows it here, and trends over time on the Charts page.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InfoPage;
