# Biome Frontend - Complete Page Structure

**Total Pages: 6**  
**Tech Stack:** React + TypeScript (optional) + React Router  
**Design:** Clean, modern, fitness-focused

---

## Page Overview

1. **Landing Page** - Hook visitors
2. **How It Works** - Explain the magic
3. **Exercise Selection** - Choose what to analyze
4. **Upload/Record** - Submit video
5. **Analysis** - Processing with real-time updates
6. **Results** - Coaching feedback and insights

---

## 1. Landing Page (`/`)

### Purpose
Make a strong first impression, get users excited, direct them to try it

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]              [Try It] [About]    │ ← Navbar
├─────────────────────────────────────────────────┤
│                                                 │
│          Hero Section                           │
│     ┌───────────────────────┐                  │
│     │  🎥 Video Preview     │                  │
│     │  (Demo of system)     │                  │
│     └───────────────────────┘                  │
│                                                 │
│      YOUR AI FITNESS COACH                      │
│      Real-time form coaching for ANY exercise   │
│                                                 │
│      [Start Analyzing] [See How It Works]       │
│                                                 │
├─────────────────────────────────────────────────┤
│          Features Section                       │
│                                                 │
│   🎯 Universal          👁️ Real-time         💪 Expert  │
│   Works for any         Sees your form        AI coaching│
│   exercise             instantly             powered by  │
│                                              Gemini      │
│                                                 │
├─────────────────────────────────────────────────┤
│          Supported Exercises                    │
│                                                 │
│  [Squat] [Push-up] [Deadlift] [Plank]         │
│  [Lunge] [Pull-up] [+ 100 more...]            │
│                                                 │
├─────────────────────────────────────────────────┤
│          CTA Section                            │
│                                                 │
│      Ready to improve your form?                │
│      [Analyze My Form Now]                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/Landing.tsx
export default function Landing() {
  return (
    <div className="landing-page">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <ExerciseShowcase />
      <CTASection />
      <Footer />
    </div>
  );
}
```

### Content
```jsx
// HeroSection.tsx
<section className="hero">
  <div className="hero-video">
    {/* Demo video or animated GIF showing system in action */}
    <video autoPlay loop muted playsInline>
      <source src="/demo-loop.mp4" type="video/mp4" />
    </video>
  </div>
  
  <h1>Your AI Fitness Coach</h1>
  <p>Get real-time form coaching for any exercise. 
     No equipment. No subscription. Just better movement.</p>
  
  <div className="cta-buttons">
    <button className="primary" onClick={() => navigate('/analyze')}>
      Start Analyzing
    </button>
    <button className="secondary" onClick={() => navigate('/how-it-works')}>
      See How It Works
    </button>
  </div>
  
  <div className="social-proof">
    <p>✨ Powered by Google Gemini & MediaPipe</p>
  </div>
