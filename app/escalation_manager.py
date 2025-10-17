"""
Escalation Manager for Imperial Court Incident Response
Handles contact information loading, escalation summaries, and ticketing integration.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from loguru import logger


@dataclass
class ContactInfo:
    """Contact information for escalation purposes."""
    module: str
    product_ops_manager: str
    role: str
    email: str
    responsibility: str
    escalation_steps: List[str]


@dataclass
class EscalationSummary:
    """Structured escalation summary with contact details and actions."""
    incident_id: str
    incident_type: str
    severity: str
    affected_module: str
    primary_contact: ContactInfo
    escalation_timeline: List[Dict[str, str]]
    immediate_actions: List[str]
    monitoring_requirements: List[str]
    ticket_priority: str
    estimated_resolution_time: str
    stakeholder_notifications: List[str]


class EscalationManager:
    """Manages escalation processes, contact information, and ticketing workflows."""
    
    def __init__(self, contacts_file: str = "app/data/contacts.json"):
        self.contacts_file = contacts_file
        self.contacts = self._load_contacts()
        
    def _load_contacts(self) -> List[ContactInfo]:
        """Load contact information from JSON file."""
        try:
            if not os.path.exists(self.contacts_file):
                logger.warning(f"Contacts file not found: {self.contacts_file}")
                return []
                
            with open(self.contacts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            contacts = []
            for contact_data in data.get("important_contacts", []):
                contacts.append(ContactInfo(
                    module=contact_data["module"],
                    product_ops_manager=contact_data["product_ops_manager"],
                    role=contact_data["role"],
                    email=contact_data["email"],
                    responsibility=contact_data["responsibility"],
                    escalation_steps=contact_data["escalation_steps"]
                ))
                
            logger.info(f"Loaded {len(contacts)} contact entries")
            return contacts
            
        except Exception as e:
            logger.error(f"Failed to load contacts: {e}")
            return []
    
    def get_contact_by_module(self, incident_type: str) -> Optional[ContactInfo]:
        """Get appropriate contact based on incident type."""
        # Map incident types to contact modules
        incident_module_mapping = {
            "Container Management": "Container (CNTR)",
            "Container Operations": "Container (CNTR)",
            "Vessel Operations": "Vessel (VS)",
            "Vessel Management": "Vessel (VS)",
            "EDI Communication": "EDI/API (EA)",
            "EDI Messages": "EDI/API (EA)",
            "API Issues": "EDI/API (EA)",
            "System Issues": "Others",
            "Infrastructure": "Others",
            "Email System": "PSA Helpdesk",
            "PORTNET System": "PSA Helpdesk",
            "General": "PSA Helpdesk"
        }
        
        module = incident_module_mapping.get(incident_type, "PSA Helpdesk")
        
        for contact in self.contacts:
            if contact.module == module:
                return contact
                
        # Fallback to helpdesk
        for contact in self.contacts:
            if "Helpdesk" in contact.module:
                return contact
                
        return None
    
    def determine_ticket_priority(self, severity: str, system_health: Dict[str, Any]) -> str:
        """Determine ticket priority based on severity and system health."""
        severity_lower = severity.lower()
        
        # Check system health indicators
        edi_errors = system_health.get("edi_health", {}).get("error_rate_percent", 0)
        api_errors = system_health.get("api_health", {}).get("error_rate_percent", 0)
        
        if severity_lower == "high" or edi_errors > 10 or api_errors > 10:
            return "P1 - Critical"
        elif severity_lower == "medium" or edi_errors > 5 or api_errors > 5:
            return "P2 - High"
        else:
            return "P3 - Medium"
    
    def estimate_resolution_time(self, incident_type: str, severity: str) -> str:
        """Estimate resolution time based on incident type and severity."""
        base_times = {
            "Container Management": {"High": "4 hours", "Medium": "8 hours", "Low": "24 hours"},
            "Container Operations": {"High": "4 hours", "Medium": "8 hours", "Low": "24 hours"},
            "Vessel Operations": {"High": "6 hours", "Medium": "12 hours", "Low": "48 hours"},
            "EDI Communication": {"High": "2 hours", "Medium": "6 hours", "Low": "12 hours"},
            "System Issues": {"High": "1 hour", "Medium": "4 hours", "Low": "8 hours"},
            "General": {"High": "8 hours", "Medium": "24 hours", "Low": "72 hours"}
        }
        
        incident_times = base_times.get(incident_type, base_times["General"])
        return incident_times.get(severity, "24 hours")
    
    def generate_escalation_timeline(self, contact: ContactInfo, severity: str) -> List[Dict[str, str]]:
        """Generate escalation timeline based on contact info and severity."""
        now = datetime.now()
        timeline = []
        
        if severity.lower() == "high":
            # Immediate escalation for high severity
            timeline.append({
                "time": "Immediate",
                "action": f"Notify {contact.product_ops_manager} ({contact.email})",
                "responsible": contact.role
            })
            timeline.append({
                "time": "15 minutes",
                "action": contact.escalation_steps[0] if contact.escalation_steps else "Escalate to duty team",
                "responsible": "Duty Team"
            })
            if len(contact.escalation_steps) > 1:
                timeline.append({
                    "time": "30 minutes",
                    "action": contact.escalation_steps[1],
                    "responsible": "Manager"
                })
        else:
            # Standard escalation for medium/low severity
            timeline.append({
                "time": "Within 30 minutes",
                "action": f"Notify {contact.product_ops_manager} ({contact.email})",
                "responsible": contact.role
            })
            timeline.append({
                "time": "Within 2 hours",
                "action": contact.escalation_steps[0] if contact.escalation_steps else "Escalate to duty team",
                "responsible": "Duty Team"
            })
            if len(contact.escalation_steps) > 1:
                timeline.append({
                    "time": "If unresolved after 4 hours",
                    "action": contact.escalation_steps[1],
                    "responsible": "Senior Management"
                })
        
        return timeline
    
    def generate_stakeholder_notifications(self, incident_type: str, severity: str, affected_entities: List[str]) -> List[str]:
        """Generate stakeholder notification list."""
        notifications = []
        
        # Always notify the primary contact
        notifications.append("Primary contact via email and phone")
        
        if severity.lower() == "high":
            notifications.extend([
                "Management team via urgent notification",
                "Customer service team for external communication",
                "Partner notifications if external systems affected"
            ])
        
        if "Container" in incident_type and affected_entities:
            notifications.append("Terminal operators handling affected containers")
            
        if "Vessel" in incident_type:
            notifications.append("Port authority and vessel operators")
            
        if "EDI" in incident_type or "API" in incident_type:
            notifications.append("Partner systems and external stakeholders")
        
        return notifications
    
    def create_escalation_summary(self, 
                                incident_data: Dict[str, Any], 
                                database_analysis: Dict[str, Any],
                                crew_analysis: str) -> EscalationSummary:
        """Create comprehensive escalation summary with contact information."""
        
        # Extract incident details
        incident_analysis = incident_data.get("incident_analysis", {})
        incident_type = incident_analysis.get("incident_type", "General")
        severity = incident_analysis.get("severity", "Medium")
        original_text = incident_analysis.get("original_text", "")
        
        # Get appropriate contact
        contact = self.get_contact_by_module(incident_type)
        if not contact:
            logger.warning(f"No contact found for incident type: {incident_type}")
            # Create default contact
            contact = ContactInfo(
                module="PSA Helpdesk",
                product_ops_manager="Helpdesk Team", 
                role="General Support",
                email="support@psa123.com",
                responsibility="General incident handling",
                escalation_steps=["Contact duty manager", "Escalate to senior staff"]
            )
        
        # Generate incident ID
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{abs(hash(original_text[:50])) % 10000:04d}"
        
        # Get system health for priority determination
        system_health = database_analysis.get("system_health", {})
        
        # Extract affected entities from analysis
        affected_entities = []
        if "container_details" in database_analysis:
            container_info = database_analysis["container_details"]
            if isinstance(container_info, dict) and "container" in container_info:
                affected_entities.append(container_info["container"].get("cntr_no", "Unknown"))
        
        # Generate escalation components
        escalation_timeline = self.generate_escalation_timeline(contact, severity)
        ticket_priority = self.determine_ticket_priority(severity, system_health)
        estimated_resolution = self.estimate_resolution_time(incident_type, severity)
        stakeholder_notifications = self.generate_stakeholder_notifications(incident_type, severity, affected_entities)
        
        # Extract immediate actions from crew analysis
        immediate_actions = [
            f"Contact {contact.product_ops_manager} immediately",
            f"Create {ticket_priority} ticket in tracking system",
            "Begin operational investigation using database tools",
            "Prepare stakeholder communication materials"
        ]
        
        # Monitoring requirements
        monitoring_requirements = [
            "Monitor system health metrics every 15 minutes",
            "Track resolution progress via database tools",
            "Update stakeholders every 2 hours until resolved",
            "Document all actions taken for post-incident review"
        ]
        
        return EscalationSummary(
            incident_id=incident_id,
            incident_type=incident_type,
            severity=severity,
            affected_module=contact.module,
            primary_contact=contact,
            escalation_timeline=escalation_timeline,
            immediate_actions=immediate_actions,
            monitoring_requirements=monitoring_requirements,
            ticket_priority=ticket_priority,
            estimated_resolution_time=estimated_resolution,
            stakeholder_notifications=stakeholder_notifications
        )
    
    def format_escalation_summary(self, summary: EscalationSummary) -> str:
        """Format escalation summary as structured text."""
        
        timeline_text = "\n".join([
            f"   • {item['time']}: {item['action']} (Responsible: {item['responsible']})"
            for item in summary.escalation_timeline
        ])
        
        immediate_actions_text = "\n".join([
            f"   • {action}" for action in summary.immediate_actions
        ])
        
        monitoring_text = "\n".join([
            f"   • {req}" for req in summary.monitoring_requirements
        ])
        
        notifications_text = "\n".join([
            f"   • {notif}" for notif in summary.stakeholder_notifications
        ])
        
        return f"""
