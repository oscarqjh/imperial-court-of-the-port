#!/usr/bin/env python3
"""
Test the improved CrewAI contact selection system.
"""

import os
import sys

def test_crewai_contact_fix():
    """Test that CrewAI mode now properly selects contacts"""
    print("🤖 TESTING IMPROVED CREWAI CONTACT SELECTION")
    print("=" * 60)
    
    # Force CrewAI mode (disable mock mode)
    os.environ["MOCK_MODE"] = "false"
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app.orchestrator import ImperialOrchestrator
        
        orchestrator = ImperialOrchestrator()
        
        # Test container incident
        print("📦 Testing Container Incident:")
        container_query = "Container CMAU0000020 showing duplicate processing entries in PORTNET system"
        
        try:
            result = orchestrator.run({"incident_text": container_query})
            
            print(f"📋 Incident Type: {result.get('incident_analysis', {}).get('incident_type', 'Unknown')}")
            print(f"⚖️ Severity: {result.get('incident_analysis', {}).get('severity', 'Unknown')}")
            
            # Check contact information
            contact_info = result.get("contact_information", {})
            if contact_info and "error" not in contact_info:
                print(f"✅ Contact: {contact_info.get('name', contact_info.get('product_ops_manager', 'Unknown'))}")
                print(f"📧 Email: {contact_info.get('email', 'Unknown')}")
                print(f"🎯 Role: {contact_info.get('role', 'Unknown')}")
            else:
                print(f"❌ Contact Info: {contact_info}")
            
            # Check escalation summary
            escalation_summary = result.get("escalation_summary", "")
            if "Mark Lee" in escalation_summary and "mark.lee@psa123.com" in escalation_summary:
                print("✅ Escalation summary contains correct contact (Mark Lee)")
            elif any(generic in escalation_summary for generic in ["[Technical Team Lead Contact Information]", "John Doe", "Jane Smith"]):
                print("❌ Escalation summary still contains generic placeholders")
            else:
                print("⚠️ Escalation summary contact status unclear")
            
            # Show escalation summary preview
            summary_lines = escalation_summary.split('\n')[:20]
            print("\n📄 Escalation Summary Preview:")
            for i, line in enumerate(summary_lines):
                if line.strip():
                    print(f"   {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
                    
        except Exception as e:
            print(f"❌ CrewAI test failed: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n" + "=" * 60)
        print("Expected for container incident:")
        print("- Contact: Mark Lee (mark.lee@psa123.com)")
        print("- NO generic placeholders like '[Technical Team Lead Contact Information]'")
        
    except ImportError as e:
        print(f"❌ Could not import orchestrator: {e}")

if __name__ == "__main__":
    test_crewai_contact_fix()