</section>
```

### Styling Notes
- Big, bold hero text
- Gradient background (fitness theme: blue → purple or orange → red)
- Smooth animations on scroll
- Mobile-first responsive

---

## 2. How It Works Page (`/how-it-works`)

### Purpose
Explain the technology, build credibility, show it's not magic

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]         [Back] [Try It Now]      │
├─────────────────────────────────────────────────┤
│                                                 │
│           How Biome Works                       │
│                                                 │
│   Three-step process to perfect form            │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Step 1: Vision Agent                          │
│  ┌──────────────────────────┐                  │
│  │  📹 → 🤖 → 📊             │                  │
│  │  Video  AI   Metrics     │                  │
│  └──────────────────────────┘                  │
│                                                 │
│  Our Vision Agent uses MediaPipe to extract     │
│  33 body landmarks and calculate biomechanics:  │
│  • Joint angles (knee, hip, elbow, etc.)       │
│  • Left/right symmetry                         │
│  • Movement stability                          │
│  • Posture alignment                           │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Step 2: Coaching Agent                        │
│  ┌──────────────────────────┐                  │
│  │  📊 → 🧠 → 💬             │                  │
│  │  Data  Gemini  Cue       │                  │
│  └──────────────────────────┘                  │
│                                                 │
│  Your biomechanics + exercise name goes to      │
│  Google Gemini, which interprets the data and   │
│  generates specific, actionable coaching cues.  │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Step 3: You Improve                           │
│  ┌──────────────────────────┐                  │
│  │  💬 → 👤 → 📈             │                  │
│  │  Cue  You  Better        │                  │
│  └──────────────────────────┘                  │
│                                                 │
│  Get instant feedback, fix your form, and       │
│  build better movement patterns over time.      │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  The Technology Behind Biome                    │
│                                                 │
│  [Google ADK]  [MediaPipe]  [Gemini 2.0]       │
│   Agentic AI    Pose         Reasoning         │
│   Architecture  Detection    Engine            │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Ready to try it?                               │
│  [Analyze Your Form]                            │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/HowItWorks.tsx
export default function HowItWorks() {
  return (
    <div className="how-it-works-page">
      <Navbar />
      
      <section className="hero">
        <h1>How Biome Works</h1>
        <p>AI-powered form coaching in three steps</p>
      </section>
      
      <ProcessStep 
        number={1}
        title="Vision Agent Analyzes"
        icon="👁️"
        description="MediaPipe extracts 33 body landmarks and calculates biomechanics"
        details={[
          "Joint angles (knee, hip, elbow)",
          "Left/right symmetry",
          "Movement stability",
          "Posture alignment"
        ]}
        visual={<SkeletonVisualization />}
      />
      
      <ProcessStep 
        number={2}
        title="Coaching Agent Reasons"
        icon="🧠"
        description="Gemini interprets your biomechanics and generates coaching"
        details={[
          "Understands 100+ exercises",
          "Context-aware feedback",
          "Safety-first recommendations"
        ]}
        visual={<GeminiPromptDemo />}
      />
      
      <ProcessStep 
        number={3}
        title="You Improve"
        icon="💪"
        description="Get instant, actionable feedback to perfect your form"
        details={[
          "Real-time corrections",
          "Track progress over time",
          "Build better habits"
        ]}
      />
      
      <TechStack />
      <CTASection />
    </div>
  );
}
```

---

## 3. Exercise Selection Page (`/analyze`)

### Purpose
User specifies what exercise they're doing

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]                    [Back Home]   │
├─────────────────────────────────────────────────┤
│                                                 │
│        What exercise are you doing?             │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  🔍 Search exercises...                  │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│          Popular Exercises                      │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  Squat  │  │ Push-up │  │Deadlift │        │
│  └─────────┘  └─────────┘  └─────────┘        │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  Plank  │  │  Lunge  │  │ Pull-up │        │
│  └─────────┘  └─────────┘  └─────────┘        │
│                                                 │
│          All Exercises (A-Z)                    │
│                                                 │
│  Upper Body  |  Lower Body  |  Core  | Other   │
│  ─────────────────────────────────────────     │
│  • Bench Press    • Box Jump    • Crunch       │
│  • Bicep Curl     • Bulgarian   • Plank        │
│  • Dip              Split                       │
│  • Overhead Press • Calf Raise                 │
│  ...more                                       │
│                                                 │
│          Or type your own                       │
│  ┌─────────────────────────────────────────┐   │
│  │  Custom exercise name...                 │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│            [Continue to Upload]                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/ExerciseSelection.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const POPULAR_EXERCISES = [
  { id: 'squat', name: 'Squat', icon: '🏋️' },
  { id: 'pushup', name: 'Push-up', icon: '💪' },
  { id: 'deadlift', name: 'Deadlift', icon: '⚡' },
  { id: 'plank', name: 'Plank', icon: '🧘' },
  { id: 'lunge', name: 'Lunge', icon: '🦵' },
  { id: 'pullup', name: 'Pull-up', icon: '🔝' },
];

