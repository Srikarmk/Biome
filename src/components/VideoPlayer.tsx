import React, { useRef } from "react";

interface VideoPlayerProps {
  videoUrl: string;
  markers?: Array<{ time: number; type: string }>;
}

export default function VideoPlayer({
  videoUrl,
  markers = [],
}: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleMarkerClick = (time: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      videoRef.current.play();
    }
  };

  return (
    <div className="relative bg-gray-800 rounded-lg overflow-hidden">
      <video
        ref={videoRef}
        src={videoUrl}
        controls
        className="w-full h-auto"
        poster="/api/placeholder/800/450"
      />

      {/* Clickable marker overlay */}
      {markers.length > 0 && (
        <div className="absolute bottom-4 left-4 flex space-x-2">
          {markers.map((marker, index) => (
            <button
              key={index}
              onClick={() => handleMarkerClick(marker.time)}
              className={`w-3 h-3 rounded-full cursor-pointer hover:scale-150 transition-transform ${
                marker.type === "severe"
                  ? "bg-red-500"
                  : marker.type === "moderate"
                  ? "bg-yellow-500"
                  : "bg-green-500"
              }`}
              title={`Click to jump to ${marker.time.toFixed(1)}s`}
              aria-label={`Jump to issue at ${marker.time.toFixed(1)} seconds`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
