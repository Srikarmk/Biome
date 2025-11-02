import { useLocation, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import VideoPlayer from "../components/VideoPlayer";

interface Issue {
  type: string;
  severity: "severe" | "moderate" | "minor";
  frameStart: number;
  frameEnd: number;
  cue: string;
}

interface Metric {
  actual: string;
  target: string;
  status: "good" | "warning" | "error";
}

interface AnalysisResults {
  overallScore: number;
  issues: Issue[];
  strengths: string[];
  metrics: Record<string, Metric>;
  recommendations: string[];
}

function IssueCard({ issue }: { issue: Issue }) {
  const severityConfig = {
    severe: { icon: "🔴", color: "border-red-500 bg-red-500/10" },
    moderate: { icon: "⚠️", color: "border-yellow-500 bg-yellow-500/10" },
    minor: { icon: "⚡", color: "border-blue-500 bg-blue-500/10" },
  };

  const config = severityConfig[issue.severity];

  return (
    <div className={`border-2 ${config.color} rounded-xl p-6 mb-4`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-text flex items-center">
          <span className="text-xl mr-2">{config.icon}</span>
          {issue.type} ({issue.severity})
        </h3>
        <span className="text-text-secondary text-sm">
          Frame: {issue.frameStart}-{issue.frameEnd}
        </span>
      </div>

      <div className="bg-surface rounded-lg p-4 mb-4">
        <p className="text-text-secondary">💬 {issue.cue}</p>
      </div>

      <div className="flex space-x-3">
        <button className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          View Frame
        </button>
        <button className="border border-gray-600 hover:border-gray-500 text-text px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          Learn More
        </button>
      </div>
    </div>
  );
}

function MetricCard({ name, value }: { name: string; value: Metric }) {
  const statusConfig = {
    good: { icon: "✓", color: "text-success" },
    warning: { icon: "⚠️", color: "text-warning" },
    error: { icon: "❌", color: "text-error" },
  };

  const config = statusConfig[value.status];

  return (
    <div className="bg-surface rounded-lg p-4">
      <h4 className="text-text font-medium mb-2">{name}</h4>
      <p className={`text-lg font-semibold ${config.color} mb-1`}>
        {value.actual} {config.icon}
      </p>
      <p className="text-text-secondary text-sm">Target: {value.target}</p>
    </div>
  );
}

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Safely extract state with fallback
  const { exercise, results, videoUrl } = location.state || {};

  // Handle missing state (e.g., direct navigation or refresh)
  if (!exercise || !results) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center">
        <Navbar />
        <div className="text-center px-4">
          <h1 className="text-3xl font-bold text-text mb-4">No Results Found</h1>
          <p className="text-text-secondary mb-8">
            It looks like you navigated here directly. Please upload and analyze a video first.
          </p>
          <button
            onClick={() => navigate("/analyze")}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  const { overallScore, issues, strengths, metrics, recommendations } = results;

  const getScoreEmoji = (score: number) => {
    if (score >= 8) return "✅";
    if (score >= 6) return "⚠️";
    return "🔴";
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return "text-success";
    if (score >= 6) return "text-warning";
    return "text-error";
  };

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <h1 className="text-4xl font-bold text-text">
            {exercise} Form Analysis
          </h1>
          <button
            onClick={() => navigate("/analyze")}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            Analyze Another
          </button>
        </div>

        {/* Video Player with Markers */}
        {videoUrl && (
          <div className="mb-12">
            <VideoPlayer
              videoUrl={videoUrl}
              markers={issues.map((i) => ({
                time: i.frameStart / 30,
                type: i.severity,
              }))}
            />
          </div>
        )}

        {/* Overall Score */}
        <div className="bg-surface rounded-xl p-8 mb-12">
          <h2 className="text-2xl font-semibold text-text mb-6">
            Overall Form Quality
          </h2>
          <div className="flex items-center justify-center mb-6">
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <span
                  className={`text-6xl font-bold ${getScoreColor(
                    overallScore
                  )}`}
                >
                  {overallScore}
                </span>
                <span className="text-3xl text-text-secondary ml-2">/10</span>
                <span className="text-4xl ml-4">
                  {getScoreEmoji(overallScore)}
                </span>
              </div>
              <div className="w-80 bg-gray-700 rounded-full h-4">
                <div
                  className={`h-4 rounded-full transition-all duration-1000 ${
                    overallScore >= 8
                      ? "bg-success"
                      : overallScore >= 6
                      ? "bg-warning"
                      : "bg-error"
                  }`}
                  style={{ width: `${overallScore * 10}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Issues Detected */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-text mb-8">
            🔴 Issues Detected ({issues.length})
          </h2>
          {issues.map((issue, i) => (
            <IssueCard key={i} issue={issue} />
          ))}
        </section>

        {/* Strengths */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-text mb-6">
            ✅ What You Did Well
          </h2>
          <div className="bg-surface rounded-xl p-8">
            <ul className="space-y-3">
              {strengths.map((strength, i) => (
                <li key={i} className="flex items-start">
                  <span className="text-success mr-3 mt-1">•</span>
                  <span className="text-text-secondary text-lg">
                    {strength}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Detailed Metrics */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-text mb-8">
            📊 Detailed Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(metrics).map(([key, value]) => (
              <MetricCard key={key} name={key} value={value} />
            ))}
          </div>
        </section>

        {/* Recommendations */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-text mb-6">Next Steps</h2>
          <div className="bg-surface rounded-xl p-8">
            <p className="text-text-secondary text-lg mb-6">
              Based on your analysis, focus on:
            </p>
            <ol className="space-y-3">
              {recommendations.map((rec, i) => (
                <li key={i} className="flex items-start">
                  <span className="bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold mr-4 mt-1">
                    {i + 1}
                  </span>
                  <span className="text-text-secondary text-lg">{rec}</span>
                </li>
              ))}
            </ol>
            <div className="flex space-x-4 mt-8">
              <button className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                Get Corrective Exercises
              </button>
              <button className="border border-gray-600 hover:border-gray-500 text-text px-6 py-3 rounded-lg font-semibold transition-colors">
                Track Progress
              </button>
            </div>
          </div>
        </section>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4">
          <button className="bg-surface hover:bg-gray-700 text-text px-6 py-3 rounded-lg font-semibold transition-colors flex items-center">
            📥 Download Report
          </button>
          <button className="bg-surface hover:bg-gray-700 text-text px-6 py-3 rounded-lg font-semibold transition-colors flex items-center">
            📤 Share Results
          </button>
          <button
            onClick={() => navigate("/analyze")}
            className="bg-surface hover:bg-gray-700 text-text px-6 py-3 rounded-lg font-semibold transition-colors flex items-center"
          >
            ↻ Try Again
          </button>
        </div>
      </div>
    </div>
  );
}