const EXERCISE_CATEGORIES = {
  'Upper Body': ['Bench Press', 'Overhead Press', 'Bicep Curl', 'Tricep Dip'],
  'Lower Body': ['Squat', 'Deadlift', 'Lunge', 'Calf Raise', 'Box Jump'],
  'Core': ['Plank', 'Crunch', 'Russian Twist', 'Leg Raise'],
  'Other': ['Burpee', 'Jump Rope', 'Mountain Climber']
};

export default function ExerciseSelection() {
  const [selectedExercise, setSelectedExercise] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleContinue = () => {
    if (selectedExercise) {
      // Store in state or context
      localStorage.setItem('selectedExercise', selectedExercise);
      navigate('/upload');
    }
  };

  return (
    <div className="exercise-selection-page">
      <Navbar />
      
      <div className="container">
        <h1>What exercise are you doing?</h1>
        
        {/* Search Bar */}
        <div className="search-bar">
          <input
            type="text"
            placeholder="🔍 Search exercises..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        {/* Popular Exercises */}
        <section className="popular-exercises">
          <h2>Popular</h2>
          <div className="exercise-grid">
            {POPULAR_EXERCISES.map(ex => (
              <button
                key={ex.id}
                className={`exercise-card ${selectedExercise === ex.name ? 'selected' : ''}`}
                onClick={() => setSelectedExercise(ex.name)}
              >
                <span className="icon">{ex.icon}</span>
                <span className="name">{ex.name}</span>
              </button>
            ))}
          </div>
        </section>
        
        {/* All Exercises by Category */}
        <section className="all-exercises">
          <h2>All Exercises</h2>
          <div className="category-tabs">
            {Object.keys(EXERCISE_CATEGORIES).map(cat => (
              <button key={cat} className="tab">{cat}</button>
            ))}
          </div>
          <div className="exercise-list">
            {/* Show exercises based on selected category */}
          </div>
        </section>
        
        {/* Custom Input */}
        <section className="custom-exercise">
          <h2>Or type your own</h2>
          <input
            type="text"
            placeholder="e.g., Downward Dog, Turkish Get-up"
            value={selectedExercise}
            onChange={(e) => setSelectedExercise(e.target.value)}
          />
        </section>
        
        {/* Continue Button */}
        <button 
          className="continue-btn"
          disabled={!selectedExercise}
          onClick={handleContinue}
        >
          Continue to Upload
        </button>
      </div>
    </div>
  );
}
```

---

## 4. Upload/Record Page (`/upload`)

### Purpose
Get video from user (upload file OR record with webcam)

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]                    [← Back]      │
├─────────────────────────────────────────────────┤
│                                                 │
│     Analyzing: Squat                            │
│                                                 │
│     Choose how to submit your video:            │
│                                                 │
│  ┌─────────────────┐    ┌─────────────────┐   │
│  │   📹 Record     │    │   📁 Upload     │   │
│  │   with Webcam   │    │   Video File    │   │
│  │                 │    │                 │   │
│  │  [Start Camera] │    │  [Choose File]  │   │
│  └─────────────────┘    └─────────────────┘   │
│                                                 │
│  ─────────────  OR  ─────────────              │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  📎 Drag & drop video here              │   │
│  │                                         │   │
│  │  Supported: MP4, MOV, AVI, WebM         │   │
│  │  Max size: 100MB                        │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ─────────── If recording ─────────────        │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │                                         │   │
│  │       [Webcam Preview]                  │   │
│  │                                         │   │
│  │       • • •  (00:05)                    │   │
│  │                                         │   │
│  │    [⏺ Start] [⏹ Stop] [↻ Retake]      │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Tips for best results:                        │
│  ✓ Show full body in frame                     │
│  ✓ Good lighting                               │
│  ✓ Perform 3-5 reps                           │
│                                                 │
│           [Analyze My Form →]                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/Upload.tsx
import { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';

export default function Upload() {
  const [uploadMethod, setUploadMethod] = useState<'file' | 'webcam' | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  
  const webcamRef = useRef<Webcam>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const navigate = useNavigate();
  
  const exercise = localStorage.getItem('selectedExercise') || 'Unknown';
  
  // File upload handler
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
      setUploadMethod('file');
    }
  };
  
  // Drag and drop
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setVideoFile(e.dataTransfer.files[0]);
      setUploadMethod('file');
    }
  };
  
  // Webcam recording
  const handleStartRecording = () => {
    setIsRecording(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current!.stream!, {
      mimeType: 'video/webm'
    });
    
    mediaRecorderRef.current.addEventListener('dataavailable', handleDataAvailable);
    mediaRecorderRef.current.start();
  };
  
  const handleStopRecording = () => {
    setIsRecording(false);
    mediaRecorderRef.current?.stop();
  };
  
  const handleDataAvailable = ({ data }: BlobEvent) => {
    if (data.size > 0) {
      setRecordedChunks(prev => [...prev, data]);
    }
  };
  
  // Submit for analysis
  const handleAnalyze = () => {
    // Store video (as blob or file) in context/state
    if (videoFile) {
      // Handle file upload
      navigate('/analyzing', { state: { video: videoFile, exercise } });
    } else if (recordedChunks.length > 0) {
      // Handle recorded video
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      navigate('/analyzing', { state: { video: blob, exercise } });
    }
  };
  
  return (
    <div className="upload-page">
      <Navbar />
      
      <div className="container">
        <h1>Analyzing: {exercise}</h1>
        <p>Choose how to submit your video</p>
        
        {/* Method Selection */}
        {!uploadMethod && (
          <div className="method-selection">
            <button 
              className="method-card"
              onClick={() => setUploadMethod('webcam')}
            >
              <span className="icon">📹</span>
              <h3>Record with Webcam</h3>
              <p>Use your camera to record</p>
            </button>
            
            <button 
              className="method-card"
              onClick={() => document.getElementById('file-input')?.click()}
            >
              <span className="icon">📁</span>
              <h3>Upload Video File</h3>
              <p>Choose from your device</p>
            </button>
            
            <input
              id="file-input"
              type="file"
              accept="video/*"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </div>
        )}
        
        {/* Drag and Drop Zone */}
        <div 
          className="drop-zone"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          <p>📎 Or drag & drop video here</p>
          <small>Supported: MP4, MOV, AVI, WebM (Max 100MB)</small>
        </div>
        
        {/* Webcam Recording Interface */}
        {uploadMethod === 'webcam' && (
          <div className="webcam-section">
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={{
                width: 1280,
                height: 720,
                facingMode: "user"
              }}
            />
            
            <div className="recording-controls">
              {!isRecording ? (
                <button onClick={handleStartRecording}>⏺ Start Recording</button>
              ) : (
                <button onClick={handleStopRecording}>⏹ Stop Recording</button>
              )}
              {recordedChunks.length > 0 && (
                <button onClick={() => setRecordedChunks([])}>↻ Retake</button>
              )}
            </div>
          </div>
        )}
        
        {/* File Upload Preview */}
        {videoFile && (
          <div className="video-preview">
            <video src={URL.createObjectURL(videoFile)} controls />
            <button onClick={() => setVideoFile(null)}>↻ Choose Different File</button>
          </div>
        )}
        
        {/* Tips */}
        <div className="tips">
          <h3>Tips for best results:</h3>
          <ul>
            <li>✓ Show full body in frame</li>
            <li>✓ Good lighting</li>
            <li>✓ Perform 3-5 reps</li>
            <li>✓ Side view works best for most exercises</li>
          </ul>
        </div>
        
        {/* Analyze Button */}
        <button 
          className="analyze-btn"
          disabled={!videoFile && recordedChunks.length === 0}
          onClick={handleAnalyze}
        >
          Analyze My Form →
        </button>
      </div>
    </div>
  );
}
```

