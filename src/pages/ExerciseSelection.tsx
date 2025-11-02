import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const POPULAR_EXERCISES = [
  { id: "squat", name: "Squat", icon: "🏋️" },
  { id: "pushup", name: "Push-up", icon: "💪" },
  { id: "deadlift", name: "Deadlift", icon: "⚡" },
  { id: "plank", name: "Plank", icon: "🧘" },
  { id: "lunge", name: "Lunge", icon: "🦵" },
  { id: "pullup", name: "Pull-up", icon: "🔝" },
];

const EXERCISE_CATEGORIES = {
  "Upper Body": [
    "Bench Press",
    "Overhead Press",
    "Bicep Curl",
    "Tricep Dip",
    "Shoulder Press",
    "Lateral Raise",
  ],
  "Lower Body": [
    "Squat",
    "Deadlift",
    "Lunge",
    "Calf Raise",
    "Box Jump",
    "Bulgarian Split Squat",
  ],
  Core: [
    "Plank",
    "Crunch",
    "Russian Twist",
    "Leg Raise",
    "Mountain Climber",
    "Bicycle Crunch",
  ],
  Other: [
    "Burpee",
    "Jump Rope",
    "Mountain Climber",
    "High Knees",
    "Jumping Jacks",
    "Bear Crawl",
  ],
};

export default function ExerciseSelection() {
  const [selectedExercise, setSelectedExercise] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("Upper Body");
  const navigate = useNavigate();

  const handleContinue = () => {
    if (selectedExercise) {
      localStorage.setItem("selectedExercise", selectedExercise);
      navigate("/upload");
    }
  };

  const filteredExercises =
    EXERCISE_CATEGORIES[
      selectedCategory as keyof typeof EXERCISE_CATEGORIES
    ]?.filter((exercise) =>
      exercise.toLowerCase().includes(searchQuery.toLowerCase())
    ) || [];

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-text mb-4">
            What exercise are you doing?
          </h1>
          <p className="text-xl text-text-secondary">
            Choose from our supported exercises or enter your own
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <input
              type="text"
              placeholder="🔍 Search exercises..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-surface border border-gray-600 rounded-lg px-4 py-3 text-text placeholder-text-secondary focus:outline-none focus:border-primary-500 transition-colors"
            />
          </div>
        </div>

        {/* Popular Exercises */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-text mb-6">Popular</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {POPULAR_EXERCISES.map((ex) => (
              <button
                key={ex.id}
                className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                  selectedExercise === ex.name
                    ? "border-primary-500 bg-primary-500/10"
                    : "border-gray-600 bg-surface hover:border-gray-500"
                }`}
                onClick={() => setSelectedExercise(ex.name)}
              >
                <div className="text-3xl mb-2">{ex.icon}</div>
                <div className="text-text font-medium text-sm">{ex.name}</div>
              </button>
            ))}
          </div>
        </section>

        {/* All Exercises by Category */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-text mb-6">
            All Exercises
          </h2>

          {/* Category Tabs */}
          <div className="flex flex-wrap gap-2 mb-6">
            {Object.keys(EXERCISE_CATEGORIES).map((cat) => (
              <button
                key={cat}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedCategory === cat
                    ? "bg-primary-500 text-white"
                    : "bg-surface text-text-secondary hover:text-text border border-gray-600"
                }`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Exercise List */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {filteredExercises.map((exercise, index) => (
              <button
                key={index}
                className={`p-3 rounded-lg text-left transition-all duration-200 ${
                  selectedExercise === exercise
                    ? "border-primary-500 bg-primary-500/10 border-2"
                    : "border border-gray-600 bg-surface hover:border-gray-500"
                }`}
                onClick={() => setSelectedExercise(exercise)}
              >
                <div className="text-text font-medium text-sm">{exercise}</div>
              </button>
            ))}
          </div>
        </section>

        {/* Custom Input */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-text mb-6">
            Or type your own
          </h2>
          <input
            type="text"
            placeholder="e.g., Downward Dog, Turkish Get-up, Handstand"
            value={selectedExercise}
            onChange={(e) => setSelectedExercise(e.target.value)}
            className="w-full bg-surface border border-gray-600 rounded-lg px-4 py-3 text-text placeholder-text-secondary focus:outline-none focus:border-primary-500 transition-colors"
          />
        </section>

        {/* Selected Exercise Display */}
        {selectedExercise && (
          <div className="mb-8 p-4 bg-primary-500/10 border border-primary-500 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-text-secondary text-sm">
                  Selected Exercise:
                </p>
                <p className="text-text font-semibold text-lg">
                  {selectedExercise}
                </p>
              </div>
              <button
                onClick={() => setSelectedExercise("")}
                className="text-text-secondary hover:text-text transition-colors"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Continue Button */}
        <div className="text-center">
          <button
            className={`px-8 py-4 rounded-lg font-semibold text-lg transition-colors duration-200 ${
              selectedExercise
                ? "bg-primary-500 hover:bg-primary-600 text-white"
                : "bg-gray-600 text-gray-400 cursor-not-allowed"
            }`}
            disabled={!selectedExercise}
            onClick={handleContinue}
          >
            Continue to Upload
          </button>
        </div>
      </div>
    </div>
  );
}
