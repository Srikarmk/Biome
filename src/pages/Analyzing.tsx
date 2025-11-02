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

// Mock results for demonstration
const MOCK_RESULTS = {
  overallScore: 7.2,
  issues: [
    {
      type: "Knee Valgus",
      severity: "moderate",
      frameStart: 23,
      frameEnd: 45,
      cue: "Your right knee is collapsing inward 12°. Push both knees out to track over your toes.",
    },
    {
      type: "Insufficient Depth",
      severity: "minor",
      frameStart: 34,
      frameEnd: 56,
      cue: "You're stopping 5° above parallel. Sit back like reaching for a chair to achieve proper depth.",
    },
    {
      type: "Back Rounding",
      severity: "moderate",
      frameStart: 78,
      frameEnd: 92,
      cue: "Your spine is flexing 15° at the bottom. Keep your chest up and maintain your natural curve.",
    },
  ],
  strengths: [
    "Consistent tempo (good control)",
    "Balanced left/right symmetry",
    "Strong bracing throughout",
  ],
  metrics: {
    "Knee Angle (bottom)": { actual: "87°", target: "90°", status: "warning" },
    "Hip Angle (bottom)": { actual: "92°", target: "85-95°", status: "good" },
    "Back Angle": { actual: "18°", target: "<15°", status: "warning" },
    "Depth Achieved": { actual: "95%", target: "100%", status: "warning" },
    "Symmetry Score": { actual: "9.2/10", target: ">8/10", status: "good" },
  },
  recommendations: [
    "Strengthening glutes (knee stability)",
    "Ankle mobility drills",
    "Core bracing practice",
  ],
};

export default function Analyzing() {
  const location = useLocation();
  const navigate = useNavigate();
  const { video, exercise } = location.state;

  const [progress, setProgress] = useState(0);
  const [, setCurrentStep] = useState("uploading");
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    vision: "processing",
    coaching: "waiting",
  });

  const simulateAnalysis = useCallback(async () => {
    // Step 1: Upload
    setCurrentStep("uploading");
    await delay(1000);
    setProgress(10);

    // Step 2: Vision processing
    setCurrentStep("vision");
    setAgentStatus({ vision: "processing", coaching: "waiting" });

    for (let i = 10; i <= 60; i += 5) {
      await delay(500);
      setProgress(i);
    }

    setAgentStatus({ vision: "complete", coaching: "processing" });

    // Step 3: Coaching
    setCurrentStep("coaching");
    for (let i = 60; i <= 100; i += 10) {
      await delay(800);
      setProgress(i);
    }

    setAgentStatus({ vision: "complete", coaching: "complete" });

    // Navigate to results
    await delay(500);
    navigate("/results", {
      state: {
        exercise,
        results: MOCK_RESULTS,
      },
    });
  }, [navigate, exercise]);

  useEffect(() => {
    // Simulate analysis process (replace with actual API call)
    simulateAnalysis();
  }, [simulateAnalysis]);

  const delay = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const visionTasks: Task[] = [
    { name: "Extracting body landmarks", status: "complete" },
    { name: "Calculating joint angles", status: "complete" },
    { name: "Detecting deviations", status: agentStatus.vision },
  ];

  const coachingTasks: Task[] = [
    { name: "Analyzing with Gemini", status: agentStatus.coaching },
    { name: "Generating coaching cues", status: agentStatus.coaching },
  ];

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
