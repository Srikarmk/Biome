import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary";
import Landing from "./pages/Landing";
import HowItWorks from "./pages/HowItWorks";
import ExerciseSelection from "./pages/ExerciseSelection";
import Upload from "./pages/Upload";
import Analyzing from "./pages/Analyzing";
import Results from "./pages/Results";

function App() {
  return (
    <ErrorBoundary>
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
    </ErrorBoundary>
  );
}

export default App;
