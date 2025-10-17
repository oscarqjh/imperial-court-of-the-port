"""
Example usage of database tools by AI agents for incident analysis.
This demonstrates the thought process and tool usage patterns agents should follow.
"""

from typing import Dict, Any
from .agent_tools import AgentDatabaseTools


class AgentAnalysisExample:
    """Example of how agents should think about and use database tools."""
    
    def __init__(self):
        self.tools = AgentDatabaseTools()
        
    def analyze_incident_example(self, incident_text: str) -> Dict[str, Any]:
        """
        Example analysis flow demonstrating proper database tool usage.
        This shows the systematic approach agents should take.
        """
        
        analysis_log = []
        gathered_evidence = {}
        
        # Step 1: Always start with operational baseline
        analysis_log.append("🏛️ IMPERIAL ANALYSIS BEGINS - Gathering operational baseline...")
        
        try:
            operational_overview = self.tools.get_operational_overview()
            gathered_evidence["baseline"] = operational_overview
            analysis_log.append(f"✅ Baseline established: {operational_overview.get('total_vessels', 'N/A')} vessels in port")
        except Exception as e:
            analysis_log.append(f"❌ Baseline gathering failed: {e}")
            
        # Step 2: Assess current system health
        analysis_log.append("🔍 Assessing current system health...")
        
        try:
            system_health = self.tools.check_system_health()
            gathered_evidence["health"] = system_health
            
            edi_errors = system_health.get("edi_health", {}).get("error_rate_percent", 0)
            api_errors = system_health.get("api_health", {}).get("error_rate_percent", 0)
            
            if edi_errors > 5 or api_errors > 5:
                analysis_log.append(f"⚠️ System stress detected - EDI: {edi_errors}%, API: {api_errors}% error rates")
            else:
                analysis_log.append("✅ System health nominal")
                
        except Exception as e:
            analysis_log.append(f"❌ Health check failed: {e}")
        
        # Step 3: Parse incident for specific entities to investigate
        analysis_log.append("🔎 Analyzing incident text for specific entities...")
        
        incident_lower = incident_text.lower()
        
        # Look for container references
        container_keywords = ["container", "cntr", "msku", "oolu", "temu", "cmau"]
        if any(keyword in incident_lower for keyword in container_keywords):
            analysis_log.append("📦 Container-related incident detected - searching containers...")
            
            # Extract potential container numbers
            words = incident_text.split()
            for word in words:
                if len(word) >= 10 and any(prefix in word.upper() for prefix in ["MSKU", "OOLU", "TEMU", "CMAU"]):
                    try:
                        container_details = self.tools.get_container_details(word.upper())
                        if container_details and "error" not in container_details:
                            gathered_evidence["target_container"] = container_details
                            analysis_log.append(f"✅ Found target container {word.upper()}: {container_details['container']['status']}")
                        break
                    except Exception as e:
                        analysis_log.append(f"❌ Container lookup failed: {e}")
            
            # Search for containers by status if no specific container found
            if "target_container" not in gathered_evidence:
                try:
                    problem_containers = self.tools.search_containers(status="ERROR", limit=5)
                    if problem_containers and "error" not in problem_containers:
                        gathered_evidence["problem_containers"] = problem_containers
                        analysis_log.append(f"✅ Found {len(problem_containers)} containers with issues")
                except Exception as e:
                    analysis_log.append(f"❌ Container search failed: {e}")
        
        # Look for EDI/communication issues
        edi_keywords = ["edi", "message", "coparn", "coarri", "codeco", "iftmin", "communication"]
        if any(keyword in incident_lower for keyword in edi_keywords):
            analysis_log.append("📡 EDI communication incident detected - analyzing message patterns...")
            
            try:
                edi_analysis = self.tools.analyze_edi_messages(hours_back=6, limit=15)
                if edi_analysis and "error" not in edi_analysis:
                    gathered_evidence["edi_patterns"] = edi_analysis
                    error_count = edi_analysis.get("error_count", 0)
                    total_msgs = edi_analysis.get("total_messages", 1)
                    error_rate = (error_count / total_msgs) * 100
                    
                    analysis_log.append(f"✅ EDI analysis: {error_count} errors in {total_msgs} messages ({error_rate:.1f}%)")
                    
                    if error_count > 0:
                        # Look for specific error patterns
                        error_keywords = ["timeout", "connection", "segment", "format", "validation"]
                        recent_issues = self.tools.search_recent_incidents(
                            keywords=error_keywords, 
                            hours_back=12
                        )
                        if recent_issues and "error" not in recent_issues:
                            gathered_evidence["recent_patterns"] = recent_issues
                            analysis_log.append(f"✅ Found {recent_issues.get('total_issues_found', 0)} similar recent issues")
                            
            except Exception as e:
                analysis_log.append(f"❌ EDI analysis failed: {e}")
        
        # Look for vessel-specific issues
        vessel_keywords = ["vessel", "ship", "mv ", "imo"]
        if any(keyword in incident_lower for keyword in vessel_keywords):
            analysis_log.append("🚢 Vessel-related incident detected - checking vessel details...")
            
            # Try to extract vessel name
            words = incident_text.split()
            for i, word in enumerate(words):
                if word.lower() in ["mv", "vessel"] and i + 1 < len(words):
                    vessel_name = f"{word} {words[i+1]}"
                    try:
                        vessel_details = self.tools.get_vessel_details(vessel_name=vessel_name)
                        if vessel_details and "error" not in vessel_details:
                            gathered_evidence["target_vessel"] = vessel_details
                            analysis_log.append(f"✅ Found vessel {vessel_name}: {vessel_details.get('operator_name', 'Unknown operator')}")
                        break
                    except Exception as e:
                        analysis_log.append(f"❌ Vessel lookup failed: {e}")
        
        # Step 4: Synthesize findings and determine severity
        analysis_log.append("⚖️ Synthesizing evidence and determining response priority...")
        
        # Determine incident severity based on gathered evidence
        severity_factors = []
        
        if gathered_evidence.get("health"):
            health = gathered_evidence["health"]
            edi_errors = health.get("edi_health", {}).get("error_rate_percent", 0)
            api_errors = health.get("api_health", {}).get("error_rate_percent", 0)
            
            if edi_errors > 10 or api_errors > 10:
                severity_factors.append("HIGH - System already under stress")
            elif edi_errors > 5 or api_errors > 5:
                severity_factors.append("MEDIUM - Moderate system stress")
        
        if gathered_evidence.get("recent_patterns"):
            issue_count = gathered_evidence["recent_patterns"].get("total_issues_found", 0)
            if issue_count > 10:
                severity_factors.append("HIGH - Part of larger pattern")
            elif issue_count > 3:
                severity_factors.append("MEDIUM - Similar recent incidents")
        
        # Incident classification
        incident_type = "General"
        if any(keyword in incident_lower for keyword in container_keywords):
            incident_type = "Container Operations"
        elif any(keyword in incident_lower for keyword in edi_keywords):
            incident_type = "EDI Communications"
        elif any(keyword in incident_lower for keyword in vessel_keywords):
            incident_type = "Vessel Operations"
        
        # Final severity assessment
        if "HIGH" in str(severity_factors):
            severity = "High"
        elif "MEDIUM" in str(severity_factors):
            severity = "Medium"
        else:
            severity = "Low"
        
        analysis_log.append(f"📋 ANALYSIS COMPLETE: {incident_type} incident, {severity} severity")
        
        # Generate recommendations based on evidence
        recommendations = []
        
        if gathered_evidence.get("target_container"):
            container = gathered_evidence["target_container"]["container"]
            recommendations.append(f"🚛 Deploy 工智 (Ministry of Works) for container {container['cntr_no']} in {container['status']} status")
        
        if gathered_evidence.get("edi_patterns") and gathered_evidence["edi_patterns"].get("error_count", 0) > 0:
            recommendations.append("📡 Deploy 信儀 (Ministry of Protocol) for EDI communication restoration")
        
        if gathered_evidence.get("health"):
            health = gathered_evidence["health"]
            if health.get("edi_health", {}).get("error_rate_percent", 0) > 5:
                recommendations.append("🔧 Deploy 維宦 (Maintenance Eunuchs) for system stabilization")
        
        if not recommendations:
            recommendations.append("👁️ Deploy 察信 (Field Censors) for detailed investigation")
        
        return {
            "incident_type": incident_type,
            "severity": severity,
            "analysis_process": analysis_log,
            "evidence_gathered": list(gathered_evidence.keys()),
            "detailed_evidence": gathered_evidence,
            "severity_factors": severity_factors,
            "recommendations": recommendations,
            "database_queries_made": len([log for log in analysis_log if "✅" in log or "❌" in log])
        }


