export default function Footer() {
  return (
    <footer className="bg-surface border-t border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="footer-section">
            <h4 className="text-lg font-semibold text-text mb-4">Biome</h4>
            <p className="text-text-secondary">
              AI-powered form coaching for everyone
            </p>
          </div>

          <div className="footer-section">
            <h4 className="text-lg font-semibold text-text mb-4">Technology</h4>
            <ul className="space-y-2">
              <li className="text-text-secondary">Google ADK</li>
              <li className="text-text-secondary">MediaPipe</li>
              <li className="text-text-secondary">Gemini 2.0</li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="text-lg font-semibold text-text mb-4">Resources</h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="/how-it-works"
                  className="text-text-secondary hover:text-text transition-colors"
                >
                  How It Works
                </a>
              </li>
              <li>
                <a
                  href="/about"
                  className="text-text-secondary hover:text-text transition-colors"
                >
                  About
                </a>
              </li>
              <li>
                <a
                  href="https://github.com"
                  className="text-text-secondary hover:text-text transition-colors"
                >
                  GitHub
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-text-secondary">
            Built with ❤️ for Google ADK Hackathon 2025
          </p>
        </div>
      </div>
    </footer>
  );
}
