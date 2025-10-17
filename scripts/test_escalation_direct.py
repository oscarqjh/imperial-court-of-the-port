#!/usr/bin/env python3
"""
Simple test script to verify escalation manager contact selection 
without requiring the full orchestrator dependencies.
"""

import sys
import os

# Add the app directory to path
sys.path.append('app')

try:
    from escalation_manager import EscalationManager
    
    def test_contact_selection():
        """Test the contact selection logic directly"""
        print("🧪 TESTING ESCALATION MANAGER CONTACT SELECTION")
        print("=" * 60)
        
        # Initialize escalation manager
        manager = EscalationManager()
        
        # Test container incident
        print("\n📦 Testing Container Management Incident:")
        container_contact = manager.get_contact_by_module("Container Management")
        if container_contact:
            print(f"   ✅ Contact: {container_contact.product_ops_manager}")
            print(f"   📧 Email: {container_contact.email}")
            print(f"   🎯 Role: {container_contact.role}")
        else:
            print("   ❌ No contact found!")
            
        # Test EDI incident
        print("\n📡 Testing EDI Communication Incident:")
        edi_contact = manager.get_contact_by_module("EDI Communication")
        if edi_contact:
            print(f"   ✅ Contact: {edi_contact.product_ops_manager}")
            print(f"   📧 Email: {edi_contact.email}")
            print(f"   🎯 Role: {edi_contact.role}")
        else:
            print("   ❌ No contact found!")
            
        # Test PORTNET incident  
        print("\n🌐 Testing PORTNET System Incident:")
        portnet_contact = manager.get_contact_by_module("PORTNET System")
        if portnet_contact:
            print(f"   ✅ Contact: {portnet_contact.product_ops_manager}")
            print(f"   📧 Email: {portnet_contact.email}")
            print(f"   🎯 Role: {portnet_contact.role}")
        else:
            print("   ❌ No contact found!")
            
        # Test general incident
        print("\n🔧 Testing General Incident:")
        general_contact = manager.get_contact_by_module("General")
        if general_contact:
            print(f"   ✅ Contact: {general_contact.product_ops_manager}")
            print(f"   📧 Email: {general_contact.email}")
            print(f"   🎯 Role: {general_contact.role}")
        else:
            print("   ❌ No contact found!")
            
        print("\n" + "=" * 60)
        print("🎯 EXPECTED BEHAVIOR FROM CONTACTS.JSON:")
        print("- Container Management → Mark Lee (Container Ops Manager)")
        print("- EDI Communication → Tom Tan (EDI/API Support)")  
        print("- PORTNET/General → Helpdesk Team (PSA Helpdesk)")
        print("- Others/Infrastructure → Jacky Chan (SRE Lead)")

    def test_escalation_summary():
        """Test generating a complete escalation summary"""
        print("\n\n🧪 TESTING ESCALATION SUMMARY GENERATION")
        print("=" * 60)
        
        manager = EscalationManager()
        
        # Mock incident data for container issue
        incident_data = {
            "incident_analysis": {
                "incident_type": "Container Management",
                "severity": "High",
                "original_text": "Container MSKU7834512 showing duplicate processing in yard management system"
            }
        }
        
        # Mock database analysis
        database_analysis = {
            "system_health": {
                "edi_health": {"error_rate_percent": 15},
                "api_health": {"error_rate_percent": 5}
            },
            "container_details": {
                "container": {"cntr_no": "MSKU7834512"}
            }
        }
        
        # Generate escalation summary
        summary = manager.create_escalation_summary(
            incident_data, 
            database_analysis, 
            "Container duplicate processing detected by technical analysis"
        )
        
        print(f"\n📋 Generated Incident ID: {summary.incident_id}")
        print(f"📦 Incident Type: {summary.incident_type}")
        print(f"⚖️ Severity: {summary.severity}")
        print(f"👤 Primary Contact: {summary.primary_contact.product_ops_manager}")
        print(f"📧 Contact Email: {summary.primary_contact.email}")
        print(f"🎫 Ticket Priority: {summary.ticket_priority}")
        print(f"⏰ Est. Resolution: {summary.estimated_resolution_time}")
        
        # Format and display the full summary
        formatted_summary = manager.format_escalation_summary(summary)
        print("\n📄 FORMATTED ESCALATION SUMMARY:")
        print(formatted_summary)

    if __name__ == "__main__":
        try:
            test_contact_selection()
            test_escalation_summary()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("This test requires the escalation_manager module and contacts.json file")