def demonstrate_agent_thinking(incident_text: str) -> str:
    """
    Demonstrate the step-by-step thinking process agents should use.
    This creates a narrative of how agents should approach database tool usage.
    """
    
    analyzer = AgentAnalysisExample()
    result = analyzer.analyze_incident_example(incident_text)
    
    narrative = f"""
🏛️ IMPERIAL COURT INCIDENT ANALYSIS DEMONSTRATION

INCIDENT: "{incident_text}"

AGENT THOUGHT PROCESS:
{'='*50}

STEP 1: OPERATIONAL BASELINE ASSESSMENT
🤔 "Before analyzing any incident, I must understand the current state of port operations."
   → Called: get_operational_overview()
   → Purpose: Establish baseline vessel count, container distribution, EDI activity

STEP 2: SYSTEM HEALTH EVALUATION  
🤔 "What is the current system health? Are there existing stresses that could affect my response?"
   → Called: check_system_health()
   → Purpose: Get real-time error rates for EDI and API systems

STEP 3: INCIDENT-SPECIFIC INVESTIGATION
🤔 "What specific entities are mentioned in this incident? I need to gather facts about them."
   → Parsed incident text for: containers, vessels, EDI messages
   → Called appropriate lookup tools based on findings
   → Purpose: Get factual details about entities involved

STEP 4: PATTERN ANALYSIS
🤔 "Is this part of a larger pattern? Have we seen similar issues recently?"
   → Called: search_recent_incidents() with relevant keywords
   → Purpose: Identify if this is an isolated incident or part of broader issue

STEP 5: EVIDENCE SYNTHESIS
🤔 "Based on factual evidence gathered, what is the true severity and appropriate response?"
   → Analyzed gathered evidence for severity factors
   → Classified incident type based on database findings
   → Generated recommendations grounded in operational reality

ANALYSIS RESULTS:
{'='*50}

Incident Type: {result['incident_type']}
Severity: {result['severity']} 
Evidence Sources: {', '.join(result['evidence_gathered'])}
Database Queries: {result['database_queries_made']}

Severity Factors:
{chr(10).join(f"• {factor}" for factor in result['severity_factors'])}

Recommendations:
{chr(10).join(f"• {rec}" for rec in result['recommendations'])}

DETAILED PROCESS LOG:
{'='*50}
{chr(10).join(result['analysis_process'])}

KEY LESSON: The agent gathered factual evidence BEFORE making any conclusions. 
This is the Imperial Way - decisions based on evidence, not assumptions.
"""
    
    return narrative


# Example incident texts for testing
EXAMPLE_INCIDENTS = {
    "container_issue": "Container MSKU0000001 shows duplicate discharge records in TOS system causing billing discrepancy",
    "edi_communication": "COPARN messages from LINE-PSA failing with segment validation errors since 14:30",
    "vessel_operations": "MV Lion City 07 berth application shows conflicting advice records for berth assignment",
    "system_health": "Multiple API timeouts reported across TOS and CMS systems affecting container operations",
    "general_inquiry": "Port operations experiencing delays, need assessment of current situation"
}

if __name__ == "__main__":
    # Demonstrate analysis for different incident types
    for incident_name, incident_text in EXAMPLE_INCIDENTS.items():
        print(f"\n{'='*80}")
        print(f"DEMONSTRATION: {incident_name.upper()}")
        print('='*80)
        narrative = demonstrate_agent_thinking(incident_text)
        print(narrative)
        print("\n" + "="*80)
