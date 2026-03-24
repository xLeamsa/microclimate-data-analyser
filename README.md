# SmartAir IoT - Microclimate Monitoring System

## Overview
This project is an integrated IoT solution designed for real-time monitoring of indoor microclimate conditions. The system collects data on temperature, humidity, and CO2 levels using sensors connected to a microcontroller, processes the information via a Python-based backend, and visualizes it through a modern, responsive web dashboard built with React.

## Tech Stack
- **Frontend:** React.js, Bootstrap 5 (Styling), Lucide-React (Icons), Axios (API calls).
- **Backend:** Python (Flask framework), REST API.
- **Database:** MySQL.
- **Hardware/Communication:** MQTT protocol for sensor data transmission.

## Key Features
- **Real-time Dashboard:** Instant visualization of current environmental parameters using intuitive sensor cards.
- **Responsive Design:** Fully accessible on different-sized screens thanks to Bootstrap integration.
- **Live Data Streaming:** Automatic data polling from the backend every 5 seconds to ensure up-to-date information.
- **Modular Architecture:** Clear separation of concerns between the API (Backend) and the User Interface (Frontend).

## Project Structure
- `/frontend`: React source code, components, and styles.
- `/backend`: Python scripts for API endpoints and database management.
- `/docs`: Project documentation and architecture diagrams.

To set up the database, import the `microclimate_db.sql` file into your MySQL server