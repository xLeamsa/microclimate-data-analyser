import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Dashboard from './Dashboard';
import '../css/App.css';

function App() {
  return (
    <div>
      <Header />

      <main>
        <Dashboard />
      </main>

      <Footer />
    </div>

  );
}

export default App;