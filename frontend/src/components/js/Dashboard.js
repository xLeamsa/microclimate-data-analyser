import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Thermometer, Droplets, Wind, Calendar, Smile, Meh, Frown, WifiOff, BellRing, BellOff, AlertTriangle } from 'lucide-react';
import { API_BASE_URL, apiRequestConfig } from './apiConfig';
import { requestNotificationPermission, sendNotification } from './notifications';
import { getComfortAdvice } from './comfortAdvice';
import '../css/Dashboard.css';

const COMFORT_STYLES = {
  'Very low': { color: '#e63946', Icon: Frown },
  Low: { color: '#f4a261', Icon: Frown },
  Medium: { color: '#ffb703', Icon: Meh },
  High: { color: '#96ad20', Icon: Smile },
  'Very high': { color: '#2a9d8f', Icon: Smile },
};

const BAD_COMFORT_LABELS = ['Very low', 'Low'];
const ALERT_COOLDOWN_MS = 15 * 60 * 1000;
const POLL_INTERVAL_MS = 5000;
const NOTIFICATIONS_MUTED_KEY = 'notificationsMuted';

function loadNotificationsMuted() {
  try {
    return localStorage.getItem(NOTIFICATIONS_MUTED_KEY) === 'true';
  } catch (error) {
    return false;
  }
}

function getComfortLabel(score) {
  if (score === undefined || score === null) return '--';
  if (score < 20) return 'Very low';
  if (score < 40) return 'Low';
  if (score < 60) return 'Medium';
  if (score < 75) return 'High';
  return 'Very high';
}

function getComfortStyle(score) {
  const label = getComfortLabel(score);
  const style = COMFORT_STYLES[label];
  return style ? { label, ...style } : { label: '--', color: '#ffffff', Icon: Smile };
}

function formatDate(timestamp) {
  if (!timestamp) return '--';
  const date = new Date(timestamp);
  const datePart = date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit' });
  const timePart = date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  return `${datePart}, ${timePart}`;
}

