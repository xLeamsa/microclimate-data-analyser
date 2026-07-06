import React, { useState } from 'react';
import Header from './Header';
import Footer from './Footer';
import Dashboard from './Dashboard';
import '../css/App.css';
import Charts from './Charts';

function App() {
  const [activePage, setActivePage] = useState('home');

  return (
    <div>
      <Header setActivePage={setActivePage} activePage={activePage} />

      <main>
        {activePage === 'home' && <Dashboard />}
        {activePage === 'charts' && <Charts />}
      </main>

      <Footer />
    </div>
  );
}

export default App;