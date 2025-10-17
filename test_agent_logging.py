"""
Test script to verify agent logging functionality.
Run this to see the enhanced logging in action.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from app.orchestrator import ImperialOrchestrator

# Configure logger to show detailed output
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

def test_agent_logging():
    """Test the enhanced logging system with a sample incident."""
    
    print("🏛️ IMPERIAL COURT LOGGING TEST")
    print("=" * 50)
    
    # Create orchestrator
    orchestrator = ImperialOrchestrator()
    
    # Test incident
    test_incident = {
        "incident_text": "Container MSKU0000001 shows duplicate discharge records in TOS system causing billing discrepancy"
    }
    
    print(f"\nTesting with incident: {test_incident['incident_text']}")
    print("\nExpected log output:")
    print("- Imperial Court incident processing initiated")
    print("- RAG context gathering")
    print("- Agent workflow initialization")
    print("- Database tool invocations (if in mock mode)")
    print("- Step-by-step agent reasoning")
    print("- Final results")
    
    print("\n" + "=" * 50)
    print("STARTING ORCHESTRATOR...")
    print("=" * 50)
    
    # Run orchestrator
    result = orchestrator.run(test_incident)
    
    print("\n" + "=" * 50)
    print("TEST COMPLETED")
    print("=" * 50)
    
    # Show summary
    if "incident_analysis" in result:
        analysis = result["incident_analysis"]
        print(f"\n📊 RESULT SUMMARY:")
        print(f"   Incident Type: {analysis.get('incident_type', 'N/A')}")
        print(f"   Severity: {analysis.get('severity', 'N/A')}")
        print(f"   Database Tools Used: {len(analysis.get('database_insights_used', []))}")
        
    if "steps" in result:
        print(f"\n📋 AGENT STEPS:")
        for i, step in enumerate(result["steps"], 1):
            print(f"   {i}. {step}")
    
    return result

if __name__ == "__main__":
    test_result = test_agent_logging()
    print(f"\n✅ Test completed. Result keys: {list(test_result.keys())}")
