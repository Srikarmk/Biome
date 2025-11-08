import { useState, useEffect, useCallback } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

interface AgentStatus {
  vision: "waiting" | "processing" | "complete";
  coaching: "waiting" | "processing" | "complete";
}

interface Task {
  name: string;
  status: "waiting" | "processing" | "complete";
}

interface AgentCardProps {
  name: string;
  icon: string;
  status: "waiting" | "processing" | "complete";
  tasks: Task[];
}

function AgentCard({ name, icon, status, tasks }: AgentCardProps) {
  const statusIcon = {
    waiting: "⏸️",
    processing: "⏳",
    complete: "✓",
  };

  const statusColor = {
    waiting: "border-gray-600",
    processing: "border-primary-500",
    complete: "border-success",
  };

  return (
    <div
      className={`bg-surface border-2 ${statusColor[status]} rounded-xl p-6`}
    >
      <h3 className="text-xl font-semibold text-text mb-4 flex items-center">
        <span className="text-2xl mr-3">{icon}</span>
        {name}
        <span className="ml-auto text-lg">{statusIcon[status]}</span>
      </h3>
      <ul className="space-y-2">
        {tasks.map((task, i) => (
          <li key={i} className="flex items-center text-text-secondary">
            <span className="mr-3">{statusIcon[task.status]}</span>
            {task.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

// Real analysis - mock data removed since backend is working

// API URL - defaults to local backend at port 8000
// For Cloud Run deployment, set REACT_APP_API_URL to your backend URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Analyzing() {
  const location = useLocation();
  const navigate = useNavigate();
  const { video, exercise, videoUrl } = location.state || {};

  const [progress, setProgress] = useState(0);
  const [, setCurrentStep] = useState("uploading");
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    vision: "processing",
    coaching: "waiting",
  });
  const [error, setError] = useState<string | null>(null);

  const delay = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const performRealAnalysis = useCallback(async () => {
    try {
      setCurrentStep("uploading");
      setProgress(10);
      setAgentStatus({ vision: "processing", coaching: "waiting" });

      // Create FormData with video
      const formData = new FormData();
      
      // Convert blob to file if needed
      let videoFile: File;
      if (video instanceof Blob && !(video instanceof File)) {
        videoFile = new File([video], "workout.webm", { type: video.type });
      } else {
        videoFile = video as File;
      }
      
      formData.append("video", videoFile);
      formData.append("exercise_name", exercise);
      formData.append("user_id", "demo_user");

      setProgress(20);

      // Call backend API
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }));
        throw new Error(errorData.error || errorData.detail?.error || "Analysis failed");
      }

      setProgress(60);
      setAgentStatus({ vision: "complete", coaching: "processing" });

      const results = await response.json();

      setProgress(100);
      setAgentStatus({ vision: "complete", coaching: "complete" });

      // Navigate to results with real data
      await delay(500);
      navigate("/results", {
        state: {
          exercise,
          videoUrl,
          results: {
            overallScore: results.overall_score,
            issues: results.issues.map((issue: any) => ({
              type: issue.issue_type,
              severity: issue.severity,
              frameStart: issue.frame_start,
              frameEnd: issue.frame_end,
              cue: issue.coaching_cue,
            })),
            strengths: results.strengths,
            metrics: results.metrics.reduce((acc: any, m: any) => {
              acc[m.metric_name] = {
                actual: m.actual_value,
                target: m.target_value,
                status: m.status,
              };
              return acc;
            }, {}),
            recommendations: results.recommendations.map((r: any) => r.recommendation_text),
          },
        },
      });
    } catch (error) {
      console.error("Analysis error:", error);
      setError(error instanceof Error ? error.message : "Unknown error occurred");
      setAgentStatus({ vision: "waiting", coaching: "waiting" });
    }
  }, [navigate, exercise, video, videoUrl]);

  // Simulation removed - using real API analysis only

  useEffect(() => {
    // Use real analysis instead of simulation
    if (video && exercise) {
      performRealAnalysis();
    }
  }, [performRealAnalysis, video, exercise]);

  const visionTasks: Task[] = [
    { name: "Extracting body landmarks", status: "complete" },
    { name: "Calculating joint angles", status: "complete" },
    { name: "Detecting deviations", status: agentStatus.vision },
  ];

  const coachingTasks: Task[] = [
    { name: "Analyzing with Gemini", status: agentStatus.coaching },
    { name: "Generating coaching cues", status: agentStatus.coaching },
  ];

  // Handle missing state (after all hooks)
  if (!video || !exercise) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center">
        <Navbar />
        <div className="text-center px-4">
          <h1 className="text-3xl font-bold text-text mb-4">Missing Video</h1>
          <p className="text-text-secondary mb-8">
            Please upload a video to analyze.
          </p>
          <button
            onClick={() => navigate("/analyze")}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-text mb-4">
            Analyzing Your {exercise}...
          </h1>
          <p className="text-xl text-text-secondary">
            Our AI agents are working hard to analyze your form
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-8 bg-red-500/10 border-2 border-red-500 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-red-500 mb-2">Analysis Failed</h3>
            <p className="text-text-secondary mb-4">{error}</p>
            <div className="flex gap-4">
              <button
                onClick={() => navigate("/upload")}
                className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Try Again
              </button>
              <button
                onClick={() => navigate("/analyze")}
                className="border border-gray-600 hover:border-gray-500 text-text px-4 py-2 rounded-lg transition-colors"
              >
                Start Over
              </button>
            </div>
          </div>
        )}

        {/* Video Preview with Skeleton Overlay */}
        <div className="bg-surface rounded-xl p-8 mb-8">
          <div className="relative">
            <video
              src={URL.createObjectURL(video)}
              autoPlay
              muted
              loop
              className="w-full rounded-lg"
            />
            {/* Skeleton overlay placeholder */}
            <div className="absolute inset-0 bg-black/20 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <div className="text-4xl mb-2">🦴</div>
                <p className="text-white font-semibold">
                  Analyzing pose landmarks...
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="bg-surface rounded-xl p-8 mb-8">
          <div className="text-center mb-6">
            <p className="text-text-secondary mb-2">
              Processing frame {Math.floor(progress * 1.2)} of 120...
            </p>
            <div className="w-full bg-gray-700 rounded-full h-3 mb-2">
              <div
                className="bg-gradient-to-r from-primary-500 to-accent-500 h-3 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-text font-semibold text-lg">{progress}%</p>
          </div>
        </div>

        {/* Agent Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <AgentCard
            name="Vision Agent"
            icon="👁️"
            status={agentStatus.vision}
            tasks={visionTasks}
          />

          <AgentCard
            name="Coaching Agent"
            icon="🧠"
            status={agentStatus.coaching}
            tasks={coachingTasks}
          />
        </div>

        {/* Fun Facts */}
        <div className="bg-gradient-to-r from-primary-500/10 to-accent-500/10 border border-primary-500/20 rounded-xl p-8">
          <h3 className="text-xl font-semibold text-text mb-4">
            💡 Did you know?
          </h3>
          <p className="text-text-secondary text-lg">
            Proper squat form reduces knee injury risk by 40% according to
            sports science research.
          </p>
        </div>
      </div>
    </div>
  );
}
