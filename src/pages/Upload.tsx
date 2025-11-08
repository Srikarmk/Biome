import { useState, useRef, useEffect } from "react";
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
  const [videoPreviewUrl, setVideoPreviewUrl] = useState<string | null>(null);
  const [webcamError, setWebcamError] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const webcamRef = useRef<Webcam>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const navigate = useNavigate();

  // Safely get selected exercise with validation
  const getSelectedExercise = (): string => {
    const stored = localStorage.getItem("selectedExercise");
    // Accept ANY exercise name from selection page (don't validate against hardcoded list)
    // This allows all exercises including Shoulder Press, Overhead Press, etc.
    if (stored && stored.trim().length > 0) {
      return stored;
    }
    // Default to Squat if missing
    return "Squat";
  };

  const exercise = getSelectedExercise();

  // Cleanup on unmount to fix memory leaks
  useEffect(() => {
    // Capture ref value for cleanup
    const webcam = webcamRef.current;
    const recordingInterval = recordingIntervalRef.current;
    const mediaRecorder = mediaRecorderRef.current;
    
    return () => {
      // Stop webcam stream
      if (webcam?.stream) {
        webcam.stream.getTracks().forEach(track => track.stop());
      }
      // Clear recording interval
      if (recordingInterval) {
        clearInterval(recordingInterval);
      }
      // Stop media recorder
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
      // Revoke object URLs to prevent memory leak
      if (videoPreviewUrl) {
        URL.revokeObjectURL(videoPreviewUrl);
      }
    };
  }, [videoPreviewUrl]);

  // Create preview URL for video file and cleanup on change
  useEffect(() => {
    if (videoFile) {
      const url = URL.createObjectURL(videoFile);
      setVideoPreviewUrl(url);
      
      // Cleanup previous URL
      return () => {
        URL.revokeObjectURL(url);
      };
    } else {
      setVideoPreviewUrl(null);
    }
  }, [videoFile]);

  // File upload handler with validation
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUploadError(null); // Clear previous errors
    
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      // Validate file type
      if (!file.type.startsWith('video/')) {
        setUploadError('Please select a video file (MP4, MOV, AVI, WebM)');
        return;
      }
      
      // Validate file size (100MB max)
      const maxSize = 100 * 1024 * 1024;
      if (file.size > maxSize) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
        setUploadError(`File too large: ${sizeMB}MB (maximum 100MB)`);
        return;
      }
      
      // Validate file not empty
      if (file.size < 1024) {
        setUploadError('File is too small or corrupted (minimum 1KB)');
        return;
      }
      
      setVideoFile(file);
      setUploadMethod("file");
    }
  };

  // Drag and drop with validation
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setUploadError(null); // Clear previous errors
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      
      // Validate file type
      if (!file.type.startsWith('video/')) {
        setUploadError('Please drop a video file (MP4, MOV, AVI, WebM)');
        return;
      }
      
      // Validate file size
      const maxSize = 100 * 1024 * 1024;
      if (file.size > maxSize) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
        setUploadError(`File too large: ${sizeMB}MB (maximum 100MB)`);
        return;
      }
      
      setVideoFile(file);
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
      recordingIntervalRef.current = null;
    }

    // Stop webcam stream after recording
    if (webcamRef.current?.stream) {
      webcamRef.current.stream.getTracks().forEach(track => track.stop());
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
      // Use existing preview URL instead of creating new one
      navigate("/analyzing", { state: { video: videoFile, exercise, videoUrl: videoPreviewUrl } });
    } else if (recordedChunks.length > 0) {
      // Handle recorded video
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      const videoUrl = URL.createObjectURL(blob);
      navigate("/analyzing", { state: { video: blob, exercise, videoUrl } });
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

        {/* Error Display */}
        {uploadError && (
          <div className="mb-8 p-4 bg-red-500/10 border-2 border-red-500 rounded-lg">
            <div className="flex items-start">
              <span className="text-2xl mr-3">⚠️</span>
              <div className="flex-1">
                <p className="text-red-500 font-semibold">Upload Error</p>
                <p className="text-text-secondary mt-1">{uploadError}</p>
              </div>
              <button
                onClick={() => setUploadError(null)}
                className="text-text-secondary hover:text-text ml-2"
                aria-label="Dismiss error"
              >
                ✕
              </button>
            </div>
          </div>
        )}

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
              {webcamError && (
                <div className="bg-red-500/10 border-2 border-red-500 rounded-lg p-4 mb-4">
                  <p className="text-red-500 font-semibold">⚠️ Camera Error</p>
                  <p className="text-text-secondary">{webcamError}</p>
                  <button
                    onClick={() => {
                      setWebcamError(null);
                      setUploadMethod(null);
                    }}
                    className="mt-2 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm"
                  >
                    Try File Upload Instead
                  </button>
                </div>
              )}
              
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
                onUserMedia={() => setWebcamError(null)}
                onUserMediaError={(error: string | DOMException) => {
                  const errorMsg = typeof error === 'string' ? error : error.message;
                  setWebcamError(
                    `Camera access denied or unavailable: ${errorMsg}. Please check browser permissions.`
                  );
                }}
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
        {videoFile && videoPreviewUrl && (
          <div className="bg-surface rounded-xl p-8 mb-8">
            <div className="max-w-2xl mx-auto">
              <video
                src={videoPreviewUrl}
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
