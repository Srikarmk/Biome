# Biome Frontend

AI-powered fitness form coaching application built with React, TypeScript, and Tailwind CSS.

## Features

- **6 Complete Pages**: Landing, How It Works, Exercise Selection, Upload/Record, Analyzing, and Results
- **Modern UI**: Clean, fitness-focused design with Tailwind CSS
- **Webcam Recording**: Built-in video recording functionality
- **File Upload**: Support for video file uploads with drag & drop
- **Responsive Design**: Mobile-first approach with responsive layouts
- **TypeScript**: Full type safety throughout the application

## Tech Stack

- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **React Webcam** for camera functionality
- **Modern ES6+** features

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── Navbar.tsx      # Navigation component
│   ├── Footer.tsx      # Footer component
│   └── VideoPlayer.tsx # Video player with markers
├── pages/              # Page components
│   ├── Landing.tsx     # Homepage
│   ├── HowItWorks.tsx  # How it works page
│   ├── ExerciseSelection.tsx # Exercise selection
│   ├── Upload.tsx      # Video upload/recording
│   ├── Analyzing.tsx   # Analysis progress
│   └── Results.tsx     # Results display
├── App.tsx             # Main app component with routing
├── index.tsx           # App entry point
└── index.css           # Global styles with Tailwind
```

## Pages Overview

1. **Landing Page** (`/`) - Marketing homepage with hero section and features
2. **How It Works** (`/how-it-works`) - Explains the AI technology and process
3. **Exercise Selection** (`/analyze`) - Choose exercise type with search and categories
4. **Upload/Record** (`/upload`) - Video upload or webcam recording
5. **Analyzing** (`/analyzing`) - Real-time analysis progress with agent status
6. **Results** (`/results`) - Detailed form analysis and coaching feedback

## Key Features

### Exercise Selection

- Popular exercises grid
- Category-based filtering (Upper Body, Lower Body, Core, Other)
- Search functionality
- Custom exercise input

### Video Upload

- Webcam recording with timer
- File upload with drag & drop
- Video preview
- Recording tips and guidelines

### Analysis Flow

- Real-time progress indicators
- Agent status tracking (Vision Agent, Coaching Agent)
- Fun facts during processing
- Smooth transitions between states

### Results Display

- Overall form quality score
- Detailed issue breakdown with severity levels
- Coaching cues and recommendations
- Detailed biomechanical metrics
- Action buttons for next steps

## Styling

The application uses a custom Tailwind CSS configuration with a fitness-focused color palette:

- **Primary**: Indigo (#4F46E5)
- **Accent**: Amber (#F59E0B)
- **Background**: Dark blue-gray (#0F172A)
- **Surface**: Slate (#1E293B)
- **Text**: Light gray (#F1F5F9)

## API Integration

The frontend is designed to work with a backend API. Key integration points:

- **Upload Page**: POST video to `/analyze` endpoint
- **Analyzing Page**: WebSocket connection for real-time updates
- **Results Page**: Display data from API response

## Development

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

### Code Style

- TypeScript for type safety
- Functional components with hooks
- Tailwind CSS for styling
- Responsive design patterns
- Clean component architecture

## Future Enhancements

- Real API integration
- User authentication
- Progress tracking
- Exercise library expansion
- Social sharing features
- Mobile app version

## License

Built for Google ADK Hackathon 2025
