#!/usr/bin/env python3
"""
Test the full orchestrator system to verify it uses the escalation manager 
and provides only the single most relevant contact.
"""

import sys
import os

# Add the app directory to path
sys.path.append('app')

try:
    import sys
    import os
    
    # Add the app directory to the Python path
    app_path = os.path.join(os.path.dirname(__file__), 'app')
    sys.path.insert(0, app_path)
    
    from orchestrator import ImperialCourtOrchestrator
    
    def test_orchestrator_contact_selection():
        """Test that the orchestrator uses the escalation manager correctly"""
        print("🏛️ TESTING FULL ORCHESTRATOR CONTACT SELECTION")
        print("=" * 60)
        
        # Initialize orchestrator
        orchestrator = ImperialCourtOrchestrator()
        
        # Test container incident
        print("\n📦 Testing Container Incident through Orchestrator:")
        container_query = "Container MSKU7834512 showing duplicate processing in yard management system"
        
        try:
            result = orchestrator.run_analysis(container_query)
            print(f"📋 Result type: {type(result)}")
            
            # Check if it's a string result
            if isinstance(result, str):
                # Look for contact information in the result
                if "Mark Lee" in result and "mark.lee@psa123.com" in result:
                    print("✅ CORRECT: Found Mark Lee as container contact")
                elif any(name in result for name in ["John Doe", "Jane Smith", "Alex Brown", "Emily White"]):
                    print("❌ WRONG: Found generic placeholder contacts instead of real contact")
                    print("🔍 Generic contacts detected in result")
                else:
                    print("⚠️ UNCLEAR: Contact information format unclear")
                    
                # Show a snippet of the result
                lines = result.split('\n')[:10]  # First 10 lines
                print("\n📄 Result preview:")
                for i, line in enumerate(lines):
                    print(f"   {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
                    
            else:
                print(f"📄 Result: {result}")
                
        except Exception as e:
            print(f"❌ Error running orchestrator: {e}")
            import traceback
            traceback.print_exc()

    def test_mock_mode_specifically():
        """Test mock mode to see if it uses escalation manager"""
        print("\n\n🎭 TESTING MOCK MODE SPECIFICALLY")
        print("=" * 60)
        
        orchestrator = ImperialCourtOrchestrator()
        
        # Force mock mode
        print("🔄 Running in mock mode...")
        
        query = "EDI communication failure affecting vessel operations"
        
        try:
            # Try to access the mock_run method directly if possible
            if hasattr(orchestrator, 'mock_run'):
                result = orchestrator.mock_run(query, {})
                print("✅ Mock mode executed successfully")
                
                # Check for correct EDI contact
                if "Tom Tan" in result and "tom.tan@psa123.com" in result:
                    print("✅ CORRECT: Found Tom Tan as EDI contact") 
                elif any(name in result for name in ["John Doe", "Jane Smith", "Alex Brown", "Emily White"]):
                    print("❌ WRONG: Found generic placeholder contacts")
                else:
                    print("⚠️ UNCLEAR: Contact information unclear")
                    
                # Show result preview
                lines = result.split('\n')[:15]
                print("\n📄 Mock result preview:")
                for i, line in enumerate(lines):
                    print(f"   {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
                    
            else:
                print("⚠️ Mock mode method not directly accessible")
                
        except Exception as e:
            print(f"❌ Error in mock mode test: {e}")

    if __name__ == "__main__":
        test_orchestrator_contact_selection()
        test_mock_mode_specifically()
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("This test requires the orchestrator module")
