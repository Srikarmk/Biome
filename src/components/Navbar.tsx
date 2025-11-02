import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-surface border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🧬</span>
            <span className="text-xl font-bold text-text">Biome</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link
              to="/how-it-works"
              className="text-text-secondary hover:text-text transition-colors duration-200"
            >
              How It Works
            </Link>
            <Link
              to="/analyze"
              className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
            >
              Try It Free
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
