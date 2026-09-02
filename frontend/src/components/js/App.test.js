import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the app header brand', () => {
  render(<App />);
  const brandElement = screen.getByText(/microclimate data/i);
  expect(brandElement).toBeInTheDocument();
});

test('renders navigation links', () => {
  render(<App />);
  expect(screen.getByText(/home/i)).toBeInTheDocument();
  expect(screen.getByText(/charts/i)).toBeInTheDocument();
});
