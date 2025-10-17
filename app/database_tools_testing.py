"""
Testing Guide for Database Tools Integration
==========================================

This guide shows how to test the database tools system and validate agent behavior.

Prerequisites:
1. Database must be initialized with POST /db/init_orm
2. Tools are registered in the orchestrator
3. Agents have access to database tools in their backstories

Testing Steps:
"""

from typing import Dict, List, Any
import asyncio
from .agents_db import (
    get_vessel_operations_summary,
    get_system_health_metrics,
    search_containers_by_criteria,
    get_container_details_by_number,
    analyze_edi_messages,
    get_vessel_details,
    search_recent_api_events,
    search_incidents_by_pattern
)

class DatabaseToolsValidator:
    """Validates that all database tools are working correctly."""
    
    async def validate_all_tools(self) -> Dict[str, Any]:
        """Test all database tools systematically."""
        
        results = {
            "tool_tests": {},
            "overall_status": "unknown",
            "error_count": 0,
            "success_count": 0
        }
        
        # Test 1: Operational Overview
        print("🔍 Testing operational overview...")
        try:
            overview = await get_vessel_operations_summary()
            results["tool_tests"]["operational_overview"] = {
                "status": "success" if "total_vessels" in overview else "error",
                "data": overview,
                "description": "Basic operational metrics"
            }
            if "total_vessels" in overview:
                results["success_count"] += 1
                print(f"✅ Found {overview['total_vessels']} vessels in system")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {overview}")
        except Exception as e:
            results["tool_tests"]["operational_overview"] = {
                "status": "error",
                "error": str(e),
                "description": "Basic operational metrics"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 2: System Health
        print("\n🏥 Testing system health monitoring...")
        try:
            health = await get_system_health_metrics()
            results["tool_tests"]["system_health"] = {
                "status": "success" if "edi_health" in health else "error",
                "data": health,
                "description": "System health and error rates"
            }
            if "edi_health" in health:
                results["success_count"] += 1
                edi_rate = health["edi_health"].get("error_rate_percent", 0)
                api_rate = health["api_health"].get("error_rate_percent", 0)
                print(f"✅ System health: EDI {edi_rate}% errors, API {api_rate}% errors")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {health}")
        except Exception as e:
            results["tool_tests"]["system_health"] = {
                "status": "error",
                "error": str(e),
                "description": "System health and error rates"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 3: Container Search
        print("\n📦 Testing container search...")
        try:
            containers = await search_containers_by_criteria(limit=3)
            results["tool_tests"]["container_search"] = {
                "status": "success" if isinstance(containers, list) else "error",
                "data": f"Found {len(containers) if isinstance(containers, list) else 0} containers",
                "description": "Search containers by various criteria"
            }
            if isinstance(containers, list):
                results["success_count"] += 1
                print(f"✅ Found {len(containers)} containers")
                if containers:
                    print(f"   Sample: {containers[0].get('cntr_no', 'Unknown')} - {containers[0].get('status', 'Unknown')}")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {containers}")
        except Exception as e:
            results["tool_tests"]["container_search"] = {
                "status": "error",
                "error": str(e),
                "description": "Search containers by various criteria"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 4: Container Details
        print("\n📋 Testing container details lookup...")
        try:
            # Try to get a specific container
            details = await get_container_details_by_number("MSKU0000001")
            results["tool_tests"]["container_details"] = {
                "status": "success" if "cntr_no" in details else "error",
                "data": details.get("cntr_no", "Not found") if isinstance(details, dict) else str(details),
                "description": "Get detailed container information"
            }
            if isinstance(details, dict) and "cntr_no" in details:
                results["success_count"] += 1
                print(f"✅ Container details: {details['cntr_no']} - {details.get('status', 'Unknown')}")
            else:
                results["error_count"] += 1
                print(f"❌ Container not found or error: {details}")
        except Exception as e:
            results["tool_tests"]["container_details"] = {
                "status": "error",
                "error": str(e),
                "description": "Get detailed container information"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 5: EDI Analysis
        print("\n📡 Testing EDI message analysis...")
        try:
            edi_analysis = await analyze_edi_messages(hours_back=24, limit=5)
            results["tool_tests"]["edi_analysis"] = {
                "status": "success" if "total_messages" in edi_analysis else "error",
                "data": edi_analysis,
                "description": "Analyze EDI message patterns and errors"
            }
            if "total_messages" in edi_analysis:
                results["success_count"] += 1
                total = edi_analysis["total_messages"]
                errors = edi_analysis.get("error_count", 0)
                print(f"✅ EDI analysis: {total} total messages, {errors} errors")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {edi_analysis}")
        except Exception as e:
            results["tool_tests"]["edi_analysis"] = {
                "status": "error", 
                "error": str(e),
                "description": "Analyze EDI message patterns and errors"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 6: Vessel Details
        print("\n🚢 Testing vessel details lookup...")
        try:
            vessel_details = await get_vessel_details(vessel_name="MV Lion City 01")
            results["tool_tests"]["vessel_details"] = {
                "status": "success" if isinstance(vessel_details, dict) and vessel_details else "error",
                "data": vessel_details,
                "description": "Get detailed vessel information"
            }
            if isinstance(vessel_details, dict) and vessel_details:
                results["success_count"] += 1
                print(f"✅ Vessel found: {vessel_details.get('vessel_name', 'Unknown')}")
            else:
                results["error_count"] += 1
                print(f"❌ Vessel not found or error: {vessel_details}")
        except Exception as e:
            results["tool_tests"]["vessel_details"] = {
                "status": "error",
                "error": str(e),
                "description": "Get detailed vessel information"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 7: API Events
        print("\n🔌 Testing API events search...")
        try:
            api_events = await search_recent_api_events(hours_back=24, limit=3)
            results["tool_tests"]["api_events"] = {
                "status": "success" if isinstance(api_events, list) else "error",
                "data": f"Found {len(api_events) if isinstance(api_events, list) else 0} events",
                "description": "Search recent API events and errors"
            }
            if isinstance(api_events, list):
                results["success_count"] += 1
                print(f"✅ Found {len(api_events)} API events")
                if api_events:
                    print(f"   Sample: {api_events[0].get('endpoint', 'Unknown')} - {api_events[0].get('status_code', 'Unknown')}")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {api_events}")
        except Exception as e:
            results["tool_tests"]["api_events"] = {
                "status": "error",
                "error": str(e),
                "description": "Search recent API events and errors"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Test 8: Incident Patterns
        print("\n🔍 Testing incident pattern search...")
        try:
            incidents = await search_incidents_by_pattern(keywords=["error", "timeout"], hours_back=48)
            results["tool_tests"]["incident_patterns"] = {
                "status": "success" if "total_issues_found" in incidents else "error",
                "data": incidents,
                "description": "Search for incident patterns and trends"
            }
            if "total_issues_found" in incidents:
                results["success_count"] += 1
                total_issues = incidents["total_issues_found"]
                print(f"✅ Pattern analysis: {total_issues} matching incidents found")
            else:
                results["error_count"] += 1
                print(f"❌ Unexpected response: {incidents}")
        except Exception as e:
            results["tool_tests"]["incident_patterns"] = {
                "status": "error",
                "error": str(e),
                "description": "Search for incident patterns and trends"
            }
            results["error_count"] += 1
            print(f"❌ Error: {e}")
        
        # Overall assessment
        total_tests = results["success_count"] + results["error_count"]
        if results["success_count"] == total_tests:
            results["overall_status"] = "all_pass"
            print(f"\n✅ ALL TESTS PASSED ({results['success_count']}/{total_tests})")
        elif results["success_count"] > 0:
            results["overall_status"] = "partial_pass"
            print(f"\n⚠️ PARTIAL SUCCESS ({results['success_count']}/{total_tests} tools working)")
        else:
            results["overall_status"] = "all_fail"
            print(f"\n❌ ALL TESTS FAILED - Database likely not initialized")
        
        return results


async def quick_database_check() -> bool:
    """Quick check if database is populated."""
    try:
        overview = await get_vessel_operations_summary()
        return "total_vessels" in overview and overview["total_vessels"] > 0
    except:
        return False


def agent_tool_usage_guide() -> str:
    """Generate comprehensive guide for agents on tool usage."""
    
    guide = """
🏛️ IMPERIAL COURT DATABASE TOOLS GUIDE FOR AI AGENTS
====================================================

PRINCIPLE: "知己知彼，百戰不殆" - Know yourself and your enemy, never lose a battle
Agents must gather factual evidence before making decisions.

MANDATORY TOOL USAGE PATTERNS:
==============================

1. INCIDENT RESPONSE PROTOCOL:
   
   Step 1: BASELINE ASSESSMENT (Always First)
   → get_operational_overview()
   Purpose: Understand current port state before analyzing incident
   
   Step 2: SYSTEM HEALTH CHECK (Always Second) 
   → check_system_health()
   Purpose: Identify existing stresses that could affect response
   
   Step 3: ENTITY-SPECIFIC INVESTIGATION (Based on Incident)
   Container Issues → get_container_details() + search_containers()
   EDI Issues → analyze_edi_messages() + search_recent_incidents()
   Vessel Issues → get_vessel_details()
   System Issues → search_recent_incidents() with technical keywords
   
   Step 4: PATTERN ANALYSIS (For Context)
   → search_recent_incidents() with relevant keywords
   Purpose: Determine if isolated incident or part of larger pattern

2. DECISION-MAKING REQUIREMENTS:
   
   HIGH SEVERITY indicators from database:
   - System error rates > 10% (from check_system_health)
   - Multiple recent similar incidents (from search_recent_incidents)
   - Critical vessel/container operations affected
   
   MEDIUM SEVERITY indicators:
   - System error rates 5-10%
   - 3-10 similar recent incidents
   - Non-critical operations affected
   
   LOW SEVERITY:
   - System error rates < 5%
   - Isolated incident (< 3 similar recent)
   - Minor operational impact

3. EVIDENCE-BASED RESPONSES:
   
   NEVER make assumptions - use database facts:
   ✅ "Database shows 15 containers in ERROR status affecting berth operations"
   ❌ "There might be container issues"
   
   ✅ "EDI error rate is currently 12% with 8 COPARN validation failures in last 6 hours"
   ❌ "EDI seems to have problems"
   
   ✅ "MV Lion City 07 shows conflicting berth advice records created 2 hours apart"
   ❌ "The vessel might have scheduling conflicts"

4. TOOL SELECTION MATRIX:
   
   Incident Type → Primary Tools → Secondary Tools
   
   Container Operations:
   Primary: get_container_details(), search_containers()
   Secondary: get_operational_overview(), check_system_health()
   
   EDI Communications:
   Primary: analyze_edi_messages(), search_recent_incidents() 
   Secondary: check_system_health(), get_operational_overview()
   
   Vessel Operations:
   Primary: get_vessel_details(), get_operational_overview()
   Secondary: search_containers() (for vessel's containers)
   
   System Performance:
   Primary: check_system_health(), search_recent_incidents()
   Secondary: analyze_edi_messages(), get_operational_overview()

5. RESPONSE ESCALATION BASED ON DATABASE EVIDENCE:
   
   Deploy 工智 (Ministry of Works) when:
   - Container status errors detected in database
   - Multiple containers showing same issue pattern
   - TOS/CMS operational data shows discrepancies
   
   Deploy 信儀 (Ministry of Protocol) when:
   - EDI error rates exceed thresholds
   - Message validation failures detected
   - Communication partner issues identified
   
   Deploy 維宦 (Maintenance Eunuchs) when:
   - System health metrics show degradation
   - Infrastructure performance issues detected
   - Multiple system components affected
   
   Deploy 察信 (Field Censors) when:
   - Database evidence insufficient for immediate action
   - Complex multi-system incidents requiring investigation
   - Pattern analysis shows unusual activity

6. IMPERIAL WISDOM INTEGRATION:
   
   Combine database facts with Imperial principles:
   
   "Based on database evidence showing..."
   + Imperial wisdom: "As the Classic of Changes teaches..."
   + Practical action: "Therefore, I recommend deploying..."
   
   Example:
   "Database shows 12% EDI error rate with 15 COPARN failures in 6 hours, 
   indicating communication breakdown. As Confucius taught, '信而后勞其民' 
   - trust comes before demanding action from people. The communication 
   infrastructure must be restored before expecting normal operations. 
   I recommend immediate deployment of 信儀 (Ministry of Protocol) to 
   restore EDI connectivity."

CRITICAL SUCCESS FACTORS:
========================

1. ALWAYS query database before concluding
2. Base severity on quantitative evidence 
3. Identify specific entities (containers, vessels, messages)
4. Check for patterns in recent incidents
5. Ground Imperial wisdom in operational facts
6. Provide specific deployment recommendations with evidence

FAILURE MODES TO AVOID:
======================

❌ Making assumptions without database queries
❌ Giving generic responses without specific evidence
❌ Ignoring system health context
❌ Missing pattern analysis for recurring issues
❌ Recommending actions without factual basis
❌ Using Imperial style without operational substance

Remember: The database tools are your eyes and ears in the port. 
Use them extensively to see the true situation before taking action.
The Imperial Court values informed decisions above all else.
"""
    
    return guide


if __name__ == "__main__":
    print("Database Tools Testing Framework")
    print("================================")
    
    # Check if database is available
    print("Checking database connectivity...")
    
    async def run_tests():
        db_available = await quick_database_check()
        
        if not db_available:
            print("❌ Database not available or not populated")
            print("Please run: POST /db/init_orm to initialize database")
            return
        
        print("✅ Database appears to be available")
        print("\nRunning comprehensive tool validation...")
        
        validator = DatabaseToolsValidator()
        results = await validator.validate_all_tools()
        
        print(f"\nTEST SUMMARY:")
        print(f"Success: {results['success_count']}")
        print(f"Errors: {results['error_count']}")
        print(f"Status: {results['overall_status']}")
        
        if results['overall_status'] == 'all_pass':
            print("\n🎉 All tools working! Agents ready for intelligent operation.")
        elif results['overall_status'] == 'partial_pass':
            print(f"\n⚠️ Some tools working. Check failed tools and database state.")
        else:
            print(f"\n❌ Tools not functional. Initialize database with POST /db/init_orm")
    
    # Run the async test
    import asyncio
    asyncio.run(run_tests())
    
    # Show agent usage guide
    print("\n" + "="*80)
    print(agent_tool_usage_guide())