---

## 5. Analysis Page (`/analyzing`)

### Purpose
Show processing status, keep user engaged while backend analyzes

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]                                  │
├─────────────────────────────────────────────────┤
│                                                 │
│         Analyzing Your Squat...                 │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │                                         │   │
│  │     [Video Playing with Skeleton]       │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ⏳ Processing frame 45 of 120...              │
│  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  37%                    │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  🧠 Vision Agent                        │   │
│  │     ✓ Extracting body landmarks         │   │
│  │     ✓ Calculating joint angles          │   │
│  │     ⏳ Detecting deviations...          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  💬 Coaching Agent                      │   │
│  │     ⏳ Analyzing with Gemini...         │   │
│  │     ⏳ Generating coaching cues...      │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Did you know?                                  │
│  Proper squat form reduces knee injury risk     │
│  by 40% according to sports science research.   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/Analyzing.tsx
import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function Analyzing() {
  const location = useLocation();
  const navigate = useNavigate();
  const { video, exercise } = location.state;
  
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('uploading');
  const [agentStatus, setAgentStatus] = useState({
    vision: 'processing',
    coaching: 'waiting'
  });
  
  useEffect(() => {
    // Simulate analysis process (replace with actual API call)
    simulateAnalysis();
  }, []);
  
  const simulateAnalysis = async () => {
    // Step 1: Upload
    setCurrentStep('uploading');
    await delay(1000);
    setProgress(10);
    
    // Step 2: Vision processing
    setCurrentStep('vision');
    setAgentStatus({ vision: 'processing', coaching: 'waiting' });
    
    for (let i = 10; i <= 60; i += 5) {
      await delay(500);
      setProgress(i);
    }
    
    setAgentStatus({ vision: 'complete', coaching: 'processing' });
    
    // Step 3: Coaching
    setCurrentStep('coaching');
    for (let i = 60; i <= 100; i += 10) {
      await delay(800);
      setProgress(i);
    }
    
    setAgentStatus({ vision: 'complete', coaching: 'complete' });
    
    // Navigate to results
    await delay(500);
    navigate('/results', { 
      state: { 
        exercise,
        // Will contain actual results from API
        results: MOCK_RESULTS 
      } 
    });
  };
  
  const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
  
  return (
    <div className="analyzing-page">
      <Navbar />
      
      <div className="container">
        <h1>Analyzing Your {exercise}...</h1>
        
        {/* Video Preview with Skeleton Overlay */}
        <div className="video-container">
          <video src={URL.createObjectURL(video)} autoPlay muted loop />
          {/* Add skeleton overlay here */}
        </div>
        
        {/* Progress Bar */}
        <div className="progress-section">
          <p>Processing frame {Math.floor(progress * 1.2)} of 120...</p>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
          <p>{progress}%</p>
        </div>
        
        {/* Agent Status Cards */}
        <div className="agent-status">
          <AgentCard
            name="Vision Agent"
            icon="👁️"
            status={agentStatus.vision}
            tasks={[
              { name: 'Extracting body landmarks', status: 'complete' },
              { name: 'Calculating joint angles', status: 'complete' },
              { name: 'Detecting deviations', status: agentStatus.vision }
            ]}
          />
          
          <AgentCard
            name="Coaching Agent"
            icon="🧠"
            status={agentStatus.coaching}
            tasks={[
              { name: 'Analyzing with Gemini', status: agentStatus.coaching },
              { name: 'Generating coaching cues', status: agentStatus.coaching }
            ]}
          />
        </div>
        
        {/* Fun Facts */}
        <div className="did-you-know">
          <h3>Did you know?</h3>
          <p>Proper squat form reduces knee injury risk by 40% according to sports science research.</p>
        </div>
      </div>
    </div>
  );
}

