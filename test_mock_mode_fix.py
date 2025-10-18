#!/usr/bin/env python3
"""Test script to verify MOCK_MODE configuration is working correctly."""

import sys
import os

# Add the app directory to Python path
sys.path.append('.')

def test_mock_mode_config():
    """Test that mock mode configuration is working correctly."""
    print("🧪 Testing MOCK_MODE configuration...")
    
    # Test 1: Check environment variable directly
    mock_mode_env = os.getenv("MOCK_MODE", "not_set")
    print(f"📋 Environment variable MOCK_MODE: {mock_mode_env}")
    
    # Test 2: Check settings configuration
    from app.config import settings
    print(f"📊 Settings mock_mode: {settings.mock_mode}")
    
    # Test 3: Check orchestrator configuration
    from app.orchestrator import ImperialOrchestrator
    orchestrator = ImperialOrchestrator()
    print(f"🏛️ Orchestrator mock_mode: {orchestrator.mock_mode}")
    print(f"🤖 Orchestrator crewai_available: {orchestrator.crewai_available}")
    
    # Test 4: Verify external availability
    try:
        from crewai import Agent as CrewAgent, Task as CrewTask, Crew
        external_available = True
        print(f"🔧 CrewAI import successful: {external_available}")
    except Exception as e:
        external_available = False
        print(f"❌ CrewAI import failed: {e}")
    
    # Summary
    print("\n🏁 Configuration Summary:")
    print(f"   • Environment MOCK_MODE: {mock_mode_env}")
    print(f"   • Settings mock_mode: {settings.mock_mode}")
    print(f"   • Orchestrator mock_mode: {orchestrator.mock_mode}")
    print(f"   • CrewAI available: {external_available}")
    print(f"   • Should use CrewAI: {orchestrator.crewai_available}")
    
    if orchestrator.crewai_available:
        print("✅ Configuration correct: Will use CrewAI for processing")
    else:
        print("⚠️ Configuration issue: Will use mock mode")
        if not external_available:
            print("   - CrewAI is not available (import failed)")
        if orchestrator.mock_mode:
            print("   - Mock mode is enabled")

if __name__ == '__main__':
    test_mock_mode_config()