function Dashboard() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState({ online: true, last_seen: null });
  const [notifPermission, setNotifPermission] = useState(
    'Notification' in window ? Notification.permission : 'unsupported'
  );
  const [notificationsMuted, setNotificationsMuted] = useState(loadNotificationsMuted);

  const lastAlertLabelRef = useRef(null);
  const lastAlertTimeRef = useRef(0);
  const wasOnlineRef = useRef(true);
  const notificationsMutedRef = useRef(notificationsMuted);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/measurements`, apiRequestConfig);
      setData(response.data);

      const latest = response.data[0];
      if (latest) {
        const label = getComfortLabel(latest.comfort_score);
        const now = Date.now();
        const isBad = BAD_COMFORT_LABELS.includes(label);

        if (isBad && (label !== lastAlertLabelRef.current || now - lastAlertTimeRef.current > ALERT_COOLDOWN_MS)) {
          if (!notificationsMutedRef.current) {
            const advice = getComfortAdvice(latest.temperature, latest.humidity, latest.co2);
            sendNotification(
              `Comfort is ${label.toLowerCase()}`,
              advice.length > 0 ? advice.join(' ') : 'Check the room conditions.'
            );
          }
          lastAlertLabelRef.current = label;
          lastAlertTimeRef.current = now;
        } else if (!isBad) {
          lastAlertLabelRef.current = null;
        }
      }
    } catch (error) {
      console.error('Cannot connect to backend:', error);
    }
  };

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/status`, apiRequestConfig);
      setStatus(response.data);

      if (!notificationsMutedRef.current) {
        if (wasOnlineRef.current && !response.data.online) {
          sendNotification(
            'Sensor offline',
            `No new data since ${formatDate(response.data.last_seen)} - showing last known readings.`
          );
        } else if (!wasOnlineRef.current && response.data.online) {
          sendNotification('Sensor back online', 'Receiving fresh readings again.');
        }
      }
      wasOnlineRef.current = response.data.online;
    } catch (error) {
      console.error('Cannot fetch sensor status:', error);
    }
  };

  useEffect(() => {
    fetchData();
    fetchStatus();
    const interval = setInterval(() => {
      fetchData();
      fetchStatus();
    }, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    notificationsMutedRef.current = notificationsMuted;
    try {
      localStorage.setItem(NOTIFICATIONS_MUTED_KEY, String(notificationsMuted));
    } catch (error) {
      // ignore - browser storage not available
    }
  }, [notificationsMuted]);

  const handleEnableNotifications = () => {
    requestNotificationPermission();
    setTimeout(() => {
      if ('Notification' in window) setNotifPermission(Notification.permission);
    }, 500);
  };

  const handleToggleNotifications = () => {
    setNotificationsMuted((muted) => !muted);
  };

  const recentReadings = data.slice(0, 3);
  const readingLabels = ['Latest', 'Previous', 'Older'];
  const isOffline = data.length > 0 && !status.online;

  return (
    <div className="dashboard-content m-5">
      <div className="dashboard-container container my-5">
        <h1 className="text-center mb-2">Latest Microclimate Data</h1>

        <div className="text-center mb-4">
          <p className="mb-1">
            Status:{' '}
            {data.length === 0 && <span className="text-warning fw-bold">Waiting for data...</span>}
            {data.length > 0 && !isOffline && <span className="text-success fw-bold">Connected</span>}
            {isOffline && (
              <span className="text-danger fw-bold d-inline-flex align-items-center gap-1">
                <WifiOff size={16} /> Offline - showing last known readings
              </span>
            )}
          </p>

          {notifPermission === 'default' && (
            <button
              type="button"
              className="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1 mt-2"
              onClick={handleEnableNotifications}
            >
              <BellRing size={14} /> Enable desktop notifications
            </button>
          )}

          {notifPermission === 'granted' && (
            <button
              type="button"
              className="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1 mt-2"
              onClick={handleToggleNotifications}
            >
              {notificationsMuted ? (
                <>
                  <BellOff size={14} /> Notifications off - click to enable
                </>
              ) : (
                <>
                  <BellRing size={14} /> Notifications on - click to disable
                </>
              )}
            </button>
          )}

          {notifPermission === 'denied' && (
            <p className="text-muted mt-2" style={{ fontSize: '0.85rem' }}>
              Desktop notifications are blocked - allow them for this site in your browser settings to enable them.
            </p>
          )}
        </div>

        <div className="row g-4 justify-content-center">
          {recentReadings.map((reading, index) => {
            const comfortStyle = getComfortStyle(reading.comfort_score);
            const ComfortIcon = comfortStyle.Icon;
            const advice =
              index === 0 && BAD_COMFORT_LABELS.includes(comfortStyle.label)
                ? getComfortAdvice(reading.temperature, reading.humidity, reading.co2)
                : [];

            return (
              <div key={reading.id || index} className="col-12 col-md-4">
                <div className={`card h-100 shadow-sm p-4 border-2 ${index === 0 ? 'border-primary' : 'border-light'}`}>
                  <div className="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom">
                    <span className="badge bg-secondary">{readingLabels[index]}</span>
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

                    {advice.length > 0 && (
                      <div className="p-2 rounded" style={{ backgroundColor: '#fff3cd' }}>
                        <div className="d-flex align-items-center gap-2 mb-1">
                          <AlertTriangle size={16} color="#e63946" />
                          <span className="fw-semibold" style={{ fontSize: '0.85rem' }}>What to change</span>
                        </div>
                        {advice.map((line) => (
                          <div key={line} style={{ fontSize: '0.8rem' }} className="text-muted">
                            {line}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}

          {recentReadings.length === 0 && (
            <div className="text-center col-12 py-5 text-muted">No measurements found in database.</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;