// Agent Status Card Component
function AgentCard({ name, icon, status, tasks }) {
  const statusIcon = {
    'waiting': '⏸️',
    'processing': '⏳',
    'complete': '✓'
  };
  
  return (
    <div className={`agent-card ${status}`}>
      <h3>{icon} {name}</h3>
      <ul>
        {tasks.map((task, i) => (
          <li key={i}>
            {statusIcon[task.status]} {task.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 6. Results Page (`/results`)

### Purpose
Show coaching feedback, form analysis, and insights

### Layout
```
┌─────────────────────────────────────────────────┐
│  [Logo: Biome]                    [← Analyze    │
│                                     Another]     │
├─────────────────────────────────────────────────┤
│                                                 │
│        Squat Form Analysis                      │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │                                         │   │
│  │     [Video with Skeleton Overlay]       │   │
│  │     [Timestamp markers for issues]      │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Overall Form Quality: 7.2/10  ⚠️              │
│  ▓▓▓▓▓▓▓░░░                                    │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  🔴 Issues Detected (3)                         │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  ⚠️  Knee Valgus (Moderate)            │   │
│  │      Frame: 23-45                       │   │
│  │                                         │   │
│  │  💬 Your right knee is collapsing       │   │
│  │     inward 12°. Push both knees out to  │   │
│  │     track over your toes.               │   │
│  │                                         │   │
│  │  [View Frame] [Learn More]              │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  ⚠️  Insufficient Depth (Minor)         │   │
│  │      Frame: 34-56                       │   │
│  │                                         │   │
│  │  💬 You're stopping 5° above parallel.  │   │
│  │     Sit back like reaching for a chair  │   │
│  │     to achieve proper depth.            │   │
│  │                                         │   │
│  │  [View Frame] [Learn More]              │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  ⚠️  Back Rounding (Moderate)           │   │
│  │      Frame: 78-92                       │   │
│  │                                         │   │
│  │  💬 Your spine is flexing 15° at the    │   │
│  │     bottom. Keep your chest up and      │   │
│  │     maintain your natural curve.        │   │
│  │                                         │   │
│  │  [View Frame] [Learn More]              │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ✅ What You Did Well                           │
│                                                 │
│  • Consistent tempo (good control)              │
│  • Balanced left/right symmetry                │
│  • Strong bracing throughout                    │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Detailed Metrics                            │
│                                                 │
│  Knee Angle (bottom):  87° ⚠️ (target: 90°)   │
│  Hip Angle (bottom):   92° ✓ (target: 85-95°) │
│  Back Angle:           18° ⚠️ (target: <15°)  │
│  Depth Achieved:       95% ⚠️ (target: 100%)  │
│  Symmetry Score:       9.2/10 ✓                │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Next Steps                                     │
│                                                 │
│  Based on your analysis, focus on:              │
│  1. Strengthening glutes (knee stability)       │
│  2. Ankle mobility drills                      │
│  3. Core bracing practice                      │
│                                                 │
│  [Get Corrective Exercises] [Track Progress]   │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Download Report] [Share Results] [Try Again] │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key Components
```jsx
// src/pages/Results.tsx
import { useLocation } from 'react-router-dom';

export default function Results() {
  const location = useLocation();
  const { exercise, results } = location.state;
  
  const {
    overallScore,
    issues,
    strengths,
    metrics,
    recommendations
  } = results;
  
  return (
    <div className="results-page">
      <Navbar />
      
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1>{exercise} Form Analysis</h1>
          <button onClick={() => navigate('/analyze')}>
            Analyze Another
          </button>
        </div>
        
        {/* Video Player with Markers */}
        <VideoPlayer 
          videoUrl={results.videoUrl}
          markers={issues.map(i => ({ time: i.frameStart / 30, type: i.severity }))}
        />
        
        {/* Overall Score */}
        <div className="overall-score">
          <h2>Overall Form Quality</h2>
          <div className="score">
            <span className="number">{overallScore}</span>
            <span className="max">/10</span>
            <span className="emoji">{overallScore >= 8 ? '✅' : overallScore >= 6 ? '⚠️' : '🔴'}</span>
          </div>
          <div className="score-bar">
            <div className="fill" style={{ width: `${overallScore * 10}%` }} />
          </div>
        </div>
        
        {/* Issues Detected */}
        <section className="issues">
          <h2>🔴 Issues Detected ({issues.length})</h2>
          {issues.map((issue, i) => (
            <IssueCard key={i} issue={issue} />
          ))}
        </section>
        
        {/* Strengths */}
        <section className="strengths">
          <h2>✅ What You Did Well</h2>
          <ul>
            {strengths.map((strength, i) => (
              <li key={i}>• {strength}</li>
            ))}
          </ul>
        </section>
        
        {/* Detailed Metrics */}
        <section className="metrics">
          <h2>📊 Detailed Metrics</h2>
          <div className="metrics-grid">
            {Object.entries(metrics).map(([key, value]) => (
              <MetricCard key={key} name={key} value={value} />
            ))}
          </div>
        </section>
        
        {/* Recommendations */}
        <section className="recommendations">
          <h2>Next Steps</h2>
          <p>Based on your analysis, focus on:</p>
          <ol>
            {recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ol>
          <div className="action-buttons">
            <button className="primary">Get Corrective Exercises</button>
            <button className="secondary">Track Progress</button>
          </div>
        </section>
        
        {/* Action Buttons */}
        <div className="bottom-actions">
          <button>📥 Download Report</button>
          <button>📤 Share Results</button>
          <button onClick={() => navigate('/analyze')}>↻ Try Again</button>
        </div>
      </div>
    </div>
  );
}

// Issue Card Component
function IssueCard({ issue }) {
  return (
    <div className={`issue-card severity-${issue.severity}`}>
      <div className="issue-header">
        <h3>
          {issue.severity === 'severe' ? '🔴' : issue.severity === 'moderate' ? '⚠️' : '⚡'}
          {issue.type} ({issue.severity})
        </h3>
        <span className="frame-info">Frame: {issue.frameStart}-{issue.frameEnd}</span>
      </div>
      
      <div className="coaching-cue">
        <p>💬 {issue.cue}</p>
      </div>
      
      <div className="issue-actions">
        <button>View Frame</button>
        <button>Learn More</button>
      </div>
    </div>
  );
}

// Metric Card Component
function MetricCard({ name, value }) {
  const isGood = value.status === 'good';
  const icon = isGood ? '✓' : '⚠️';
  
  return (
    <div className={`metric-card ${value.status}`}>
      <h4>{name}</h4>
      <p className="value">
        {value.actual} {icon}
      </p>
      <p className="target">Target: {value.target}</p>
    </div>
  );
}
```

---

## Bonus Components

### Navbar (Used on all pages)
```jsx
// src/components/Navbar.tsx
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="logo">
          <span className="icon">🧬</span>
          <span className="text">Biome</span>
        </Link>
        
        <div className="nav-links">
          <Link to="/how-it-works">How It Works</Link>
          <Link to="/analyze" className="cta-btn">Try It Free</Link>
        </div>
      </div>
    </nav>
  );
}
```

### Footer (Used on landing/info pages)
```jsx
// src/components/Footer.tsx
export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>Biome</h4>
          <p>AI-powered form coaching for everyone</p>
        </div>
        
        <div className="footer-section">
          <h4>Technology</h4>
          <ul>
            <li>Google ADK</li>
            <li>MediaPipe</li>
            <li>Gemini 2.0</li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Resources</h4>
          <ul>
            <li><a href="/how-it-works">How It Works</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">GitHub</a></li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>Built with ❤️ for Google ADK Hackathon 2025</p>
      </div>
    </footer>
  );
}
```

---

## Routing Setup

```jsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import HowItWorks from './pages/HowItWorks';
import ExerciseSelection from './pages/ExerciseSelection';
import Upload from './pages/Upload';
import Analyzing from './pages/Analyzing';
import Results from './pages/Results';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/analyze" element={<ExerciseSelection />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/analyzing" element={<Analyzing />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## API Integration Points (For Later)

When you're ready to connect the backend, here are the integration points:

### 1. ExerciseSelection Page
- No API needed (client-side only)

### 2. Upload Page
```jsx
// When user clicks "Analyze My Form"
const handleAnalyze = async () => {
  const formData = new FormData();
  formData.append('exercise', exercise);
  formData.append('video', videoFile);
  
  // POST to your API
  const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  navigate('/results', { state: { results: data } });
};
```

### 3. Analyzing Page
```jsx
// Real-time updates via WebSocket (advanced)
useEffect(() => {
  const ws = new WebSocket('ws://localhost:8000/ws/analyze');
  
  ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    if (update.type === 'progress') {
      setProgress(update.progress);
    }
    if (update.type === 'agent_status') {
      setAgentStatus(update.status);
    }
    if (update.type === 'complete') {
      navigate('/results', { state: { results: update.results } });
    }
  };
  
  ws.send(JSON.stringify({ video: videoBlob, exercise }));
}, []);
```

### 4. Results Page
- Receives data from API response, displays it
- No additional API calls needed

---

## Styling Guidelines

### Color Palette (Fitness Theme)
```css
:root {
  /* Primary Colors */
  --primary: #4F46E5;      /* Indigo */
  --primary-dark: #3730A3;
  --primary-light: #818CF8;
  
  /* Accent */
  --accent: #F59E0B;       /* Amber */
  --accent-dark: #D97706;
  
  /* Semantic */
  --success: #10B981;      /* Green */
  --warning: #F59E0B;      /* Amber */
  --error: #EF4444;        /* Red */
  
  /* Neutrals */
  --bg: #0F172A;          /* Dark blue-gray */
  --surface: #1E293B;
  --text: #F1F5F9;
  --text-secondary: #94A3B8;
}
```

### Typography
```css
/* Headings */
h1 { font-size: 3rem; font-weight: 700; }
h2 { font-size: 2rem; font-weight: 600; }
h3 { font-size: 1.5rem; font-weight: 600; }

/* Body */
body { font-size: 1rem; line-height: 1.6; }

/* Font family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Component Styles
- Rounded corners: `border-radius: 12px`
- Shadows: `box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)`
- Spacing: Use 8px grid (8, 16, 24, 32, 40, 48, 64)
- Animations: Smooth transitions `transition: all 0.3s ease`

---

## Quick Start Commands

```bash
# Create React app
npx create-react-app biome-frontend --template typescript
cd biome-frontend

# Install dependencies
npm install react-router-dom
npm install react-webcam
npm install @types/react-router-dom  # If using TypeScript

# Run development server
npm start
```

---

## Summary

**6 Pages Total:**

1. ✅ **Landing** - Marketing/hook
2. ✅ **How It Works** - Education
3. ✅ **Exercise Selection** - Input exercise name
4. ✅ **Upload/Record** - Submit video
5. ✅ **Analyzing** - Processing with agent status
6. ✅ **Results** - Coaching feedback

**Build Order:**
1. **Week 1**: Landing + Exercise Selection (static pages)
2. **Week 2**: Upload + Analyzing (file handling, UI states)
3. **Week 3**: Results (complex data display)
4. **Week 4**: Polish + integrate APIs

You can build all the UI/UX now, use mock data, and plug in the real API later. This way you have something impressive to show even while backend is still in progress!

Want me to generate actual React code for any specific page?