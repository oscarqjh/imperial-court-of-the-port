#!/usr/bin/env python3
"""
Integration test to verify the entire Imperial Court system
properly selects the correct contact for different incident types.
"""

import os
import sys

def test_system_end_to_end():
    """Test the system by examining the actual output"""
    print("🏛️ IMPERIAL COURT SYSTEM - END-TO-END CONTACT TEST")
    print("=" * 65)
    
    # Set environment to ensure mock mode
    os.environ["MOCK_MODE"] = "true"
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Test cases to verify
    test_cases = [
        {
            "name": "Container Duplicate Processing",
            "incident": "Container MSKU7834512 showing duplicate processing in yard management system",
            "expected_type": "Container Management", 
            "expected_contact": "Mark Lee",
            "expected_email": "mark.lee@psa123.com"
        },
        {
            "name": "EDI Communication Failure",
            "incident": "EDI message processing failure affecting vessel operations",
            "expected_type": "EDI Communication",
            "expected_contact": "Tom Tan", 
            "expected_email": "tom.tan@psa123.com"
        },
        {
            "name": "PORTNET Connection Issues", 
            "incident": "PORTNET system experiencing connection timeouts and delays",
            "expected_type": "PORTNET System",
            "expected_contact": "Helpdesk Team",
            "expected_email": "support@psa123.com"
        }
    ]
    
    try:
        # Import inside function to avoid import errors
        from app.orchestrator import ImperialOrchestrator
        
        orchestrator = ImperialOrchestrator()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 TEST {i}: {test_case['name']}")
            print(f"📝 Incident: {test_case['incident'][:60]}...")
            
            try:
                # Run the orchestrator
                result = orchestrator.run({"incident_text": test_case["incident"]})
                
                # Check incident classification
                incident_analysis = result.get("incident_analysis", {})
                actual_type = incident_analysis.get("incident_type", "Unknown")
                
                if actual_type == test_case["expected_type"]:
                    print(f"✅ Type Classification: {actual_type}")
                else:
                    print(f"❌ Type Mismatch: Expected '{test_case['expected_type']}', got '{actual_type}'")
                
                # Check contact information
                contact_info = result.get("contact_information", {})
                actual_contact = contact_info.get("product_ops_manager", "Unknown")
                actual_email = contact_info.get("email", "Unknown")
                
                if actual_contact == test_case["expected_contact"]:
                    print(f"✅ Contact Selection: {actual_contact}")
                else:
                    print(f"❌ Contact Mismatch: Expected '{test_case['expected_contact']}', got '{actual_contact}'")
                    
                if actual_email == test_case["expected_email"]:
                    print(f"✅ Email Correct: {actual_email}")
                else:
                    print(f"❌ Email Mismatch: Expected '{test_case['expected_email']}', got '{actual_email}'")
                
                # Check for generic contacts in escalation summary
                escalation_summary = result.get("escalation_summary", "")
                generic_contacts = ["John Doe", "Jane Smith", "Alex Brown", "Emily White"]
                found_generics = [contact for contact in generic_contacts if contact in escalation_summary]
                
                if found_generics:
                    print(f"❌ PROBLEM: Found generic contacts in summary: {found_generics}")
                else:
                    print("✅ No generic contacts found")
                    
                # Show escalation summary snippet
                summary_lines = escalation_summary.split('\n')[:15]
                contact_section = [line for line in summary_lines if 'PRIMARY CONTACT:' in line or 'Name:' in line or 'Email:' in line]
                
                if contact_section:
                    print("📋 Contact Summary:")
                    for line in contact_section:
                        print(f"   {line.strip()}")
                        
            except Exception as e:
                print(f"❌ Test failed: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n" + "=" * 65)
        print("🎯 SUMMARY:")
        print("✅ = Correct behavior (specific contact selected)")
        print("❌ = Incorrect behavior (wrong or generic contact)")
        print("The system should select ONE relevant contact per incident type")
        
    except ImportError as e:
        print(f"❌ Could not import orchestrator: {e}")
        print("This suggests there may be dependency issues.")
        
        # Fallback: test just the escalation manager
        print("\n🔄 FALLBACK: Testing escalation manager directly...")
        try:
            from app.escalation_manager import EscalationManager
            
            manager = EscalationManager()
            for test_case in test_cases:
                print(f"\n📋 {test_case['name']}: ", end="")
                contact = manager.get_contact_by_module(test_case['expected_type'])
                if contact and contact.product_ops_manager == test_case['expected_contact']:
                    print(f"✅ {contact.product_ops_manager}")
                else:
                    print(f"❌ Expected {test_case['expected_contact']}, got {contact.product_ops_manager if contact else 'None'}")
                    
        except Exception as e:
            print(f"❌ Escalation manager test failed: {e}")

if __name__ == "__main__":
    test_system_end_to_end()
