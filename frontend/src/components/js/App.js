import React, { useState } from 'react';
import Header from './Header';
import Footer from './Footer';
import Dashboard from './Dashboard';
import Charts from './Charts';
import InfoPage from './InfoPage';
import '../css/App.css';

function App() {
  const [activePage, setActivePage] = useState('home');

  return (
    <div>
      <Header setActivePage={setActivePage} activePage={activePage} />

      <main>
        {activePage === 'home' && <Dashboard />}
        {activePage === 'charts' && <Charts />}
        {activePage === 'info' && <InfoPage />}
      </main>

      <Footer />
    </div>
  );
}

export default App;
