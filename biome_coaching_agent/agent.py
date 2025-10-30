"""
Root ADK agent definition for Biome Coaching Agent.

Follows ADK convention: exports `root_agent` for discovery.
"""
from google.adk.agents import Agent


root_agent = Agent(
  name="biome_coaching_agent",
  model="gemini-2.0-flash",
  description="AI-powered fitness form coaching agent",
  instruction=(
    "You are an expert fitness coach specializing in movement analysis.\n\n"
    "Workflow: 1) Accept video uploads, 2) Extract pose landmarks, "
    "3) Analyze form and generate actionable cues, 4) Save results.\n"
    "Be encouraging, specific, prioritize injury prevention, use frame numbers."
  ),
  tools=[],
)


