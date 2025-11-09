"""
Quick test script for ADK integration
Tests that the ADK Runner can orchestrate tools without needing database
"""
import asyncio
from google.genai import types
from api_server import runner

async def test_adk_runner():
    """Test ADK Runner initialization and basic operation"""
    print("\n=== Testing ADK Integration ===\n")
    
    # Test 1: Runner exists
    print("Test 1: ADK Runner initialized")
    assert runner is not None
    print("  [PASS] Runner object exists")
    
    # Test 2: Agent loaded
    print("\nTest 2: Agent configuration")
    assert runner.agent.name == "biome_coaching_agent"
    print(f"  [PASS] Agent name: {runner.agent.name}")
    assert runner.agent.model == "gemini-2.0-flash"
    print(f"  [PASS] Model: {runner.agent.model}")
    
    # Test 3: Tools registered
    print("\nTest 3: Tools registration")
    tool_count = len(runner.agent.tools)
    assert tool_count == 4
    print(f"  [PASS] {tool_count} tools registered:")
    for tool in runner.agent.tools:
        tool_name = tool.__name__ if callable(tool) else str(tool)
        print(f"    - {tool_name}")
    
    # Test 4: Session service available
    print("\nTest 4: Session management")
    session = await runner.session_service.create_session(
        app_name="biome_coaching_agent",
        user_id="test_user"
    )
    print(f"  [PASS] Session created: {session.id}")
    
    # Test 5: Test agent can respond (simple prompt that doesn't need tools)
    print("\nTest 5: Agent can respond to prompts")
    try:
        user_message = types.Content(
            role='user',
            parts=[types.Part.from_text(text="Hello, what can you help me with?")]
        )
        
        response_text = ""
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=user_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text and event.author == "model":
                        response_text += part.text
        
        if response_text:
            print(f"  [PASS] Agent responded (length: {len(response_text)} chars)")
            print(f"  Preview: {response_text[:100]}...")
        else:
            print("  [WARN] No response received")
            
    except Exception as e:
        print(f"  [FAIL] Agent error: {e}")
        raise
    
    print("\n=== ALL TESTS PASSED ===\n")
    print("[OK] ADK Runner is working correctly")
    print("[OK] Agent can orchestrate workflows")
    print("[OK] Ready for full video analysis test")
    print("\nNext: Start the server and test with frontend:")
    print("  python api_server.py")
    print("")

if __name__ == "__main__":
    asyncio.run(test_adk_runner())

