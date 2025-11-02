import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Webcam from "react-webcam";
import Navbar from "../components/Navbar";

export default function Upload() {
  const [uploadMethod, setUploadMethod] = useState<"file" | "webcam" | null>(
    null
  );
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState<Blob[]>([]);
  const [recordingTime, setRecordingTime] = useState(0);

  const webcamRef = useRef<Webcam>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const navigate = useNavigate();

  const exercise = localStorage.getItem("selectedExercise") || "Unknown";

  // File upload handler
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
      setUploadMethod("file");
    }
  };

  // Drag and drop
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setVideoFile(e.dataTransfer.files[0]);
      setUploadMethod("file");
    }
  };

  // Webcam recording
  const handleStartRecording = () => {
    if (webcamRef.current?.stream) {
      setIsRecording(true);
      setRecordingTime(0);

      mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
        mimeType: "video/webm",
      });

      mediaRecorderRef.current.addEventListener(
        "dataavailable",
        handleDataAvailable
      );
      mediaRecorderRef.current.start();

      // Start recording timer
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    }
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    mediaRecorderRef.current?.stop();

    if (recordingIntervalRef.current) {
      clearInterval(recordingIntervalRef.current);
    }
  };

  const handleDataAvailable = ({ data }: BlobEvent) => {
    if (data.size > 0) {
      setRecordedChunks((prev) => [...prev, data]);
    }
  };

  const handleRetake = () => {
    setRecordedChunks([]);
    setRecordingTime(0);
  };

  // Submit for analysis
  const handleAnalyze = () => {
    if (videoFile) {
      // Handle file upload
      navigate("/analyzing", { state: { video: videoFile, exercise } });
    } else if (recordedChunks.length > 0) {
      // Handle recorded video
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      navigate("/analyzing", { state: { video: blob, exercise } });
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  const hasVideo = videoFile || recordedChunks.length > 0;

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-text mb-4">
            Analyzing: {exercise}
          </h1>
          <p className="text-xl text-text-secondary">
            Choose how to submit your video
          </p>
        </div>

        {/* Method Selection */}
        {!uploadMethod && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            <button
              className="p-8 bg-surface border-2 border-gray-600 rounded-xl hover:border-primary-500 transition-colors text-left"
              onClick={() => setUploadMethod("webcam")}
            >
              <div className="text-5xl mb-4">📹</div>
              <h3 className="text-2xl font-semibold text-text mb-2">
                Record with Webcam
              </h3>
              <p className="text-text-secondary">
                Use your camera to record directly
              </p>
            </button>

            <button
              className="p-8 bg-surface border-2 border-gray-600 rounded-xl hover:border-primary-500 transition-colors text-left"
              onClick={() => document.getElementById("file-input")?.click()}
            >
              <div className="text-5xl mb-4">📁</div>
              <h3 className="text-2xl font-semibold text-text mb-2">
                Upload Video File
              </h3>
              <p className="text-text-secondary">Choose from your device</p>
            </button>

            <input
              id="file-input"
              type="file"
              accept="video/*"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
          </div>
        )}

        {/* Drag and Drop Zone */}
        <div
          className="border-2 border-dashed border-gray-600 rounded-xl p-12 text-center mb-8 hover:border-primary-500 transition-colors"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          <div className="text-4xl mb-4">📎</div>
          <p className="text-text-secondary text-lg">
            Or drag & drop video here
          </p>
          <p className="text-text-secondary text-sm mt-2">
            Supported: MP4, MOV, AVI, WebM (Max 100MB)
          </p>
        </div>

        {/* Webcam Recording Interface */}
        {uploadMethod === "webcam" && (
          <div className="bg-surface rounded-xl p-8 mb-8">
            <div className="max-w-2xl mx-auto">
              <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={{
                  width: 1280,
                  height: 720,
                  facingMode: "user",
                }}
                className="w-full rounded-lg mb-6"
              />

              <div className="text-center">
                <div className="mb-4">
                  {!isRecording ? (
                    <button
                      onClick={handleStartRecording}
                      className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold mr-4"
                    >
                      ⏺ Start Recording
                    </button>
                  ) : (
                    <button
                      onClick={handleStopRecording}
                      className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold mr-4"
                    >
                      ⏹ Stop Recording
                    </button>
                  )}

                  {recordedChunks.length > 0 && (
                    <button
                      onClick={handleRetake}
                      className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold"
                    >
                      ↻ Retake
                    </button>
                  )}
                </div>

                {isRecording && (
                  <div className="text-red-500 font-semibold">
                    Recording: {formatTime(recordingTime)}
                  </div>
                )}

                {recordedChunks.length > 0 && !isRecording && (
                  <div className="text-success font-semibold">
                    ✓ Recording complete ({formatTime(recordingTime)})
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* File Upload Preview */}
        {videoFile && (
          <div className="bg-surface rounded-xl p-8 mb-8">
            <div className="max-w-2xl mx-auto">
              <video
                src={URL.createObjectURL(videoFile)}
                controls
                className="w-full rounded-lg mb-4"
              />
              <div className="text-center">
                <button
                  onClick={() => setVideoFile(null)}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold"
                >
                  ↻ Choose Different File
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="bg-surface rounded-xl p-8 mb-8">
          <h3 className="text-xl font-semibold text-text mb-4">
            Tips for best results:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start">
              <span className="text-success mr-3 mt-1">✓</span>
              <span className="text-text-secondary">
                Show full body in frame
              </span>
            </div>
            <div className="flex items-start">
              <span className="text-success mr-3 mt-1">✓</span>
              <span className="text-text-secondary">Good lighting</span>
            </div>
            <div className="flex items-start">
              <span className="text-success mr-3 mt-1">✓</span>
              <span className="text-text-secondary">Perform 3-5 reps</span>
            </div>
            <div className="flex items-start">
              <span className="text-success mr-3 mt-1">✓</span>
              <span className="text-text-secondary">
                Side view works best for most exercises
              </span>
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="text-center">
          <button
            className={`px-8 py-4 rounded-lg font-semibold text-lg transition-colors duration-200 ${
              hasVideo
                ? "bg-primary-500 hover:bg-primary-600 text-white"
                : "bg-gray-600 text-gray-400 cursor-not-allowed"
            }`}
            disabled={!hasVideo}
            onClick={handleAnalyze}
          >
            Analyze My Form →
          </button>
        </div>
      </div>
    </div>
  );
}
