import React from "react";

interface VideoPlayerProps {
  videoUrl: string;
  markers?: Array<{ time: number; type: string }>;
}

export default function VideoPlayer({
  videoUrl,
  markers = [],
}: VideoPlayerProps) {
  return (
    <div className="relative bg-gray-800 rounded-lg overflow-hidden">
      <video
        src={videoUrl}
        controls
        className="w-full h-auto"
        poster="/api/placeholder/800/450"
      />

      {/* Marker overlay */}
      {markers.length > 0 && (
        <div className="absolute bottom-4 left-4 flex space-x-2">
          {markers.map((marker, index) => (
            <div
              key={index}
              className={`w-3 h-3 rounded-full ${
                marker.type === "severe"
                  ? "bg-red-500"
                  : marker.type === "moderate"
                  ? "bg-yellow-500"
                  : "bg-green-500"
              }`}
              title={`Issue at ${marker.time}s`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