🚨 ESCALATION SUMMARY
═══════════════════════════════════════════════════════

📋 INCIDENT DETAILS:
   • Incident ID: {summary.incident_id}
   • Type: {summary.incident_type}
   • Severity: {summary.severity}
   • Affected Module: {summary.affected_module}
   • Ticket Priority: {summary.ticket_priority}
   • Estimated Resolution: {summary.estimated_resolution_time}

👤 PRIMARY CONTACT:
   • Name: {summary.primary_contact.product_ops_manager}
   • Role: {summary.primary_contact.role}
   • Email: {summary.primary_contact.email}
   • Responsibility: {summary.primary_contact.responsibility}

⏰ ESCALATION TIMELINE:
{timeline_text}

🎯 IMMEDIATE ACTIONS REQUIRED:
{immediate_actions_text}

📊 MONITORING REQUIREMENTS:
{monitoring_text}

📢 STAKEHOLDER NOTIFICATIONS:
{notifications_text}

🎫 TICKETING WORKFLOW:
   • Create {summary.ticket_priority} ticket in tracking system
   • Assign to: {summary.primary_contact.product_ops_manager}
   • Initial response required within: {summary.escalation_timeline[0]['time'] if summary.escalation_timeline else '30 minutes'}
   • Estimated resolution: {summary.estimated_resolution_time}
   • Auto-escalate if not acknowledged within: 15 minutes

📝 NEXT STEPS:
   1. Execute immediate actions listed above
   2. Follow escalation timeline precisely
   3. Update all stakeholders per notification requirements
   4. Monitor resolution progress using database tools
   5. Document outcome for operational improvement

═══════════════════════════════════════════════════════
Generated by Imperial Court Incident Response System
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


def get_escalation_guidance_text() -> str:
    """Get guidance text for agents on using escalation system."""
    return """
ESCALATION INTEGRATION REQUIREMENTS:

Agents MUST use the EscalationManager to generate proper escalation summaries:

1. EXTRACT incident details from analysis
2. IDENTIFY appropriate contact from contacts.json based on incident type
3. GENERATE structured escalation summary with:
   - Specific contact information (name, email, role)
   - Time-based escalation timeline
   - Ticket priority and resolution estimates  
   - Stakeholder notification requirements
   - Immediate action items with responsible parties

4. FORMAT escalation summary for operational use
5. INCLUDE ticketing workflow integration details

The final output must be a practical escalation summary, not generic strategic text.
Focus on actionable steps, specific contacts, and clear timelines for resolution.
"""
