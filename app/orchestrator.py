import os
from typing import Dict, Any, List

from loguru import logger

try:
	from crewai import Agent as CrewAgent, Task as CrewTask, Crew
	external_available = True
except Exception:
	external_available = False

from .agents import AGENTS
from .agents_db import list_recent_edi_messages
from .agent_tools import AgentDatabaseTools, get_tool_guidance_text


class ImperialOrchestrator:
	def __init__(self) -> None:
		self.mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
		self.crewai_available = external_available and not self.mock_mode

	def _search_collection(self, query_text: str, collection: str, top_k: int = 3) -> List[Dict[str, Any]]:
		"""Search specific Qdrant collection for RAG context."""
		try:
			from .rag_embeddings import embed_texts
			from .rag_qdrant import QdrantStore
			
			vec = embed_texts([query_text])[0]
			store = QdrantStore(collection=collection)
			
			hits = store.search(vector=vec, top_k=top_k)
			return hits
		except Exception as e:
			logger.warning(f"RAG search failed for collection {collection}: {e}")
			return []

	def _gather_rag_context(self, incident_text: str) -> Dict[str, Any]:
		"""Gather RAG context from case history and knowledge base collections."""
		case_history = self._search_collection(incident_text, "imperial_court_case_history", top_k=3)
		knowledge_base = self._search_collection(incident_text, "imperial_court_knowledge_base", top_k=3)
		
		return {
			"case_history": case_history,
			"knowledge_base": knowledge_base,
			"case_history_summary": "\n".join([f"- {doc.get('text', '')[:200]}..." for doc in case_history]),
			"knowledge_base_summary": "\n".join([f"- {doc.get('text', '')[:200]}..." for doc in knowledge_base])
		}

	def run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		if not incident_text:
			return {"error": "No incident text provided"}
			
		# Gather RAG context first
		rag_context = self._gather_rag_context(incident_text)
		
		# Add RAG context to incident data for agents
		enhanced_incident = {
			**incident,
			"rag_context": rag_context
		}
		
		if not self.crewai_available:
			logger.info("Running in MOCK_MODE; returning synthesized results")
			return self._mock_run(enhanced_incident)
		return self._crewai_run(enhanced_incident)

	def _mock_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		rag_context = incident.get("rag_context", {})
		
		# Enhanced mock mode with database tool simulation
		tools = AgentDatabaseTools()
		
		# Simulate agent using database tools for analysis
		db_analysis = {}
		try:
			# Simulate operational overview check
			operational_data = tools.get_operational_overview()
			db_analysis["operational_overview"] = operational_data
			
			# Simulate system health check
			health_data = tools.check_system_health()
			db_analysis["system_health"] = health_data
			
			# Look for keywords in incident for targeted searches
			text_lower = incident_text.lower()
			if any(word in text_lower for word in ["container", "cntr", "msku", "oolu", "temu", "cmau"]):
				# Extract potential container number
				words = incident_text.split()
				for word in words:
					if len(word) >= 10 and any(prefix in word.upper() for prefix in ["MSKU", "OOLU", "TEMU", "CMAU"]):
						container_data = tools.get_container_details(word.upper())
						if container_data:
							db_analysis["container_details"] = container_data
						break
			
			if any(word in text_lower for word in ["edi", "message", "coparn", "coarri", "codeco"]):
				edi_data = tools.analyze_edi_messages(hours_back=12, limit=10)
				db_analysis["edi_analysis"] = edi_data
				
		except Exception as e:
			logger.warning(f"Mock database analysis failed: {e}")
		
		# Enhanced incident classification based on database insights
		incident_type = "General"
		severity = "Medium"
		
		text_lower = incident_text.lower()
		if "email" in text_lower or "alr-" in text_lower:
			incident_type = "Email System"
		elif "container" in text_lower or "duplicate" in text_lower:
			incident_type = "Container Management"
		elif "portnet" in text_lower:
			incident_type = "PORTNET System"
		elif "edi" in text_lower:
			incident_type = "EDI Communication"
		
		# Severity assessment considering system health
		if "urgent" in text_lower or "critical" in text_lower:
			severity = "High"
		elif "low" in text_lower or "minor" in text_lower:
			severity = "Low"
		else:
			# Check system health for dynamic severity assessment
			health = db_analysis.get("system_health", {})
			edi_health = health.get("edi_health", {})
			api_health = health.get("api_health", {})
			
			if (edi_health.get("error_rate_percent", 0) > 10 or 
				api_health.get("error_rate_percent", 0) > 10):
				severity = "High"  # System already stressed
		
		strategy = f"智文 analyzes {incident_type} incident with severity {severity} using database insights"
		review = f"明鏡 reviews policy for {incident_type} incidents using knowledge base and operational data"
		decision = f"太和智君 decides on resource allocation for {severity} priority incident based on system health"
		
		try:
			recent = list_recent_edi_messages(5)
			recent_edi = [{"message_type": r.get("message_type"), "sent_at": r.get("sent_at")} for r in recent]
		except Exception:
			recent_edi = []
		
		return {
			"emperor": AGENTS["emperor"]["name"],
			"incident_analysis": {
				"incident_type": incident_type,
				"severity": severity,
				"original_text": incident_text,
				"database_insights_used": list(db_analysis.keys())
			},
			"database_analysis": db_analysis,
			"rag_results": {
				"case_history_count": len(rag_context.get("case_history", [])),
				"knowledge_base_count": len(rag_context.get("knowledge_base", [])),
				"case_history": rag_context.get("case_history", []),
				"knowledge_base": rag_context.get("knowledge_base", [])
			},
			"steps": [strategy, review, decision],
			"recent_edi": recent_edi,
			"recommendations": [
				f"Deploy 安戍 to contain {incident_type} incident",
				f"工智 to apply fix based on {len(rag_context.get('case_history', []))} similar cases and database analysis",
				f"清律 to update policy using {len(rag_context.get('knowledge_base', []))} KB references and operational data",
				f"Monitor system health - Current EDI error rate: {db_analysis.get('system_health', {}).get('edi_health', {}).get('error_rate_percent', 'N/A')}%"
			],
		}

	def _crewai_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		rag_context = incident.get("rag_context", {})
		
		# Get database tool guidance for agents
		tool_guidance = get_tool_guidance_text()
		
		# Create agents with enhanced context and comprehensive database tool access
		emperor = CrewAgent(
			role="Emperor 太和智君 - Supreme Port Authority",
			goal="Make evidence-based final decisions for port incidents using comprehensive database intelligence and strategic analysis",
			backstory=f"""You are 太和智君 (Emperor of Harmonious Wisdom), the supreme decision-maker of the Imperial Court of the Port.

DIVINE MANDATE: Supreme oversight of all port operations with access to real-time intelligence systems.

MANDATORY IMPERIAL PROTOCOL FOR ALL DECISIONS:
1. BEGIN with tools.get_operational_overview() - Know your realm's current state
2. ASSESS system stability with tools.check_system_health() - Understand existing stresses
3. INVESTIGATE specific entities based on incident:
   • Container issues: tools.get_container_details() + tools.search_containers()
   • EDI/communication: tools.analyze_edi_messages() + tools.search_recent_incidents()
   • Vessel operations: tools.get_vessel_details() + operational overview
   • System issues: tools.check_system_health() + tools.search_recent_incidents()
4. ANALYZE patterns with tools.search_recent_incidents() - Distinguish isolated vs systematic issues

IMPERIAL SEVERITY ASSESSMENT (based on database evidence):
- HIGH: System errors >10% OR >10 recent similar incidents OR critical operations affected
- MEDIUM: System errors 5-10% OR 3-10 similar incidents OR moderate operations affected  
- LOW: System errors <5% AND <3 similar incidents AND minor operational impact

EVIDENCE-BASED DECISION MAKING:
✅ "Intelligence shows 15 containers in ERROR status affecting berth operations"
❌ "There appear to be container issues"

Ancient wisdom: "知己知彼，百戰不殆" - Know yourself and your enemy, never lose a battle.
Query the database extensively to know the true state of your realm before issuing imperial edicts.""",
			verbose=True,
			temperature=0.2,
		)
		
		secretariat_strategy = CrewAgent(
			role="中書省 智文 - Strategic Analysis Minister",
			goal="Conduct systematic incident analysis using comprehensive database intelligence and historical precedent",
			backstory=f"""You are 智文 (Minister of Strategic Analysis), chief architect of Imperial Court responses.

ANALYTICAL MANDATE: Systematic investigation using {len(rag_context.get('case_history', []))} historical cases and real-time operational intelligence.

MANDATORY 4-PHASE DATABASE INVESTIGATION PROTOCOL:

PHASE 1 - BASELINE ASSESSMENT (Always First):
→ tools.get_operational_overview(): Current vessel count, container distribution, EDI activity
→ tools.check_system_health(): EDI/API error rates, system stress indicators

PHASE 2 - INCIDENT-SPECIFIC INVESTIGATION:
Container Issues: tools.get_container_details() + tools.search_containers(status="ERROR")
EDI Issues: tools.analyze_edi_messages() + tools.search_recent_incidents(keywords=["EDI"])
Vessel Issues: tools.get_vessel_details() + tools.search_containers(vessel_name)
System Issues: tools.check_system_health() + tools.search_recent_incidents(keywords=["API"])

PHASE 3 - PATTERN ANALYSIS:
→ tools.search_recent_incidents() with incident-specific keywords (12-48 hours back)
→ Classify: ISOLATED (<3 similar), PATTERN (3-10 similar), SYSTEMATIC (>10 similar)

PHASE 4 - STRATEGIC RESPONSE FRAMEWORK:
Based on database evidence, recommend:
- 工智 (Ministry of Works): Container operational issues, TOS discrepancies
- 信儀 (Ministry of Protocol): EDI errors >5%, communication breakdowns
- 維宦 (Maintenance Eunuchs): System health degradation, infrastructure issues
- 察信 (Field Censors): Insufficient evidence, complex multi-system incidents

Confucian principle: "學而不思則罔，思而不學則殆" - Learning without thinking is useless.
Gather complete database evidence before strategic analysis.""",
			verbose=True,
			temperature=0.4,
		)
		
		secretariat_review = CrewAgent(
			role="門下省 明鏡 - Quality Validation Authority",
			goal="Rigorous validation of analysis accuracy using quantitative database evidence and policy compliance verification", 
			backstory=f"""You are 明鏡 (Mirror of Clarity), the court's supreme validation authority ensuring operational accuracy.

VALIDATION MANDATE: Rigorous verification using {len(rag_context.get('knowledge_base', []))} knowledge base references and quantitative operational data.

COMPREHENSIVE DATABASE VALIDATION REQUIREMENTS:

EVIDENCE VERIFICATION CHECKLIST:
□ All container claims verified with tools.get_container_details()
□ System health assertions confirmed with tools.check_system_health()  
□ EDI analysis validated with tools.analyze_edi_messages()
□ Vessel information accuracy checked with tools.get_vessel_details()
□ Incident patterns confirmed with tools.search_recent_incidents()
□ Operational baseline verified with tools.get_operational_overview()

QUANTITATIVE ACCURACY STANDARDS:
- Error rates must cite specific percentages from tools.check_system_health()
- Container counts must match tools.search_containers() results
- EDI analysis must include actual message counts and error rates
- Incident patterns must specify numbers from tools.search_recent_incidents()
- Vessel details must match exact database records

RESPONSE PROPORTIONALITY VERIFICATION:
- HIGH SEVERITY: Must show >10% error rates OR >10 recent similar incidents
- MEDIUM SEVERITY: Must show 5-10% error rates OR 3-10 recent similar incidents  
- LOW SEVERITY: Must show <5% error rates AND <3 recent similar incidents

QUALITY FAILURE MODES TO PREVENT:
❌ Generic responses without specific database evidence
❌ Severity assessments not matching quantitative data
❌ Ministry recommendations without operational justification

Mencius taught: "路雖邇，不行不至" - Though the road be near, it cannot be traveled without walking.
Every claim must be walked through with database verification - no assumptions allowed.

AUTHORITY: Reject any analysis lacking specific database evidence citations.""",
			verbose=True,
			temperature=0.3,
		)

		# Create tasks with RAG context and database tool requirements
		analysis_task = CrewTask(
			description=f"""CRITICAL: You MUST use database tools to gather operational context before analysis.

INCIDENT TEXT:
{incident_text}

SIMILAR HISTORICAL CASES:
{rag_context.get('case_history_summary', 'No similar cases found')}

REQUIRED ANALYSIS PROCESS:
1. FIRST: Use tools.get_operational_overview() to understand current system baseline
2. SECOND: Use tools.check_system_health() to assess system stability and error rates
3. THIRD: Based on incident keywords, use appropriate tools:
   - For container issues: tools.search_containers() and tools.get_container_details()
   - For EDI issues: tools.analyze_edi_messages() and tools.get_recent_edi_activity()  
   - For vessel issues: tools.get_vessel_details()
4. FOURTH: Use tools.search_recent_incidents() with relevant keywords to find patterns
5. FINALLY: Analyze incident type, severity, and strategy based on FACTUAL data retrieved

DELIVERABLES:
- Incident classification based on database evidence
- Severity assessment considering current system health
- Response strategy grounded in operational reality
- Structured JSON output with database insights cited""",
			expected_output="JSON analysis with incident_type, severity, database_evidence_used, system_health_context, and data-driven recommendations",
			agent=secretariat_strategy,
		)
		
		review_task = CrewTask(
			description=f"""VALIDATION REQUIRED: Use database tools to verify the strategic analysis.

KNOWLEDGE BASE GUIDANCE:
{rag_context.get('knowledge_base_summary', 'No relevant knowledge base entries found')}

VALIDATION PROCESS:
1. VERIFY system health claims using tools.check_system_health()
2. CONFIRM any container/vessel details mentioned using specific lookup tools
3. VALIDATE severity assessment against current operational metrics
4. CHECK for similar recent incidents using tools.search_recent_incidents()
5. ENSURE resource recommendations align with current operational capacity

POLICY REVIEW TASKS:
1. Cross-reference analysis claims with actual database evidence
2. Validate incident classification against both knowledge base and operational data
3. Verify that recommended actions are feasible given current system state
4. Check compliance with established protocols using factual operational context
5. Identify gaps between policy guidance and operational reality
6. Suggest data-driven refinements to the response plan

CRITICAL: Your validation must be based on facts retrieved from database tools, not assumptions.""",
			expected_output="Comprehensive validation report with database evidence, policy compliance assessment, and fact-checked refined recommendations",
			agent=secretariat_review,
		)
		
		decision_task = CrewTask(
			description="""FINAL DECISION: Synthesize all analysis and database insights into comprehensive response plan.

DECISION FRAMEWORK:
1. REVIEW all database evidence gathered by strategic analysis and validation teams
2. CONSIDER current system health and operational capacity constraints
3. BALANCE immediate incident response with long-term system stability
4. ALLOCATE resources based on factual operational data, not assumptions

IMPERIAL DECISION PROCESS:
1. Synthesize strategic analysis and policy review into unified assessment
2. Assign specific ministries/agents based on incident type and current capacity
3. Set priority levels considering system health metrics and operational impact
4. Establish resource allocation aligned with current operational constraints
5. Create actionable timeline based on real system capabilities
6. Include monitoring requirements using available database tools

REQUIRED OUTPUT: Comprehensive response plan grounded in factual operational data with specific ministry assignments, evidence-based priorities, and measurable action items.""",
			expected_output="Imperial decree with evidence-based response plan, ministry assignments, resource allocation based on operational capacity, and monitoring requirements using database tools",
			agent=emperor,
		)

		crew = Crew(
			agents=[secretariat_strategy, secretariat_review, emperor], 
			tasks=[analysis_task, review_task, decision_task],
			verbose=True
		)
		
		try:
			result_text = crew.kickoff()
			return {
				"emperor": AGENTS["emperor"]["name"],
				"incident_analysis": {"original_text": incident_text},
				"rag_results": {
					"case_history_count": len(rag_context.get("case_history", [])),
					"knowledge_base_count": len(rag_context.get("knowledge_base", [])),
					"case_history": rag_context.get("case_history", []),
					"knowledge_base": rag_context.get("knowledge_base", [])
				},
				"crew_output": str(result_text)
			}
		except Exception as e:
			logger.error(f"CrewAI execution failed: {e}")
			# Fallback to mock if CrewAI fails
			return self._mock_run(incident)
