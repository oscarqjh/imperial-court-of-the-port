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
			logger.debug(f"🔍 Searching {collection} collection for: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}'")
			from .rag_embeddings import embed_texts
			from .rag_qdrant import QdrantStore
			
			vec = embed_texts([query_text])[0]
			store = QdrantStore(collection=collection)
			
			hits = store.search(vector=vec, top_k=top_k)
			logger.debug(f"   📊 Found {len(hits)} results in {collection}")
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

	def run(self, incident: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		if not incident_text:
			return {"error": "No incident text provided"}
		
		logger.info("🏛️ IMPERIAL COURT INCIDENT PROCESSING INITIATED")
		logger.info(f"📋 Incident Text: {incident_text[:100]}{'...' if len(incident_text) > 100 else ''}")
		
		if progress_callback:
			progress_callback(15, "Gathering RAG context from historical cases...")
		
		# Gather RAG context first
		logger.info("🔍 Gathering RAG context from historical cases and knowledge base...")
		rag_context = self._gather_rag_context(incident_text)
		logger.info(f"📚 RAG Context Retrieved - Cases: {len(rag_context.get('case_history', []))}, KB: {len(rag_context.get('knowledge_base', []))}")
		
		if progress_callback:
			progress_callback(25, "RAG context gathered, preparing agent workflow...")
		
		# Add RAG context to incident data for agents
		enhanced_incident = {
			**incident,
			"rag_context": rag_context
		}
		
		if not self.crewai_available:
			logger.info("🎭 Running in MOCK_MODE; returning synthesized results")
			return self._mock_run(enhanced_incident, progress_callback)
		
		logger.info("🤖 Initiating CrewAI Agent Workflow...")
		return self._crewai_run(enhanced_incident, progress_callback)

	def _mock_run(self, incident: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		rag_context = incident.get("rag_context", {})
		
		logger.info("🎭 MOCK MODE AGENT SIMULATION INITIATED")
		
		if progress_callback:
			progress_callback(30, "Initializing Imperial Court agents...")
		
		import time
		time.sleep(1)  # Simulate initialization time
		
		# Enhanced mock mode with database tool simulation
		tools = AgentDatabaseTools()
		
		if progress_callback:
			progress_callback(40, "Agent 太和智君 (Emperor) analyzing incident...")
		
		# Simulate agent using database tools for analysis
		logger.info("📊 Simulating agent database tool usage...")
		db_analysis = {}
		try:
			# Simulate operational overview check
			logger.info("   🔍 Agent retrieving operational overview...")
			operational_data = tools.get_operational_overview()
			db_analysis["operational_overview"] = operational_data
			logger.info(f"   ✅ Operational data retrieved: {operational_data.get('total_vessels', 'N/A')} vessels")
			
			time.sleep(1)  # Simulate processing time
			if progress_callback:
				progress_callback(50, "Agent 智文 (Grand Secretariat Strategy) reviewing data...")
			
			# Simulate system health check
			logger.info("   🏥 Agent checking system health...")
			health_data = tools.check_system_health()
			db_analysis["system_health"] = health_data
			if "edi_health" in health_data:
				edi_rate = health_data["edi_health"].get("error_rate_percent", 0)
				logger.info(f"   ✅ System health retrieved: {edi_rate}% EDI error rate")
			else:
				logger.info("   ⚠️ System health data not available")
			
			# Look for keywords in incident for targeted searches
			text_lower = incident_text.lower()
			if any(word in text_lower for word in ["container", "cntr", "msku", "oolu", "temu", "cmau"]):
				if progress_callback:
					progress_callback(60, "Agent 行吏 (Ministry Personnel) searching container details...")
				logger.info("   📦 Agent detected container-related incident, searching containers...")
				# Extract potential container number
				words = incident_text.split()
				for word in words:
					if len(word) >= 10 and any(prefix in word.upper() for prefix in ["MSKU", "OOLU", "TEMU", "CMAU"]):
						logger.info(f"   🔍 Agent searching for container: {word.upper()}")
						container_data = tools.get_container_details(word.upper())
						if container_data:
							db_analysis["container_details"] = container_data
							logger.info(f"   ✅ Container details retrieved for {word.upper()}")
						break
			
			time.sleep(1)  # Simulate processing time
			if progress_callback:
				progress_callback(70, "Agent 明鏡 (Grand Secretariat Review) analyzing EDI messages...")
			
			if any(word in text_lower for word in ["edi", "message", "coparn", "coarri", "codeco"]):
				logger.info("   📡 Agent detected EDI-related incident, analyzing messages...")
				edi_data = tools.analyze_edi_messages(hours_back=12, limit=10)
				db_analysis["edi_analysis"] = edi_data
				if "total_messages" in edi_data:
					logger.info(f"   ✅ EDI analysis completed: {edi_data['total_messages']} messages analyzed")
				
		except Exception as e:
			logger.warning(f"Mock database analysis failed: {e}")
		
		# Enhanced incident classification based on database insights
		time.sleep(1)  # Simulate processing time
		if progress_callback:
			progress_callback(80, "Agent 公衡 (Censorate Chief) classifying incident severity...")
		
		logger.info("🧠 Agent analyzing incident type and severity...")
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
		
		logger.info(f"   📋 Incident classified as: {incident_type}")
		
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
				logger.info("   ⚠️ Severity elevated to HIGH due to system stress")
		
		logger.info(f"   ⚖️ Severity assessed as: {severity}")
		
		# Agent decision simulation
		time.sleep(1)  # Simulate processing time
		if progress_callback:
			progress_callback(85, "All agents formulating strategic response...")
		
		logger.info("🎯 Agents formulating strategic response...")
		strategy = f"智文 analyzes {incident_type} incident with severity {severity} using database insights"
		review = f"明鏡 reviews policy for {incident_type} incidents using knowledge base and operational data"
		decision = f"太和智君 decides on resource allocation for {severity} priority incident based on system health"
		
		logger.info(f"   📝 Strategic Analysis (智文): {strategy}")
		logger.info(f"   🔍 Policy Review (明鏡): {review}")
		logger.info(f"   👑 Imperial Decision (太和智君): {decision}")
		
		time.sleep(1)  # Simulate processing time
		if progress_callback:
			progress_callback(90, "Agent 察信 (Censorate Field) generating escalation summary...")
		
		try:
			recent = list_recent_edi_messages(5)
			recent_edi = [{"message_type": r.get("message_type"), "sent_at": r.get("sent_at")} for r in recent]
		except Exception:
			recent_edi = []
		
		logger.info("✅ MOCK MODE AGENT PROCESSING COMPLETED")
		
		# Generate escalation summary in mock mode
		logger.info("🎫 Generating escalation summary with contact information...")
		escalation_result = tools.generate_escalation_summary(
			{"incident_analysis": {
				"incident_type": incident_type,
				"severity": severity,
				"original_text": incident_text,
				"database_insights_used": list(db_analysis.keys())
			}},
			db_analysis,
			f"Strategic analysis: {strategy}. Review: {review}. Decision: {decision}"
		)
		
		if "error" not in escalation_result:
			logger.info(f"   ✅ Escalation summary generated: {escalation_result.get('incident_id', 'Unknown ID')}")
			logger.info(f"   📞 Contact: {escalation_result.get('primary_contact', {}).get('name', 'Unknown')}")
		
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
			"escalation_summary": escalation_result.get("formatted_summary", "Escalation summary generation failed"),
			"contact_information": escalation_result.get("primary_contact", {}),
			"ticket_priority": escalation_result.get("ticket_priority", "P3 - Medium"),
			"incident_id": escalation_result.get("incident_id", "Unknown")
		}

	def _crewai_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		rag_context = incident.get("rag_context", {})
		
		logger.info("🤖 CREWAI AGENT WORKFLOW INITIATED")
		logger.info(f"👥 Assembling Expanded Imperial Court: 6 Specialized Agents")
		
		# Get database tool guidance for agents
		tool_guidance = get_tool_guidance_text()
		
		logger.info("🏗️ Creating specialized multi-agent system with database tool access...")
		
		# Create expanded agent system with specialized roles
		
		# 1. Intelligence Gathering Agent - First Line Investigation
		intelligence_agent = CrewAgent(
			role="察信 (Field Censor) - Intelligence Gathering Specialist",
			goal="Conduct comprehensive initial investigation and evidence collection using all available database tools",
			backstory=f"""You are 察信 (Truth Seeker), the Imperial Court's premier intelligence gathering specialist.

INVESTIGATION MANDATE: Comprehensive evidence collection using all available database intelligence systems.

COMPLETE INVESTIGATION PROTOCOL:
1. SYSTEM BASELINE: tools.get_operational_overview() + tools.check_system_health()
2. INCIDENT TRIAGE: Extract keywords and classify incident type from text
3. TARGETED INVESTIGATION:
   - Container incidents: tools.search_containers() + tools.get_container_details()
   - EDI incidents: tools.analyze_edi_messages() + tools.get_recent_edi_activity()
   - Vessel incidents: tools.get_vessel_details() 
   - System incidents: tools.check_system_health() deep dive
4. PATTERN SEARCH: tools.search_recent_incidents() with relevant keywords
5. EVIDENCE SYNTHESIS: Compile complete factual dossier

Your duty: Gather ALL relevant evidence before any other agents begin analysis.
Motto: "事實勝於雄辯" - Facts are more eloquent than speeches.""",
			verbose=True,
			temperature=0.2,
		)
		
		# 2. Technical Analysis Agent - Deep Technical Investigation  
		technical_agent = CrewAgent(
			role="工智 (Ministry of Works) - Technical Analysis Expert",
			goal="Perform deep technical analysis of system components, root cause investigation, and technical impact assessment",
			backstory=f"""You are 工智 (Master of Technical Wisdom), the Imperial Court's chief technical analyst.

TECHNICAL ANALYSIS MANDATE: Deep dive technical investigation and root cause analysis.

TECHNICAL INVESTIGATION FRAMEWORK:
1. RECEIVE evidence dossier from 察信 (Intelligence Agent)
2. TECHNICAL DEEP DIVE:
   - System Performance: Analyze error rates, throughput metrics, capacity utilization
   - Component Analysis: Examine specific systems (EDI, TOS, PORTNET) affected
   - Integration Points: Check API connections, message flows, data consistency
   - Infrastructure Health: Network, database, application layer assessment
3. ROOT CAUSE ANALYSIS:
   - Timeline reconstruction using database timestamps
   - Dependency mapping between affected systems
   - Error correlation across multiple components
4. TECHNICAL IMPACT ASSESSMENT:
   - Current operational impact (quantified)
   - Downstream risk assessment
   - Recovery complexity estimation

Your expertise: Transform raw evidence into technical understanding.
Engineering principle: "工欲善其事，必先利其器" - To do good work, first sharpen your tools.""",
			verbose=True,
			temperature=0.3,
		)
		
		# 3. Business Impact Agent - Operations and Business Analysis
		business_agent = CrewAgent(
			role="戶部 (Ministry of Finance) - Business Impact Analyst", 
			goal="Assess operational and business impact, resource requirements, and strategic implications",
			backstory=f"""You are 金策 (Financial Strategy), the Imperial Court's business impact assessment specialist.

BUSINESS ANALYSIS MANDATE: Operational impact assessment and resource optimization.

BUSINESS IMPACT FRAMEWORK:
1. OPERATIONAL IMPACT ANALYSIS:
   - Service Level Assessment: Which operations are affected and how severely
   - Customer Impact: Internal/external stakeholder effects
   - Performance Metrics: KPI degradation measurement
   - Resource Utilization: Current vs optimal resource allocation
2. BUSINESS CONTINUITY:
   - Workaround feasibility assessment
   - Alternative process identification
   - Service restoration priorities
3. STRATEGIC IMPLICATIONS:
   - Long-term operational risk
   - Compliance and regulatory considerations  
   - Stakeholder communication requirements
4. RESOURCE OPTIMIZATION:
   - Personnel allocation recommendations
   - System resource reallocation
   - Budget impact assessment

Your domain: Translate technical problems into business understanding.
Wisdom: "取之有度，用之有節" - Take with measure, use with moderation.""",
			verbose=True,
			temperature=0.4,
		)
		
		# 4. Communication Coordinator - Stakeholder Management
		communication_agent = CrewAgent(
			role="信儀 (Ministry of Protocol) - Communication Coordinator",
			goal="Design communication strategy, stakeholder notifications, and escalation pathways",
			backstory=f"""You are 信儀 (Master of Protocol), the Imperial Court's communication and escalation specialist.

COMMUNICATION MANDATE: Orchestrate all stakeholder communication and escalation protocols.

COMMUNICATION FRAMEWORK:
1. STAKEHOLDER MAPPING:
   - Internal teams: Technical, operations, management
   - External parties: Customers, vendors, regulatory bodies
   - Contact classification: Primary, secondary, emergency contacts
2. COMMUNICATION STRATEGY:
   - Message crafting for different audiences
   - Timing and frequency optimization
   - Channel selection (email, phone, emergency alerts)
3. ESCALATION PATHWAY DESIGN:
   - Progressive escalation triggers and timelines
   - Authority level requirements for decisions
   - Emergency bypass procedures
4. COORDINATION MANAGEMENT:
   - Cross-team synchronization requirements
   - Status update schedules
   - Resolution confirmation protocols

Your responsibility: Ensure information flows efficiently to enable rapid response.
Protocol: "信則人任焉" - When there is trust, people will take responsibility.""",
			verbose=True,
			temperature=0.3,
		)
		
		# 5. Strategic Analysis Agent - High-Level Strategy (Enhanced)
		secretariat_strategy = CrewAgent(
			role="中書省 智文 - Strategic Synthesis Minister",
			goal="Synthesize all specialist analysis into comprehensive strategic response framework",
			backstory=f"""You are 智文 (Minister of Strategic Synthesis), orchestrator of specialized intelligence into unified strategy.

STRATEGIC SYNTHESIS MANDATE: Integrate all specialist analysis into cohesive response strategy.

SYNTHESIS FRAMEWORK:
1. INTELLIGENCE INTEGRATION:
   - Combine technical, business, and communication assessments
   - Identify strategic patterns and implications
   - Resolve conflicts between specialist recommendations
2. STRATEGIC RESPONSE DESIGN:
   - Multi-phase response plan development
   - Resource allocation optimization across all domains
   - Timeline coordination between technical and business actions
3. RISK MANAGEMENT:
   - Comprehensive risk assessment across all dimensions
   - Contingency planning for multiple scenarios
   - Success metrics and monitoring framework
4. DECISION SUPPORT:
   - Present clear options with trade-off analysis
   - Recommendation prioritization and sequencing
   - Implementation feasibility assessment

Enhanced Role: You now orchestrate 4 specialist agents rather than conducting primary investigation.
Philosophy: "統而不治，治而不統" - Coordinate without micromanaging, manage without controlling.""",
			verbose=True,
			temperature=0.4,
		)
		
		# 6. Quality Validation Agent (Enhanced)
		secretariat_review = CrewAgent(
			role="門下省 明鏡 - Multi-Domain Validation Authority",
			goal="Comprehensive validation across technical, business, communication, and strategic dimensions", 
			backstory=f"""You are 明鏡 (Mirror of Universal Clarity), supreme validation authority across all specialist domains.

MULTI-DOMAIN VALIDATION MANDATE: Rigorous verification across all specialist analysis areas.

COMPREHENSIVE VALIDATION FRAMEWORK:
1. TECHNICAL VALIDATION:
   - Verify all database evidence and technical analysis accuracy
   - Confirm root cause analysis logic and supporting data
   - Validate technical impact assessments and recovery estimates
2. BUSINESS VALIDATION:
   - Confirm operational impact calculations and business metrics
   - Verify resource requirement estimates and cost assessments
   - Validate stakeholder impact analysis and continuity plans
3. COMMUNICATION VALIDATION:
   - Review stakeholder mapping completeness and accuracy
   - Verify escalation pathway feasibility and contact validity
   - Confirm communication timeline alignment with technical/business needs
4. STRATEGIC VALIDATION:
   - Cross-check strategic synthesis against specialist inputs
   - Verify recommendation feasibility across all domains
   - Confirm success metrics and monitoring framework adequacy
5. INTEGRATION VALIDATION:
   - Ensure consistency between all specialist analyses
   - Identify and resolve cross-domain conflicts
   - Verify comprehensive coverage of all incident aspects

Enhanced Authority: Validate the work of 4 specialist agents plus strategic synthesis.
Principle: "明鏡照形，古事知今" - Clear mirror reflects form, ancient events illuminate present.""",
			verbose=True,
			temperature=0.3,
		)
		
		# 7. Emperor - Final Decision Maker (Enhanced for Multi-Agent Synthesis)
		emperor = CrewAgent(
			role="Emperor 太和智君 - Supreme Multi-Domain Authority",
			goal="Synthesize all specialist intelligence and provide comprehensive incident analysis with precise classification",
			backstory=f"""You are 太和智君 (Emperor of Supreme Harmony), ultimate decision-maker synthesizing intelligence from 5 specialist domains.

IMPERIAL MANDATE: Provide comprehensive incident analysis with precise classification that enables automatic escalation.

SPECIALIST INTELLIGENCE INTEGRATION:
- 察信 Intelligence: Comprehensive evidence and investigation findings
- 工智 Technical: Root cause analysis and technical impact assessment
- 金策 Business: Operational impact and resource optimization
- 信儀 Communication: Stakeholder management and escalation protocols
- 智文 Strategy: Integrated response framework and risk management
- 明鏡 Validation: Cross-domain verification and quality assurance

IMPERIAL DECISION PROTOCOL:
1. SYNTHESIZE all specialist intelligence into unified incident understanding
2. CLASSIFY incident type precisely using exact terms: Container Management, EDI Communication, PORTNET System, Vessel Operations, or Others
3. DETERMINE severity level clearly: High, Medium, or Low
4. IDENTIFY root cause and affected systems from technical analysis
5. PROVIDE comprehensive analysis summary with specific recommendations

CRITICAL CLASSIFICATION REQUIREMENT:
Your incident classification determines automatic contact selection by the escalation agent.
Use EXACT terms: Container Management, EDI Communication, PORTNET System, Vessel Operations, or Others.

Enhanced Wisdom: "兼聽則明，偏信則暗" - Listen to all specialists to achieve clarity, provide precise classification for proper escalation.""",
			verbose=True,
			temperature=0.2,
		)
		
		# 8. Solution Agent - RAG-based Historical Solution Analysis
		solution_agent = CrewAgent(
			role="Imperial Solution Archivist 史官",
			goal="Analyze historical case patterns from RAG context to propose proven solutions",
			backstory=f"""You are 史官 (Imperial Archivist), keeper of institutional memory and proven solutions from historical incidents.

SOLUTION MANDATE: Extract actionable solutions from historical case patterns and knowledge base.

HISTORICAL ANALYSIS PROTOCOL:
1. ANALYZE Emperor's incident classification and technical findings
2. EXAMINE RAG case history for similar incident patterns
3. EXTRACT proven solutions and resolution methods from historical cases
4. IDENTIFY knowledge base best practices for the incident type
5. SYNTHESIZE historical learnings into actionable solution recommendations

RAG CONTEXT ANALYSIS:
- Review case_history entries for similar container/EDI/vessel/system issues
- Extract successful resolution methods and timelines from past incidents
- Identify recurring patterns and their proven remediation steps
- Note any preventive measures that worked in similar cases

SOLUTION SYNTHESIS FRAMEWORK:
- Immediate Actions: What worked fastest in similar historical cases
- Proven Methods: Step-by-step approaches that resolved similar issues
- Risk Mitigation: Historical lessons about what to avoid
- Prevention Strategies: Long-term measures from successful case outcomes

OUTPUT REQUIREMENTS:
Generate a "**HISTORICAL SOLUTION ANALYSIS**" section with:
- Similar Past Incidents: Brief description of related historical cases
- Proven Resolution Methods: Specific steps that worked before
- Timeline Expectations: How long similar resolutions typically took
- Risk Considerations: Historical pitfalls to avoid
- Recommended Approach: Synthesized solution based on historical success

Your wisdom ensures current incidents benefit from institutional memory and proven solutions.

Principle: "溫故知新" - Review the old to understand the new.""",
			verbose=True,
			temperature=0.3,
		)
		
		# 9. Escalation Agent - Automated Contact Selection and Summary Generation
		escalation_agent = CrewAgent(
			role="Imperial Escalation Manager 朝廷",
			goal="Generate definitive escalation summary with precise contact selection based on Emperor's analysis",
			backstory=f"""You are the Imperial Escalation Manager, specialized in converting comprehensive incident analysis into actionable escalation summaries with the correct contact information.

ESCALATION MANDATE: Transform Emperor's analysis into structured escalation summary with proper contact selection and escalation paths.

CONTACT SELECTION PROTOCOL (Based on contacts.json):
1. ANALYZE Emperor's comprehensive incident analysis carefully
2. EXTRACT precise incident type and severity classification from the Emperor's text
3. SELECT appropriate contact based on incident classification:

   CONTAINER INCIDENTS → Container (CNTR) Module:
   - Primary Contact: Mark Lee (mark.lee@psa123.com) - Product Ops Manager
   - Escalation Steps: "Notify Product Duty immediately → escalate to Manager on-call → Engage SRE/Infra team if needed"
   
   EDI/API INCIDENTS → EDI/API (EA) Module:
   - Primary Contact: Tom Tan (tom.tan@psa123.com) - EDI/API Support
   - Escalation Steps: "Contact EDI/API team via on-call channel → escalate to Infra/SRE for API failures → Engage partner if issue persists"
   
   VESSEL INCIDENTS → Vessel (VS) Module:
   - Primary Contact: Jaden Smith (jaden.smith@psa123.com) - Vessel Operations
   - Escalation Steps: "Notify Vessel Duty team → escalate to Senior Ops Manager → Engage Vessel Static team for further diagnostics"
   
   GENERAL/INFRASTRUCTURE INCIDENTS → Others Module:
   - Primary Contact: Jacky Chan (jacky.chan@psa123.com) - Infra/SRE Support Lead
   - Escalation Steps: "Engage Infra team immediately for system errors → Escalate to Jacky Chan (SRE) for urgent cases"

OUTPUT FORMAT REQUIREMENTS:
- Incident ID: Generate format INC-YYYYMMDD-HHMMSS
- Incident Type: Use exact classification from Emperor's analysis
- Severity Level: High/Medium/Low from Emperor's analysis
- Primary Contact: Specific person with email from contacts.json
- Summary: Technical root cause + business impact + recommended actions + historical solution
- Timeline: Immediate, short-term, and long-term actions
- Escalation Path: Use exact escalation steps from contacts.json for the module

CRITICAL: Use ONLY the contacts and escalation paths defined in contacts.json. Do NOT invent contacts like "Robert Wong" or "Sarah Chen" that don't exist.

Your role ensures Emperor's analysis becomes actionable escalation with the correct contact and proper escalation procedures.

Principle: "令出如山，責任到人" - Orders must be clear as mountains, responsibility assigned to specific individuals.""",
			verbose=True,
			temperature=0.1,
		)

		logger.info("📋 Creating comprehensive multi-agent task workflow...")

		# Create multi-phase task workflow with 6 specialized agents
		
		# Phase 1: Intelligence Gathering
		intelligence_task = CrewTask(
			description=f"""INTELLIGENCE GATHERING MISSION: Comprehensive evidence collection and initial investigation.

INCIDENT TEXT:
{incident_text}

MANDATORY INVESTIGATION PROTOCOL:
1. SYSTEM BASELINE ASSESSMENT:
   - Execute tools.get_operational_overview() for current system state
   - Execute tools.check_system_health() for error rates and stability metrics
   
2. INCIDENT CLASSIFICATION AND KEYWORD EXTRACTION:
   - Analyze incident text for technical keywords (container, EDI, vessel, API, system)
   - Classify incident type based on content and affected systems
   
3. TARGETED EVIDENCE COLLECTION:
   Based on incident classification, execute appropriate database queries:
   - Container incidents: tools.search_containers() + tools.get_container_details() 
   - EDI/API incidents: tools.analyze_edi_messages() + tools.get_recent_edi_activity()
   - Vessel incidents: tools.get_vessel_details() with relevant vessel information
   - System incidents: Deep dive tools.check_system_health() analysis
   
4. PATTERN INVESTIGATION:
   - Execute tools.search_recent_incidents() with incident-specific keywords
   - Analyze historical patterns in last 12-48 hours
   - Identify if incident is isolated, pattern-based, or systematic
   
5. EVIDENCE COMPILATION:
   - Compile complete factual dossier with all database evidence
   - Organize findings by system, timeline, and impact
   - Prepare evidence package for specialist analysis

DELIVERABLE: Comprehensive evidence dossier with all relevant database findings, system baseline, and pattern analysis.""",
			expected_output="Complete evidence dossier including system baseline, targeted investigation results, pattern analysis, and organized factual findings ready for specialist analysis",
			agent=intelligence_agent,
		)
		
		# Phase 2A: Technical Analysis (Parallel)
		technical_task = CrewTask(
			description=f"""TECHNICAL ANALYSIS MISSION: Deep technical investigation and root cause analysis.

PREREQUISITES: Receive evidence dossier from Intelligence Gathering Agent (察信).

TECHNICAL INVESTIGATION FRAMEWORK:
1. EVIDENCE REVIEW:
   - Analyze all technical evidence collected by Intelligence Agent
   - Identify technical systems and components involved
   - Review error patterns and system health indicators
   
2. ROOT CAUSE ANALYSIS:
   - Reconstruct incident timeline using database timestamps
   - Map dependencies between affected systems (EDI ↔ TOS ↔ PORTNET)
   - Analyze error correlation across multiple components
   - Identify primary failure point and cascading effects
   
3. TECHNICAL IMPACT ASSESSMENT:
   - Quantify current operational impact using metrics from evidence
   - Assess downstream risks to interconnected systems
   - Estimate recovery complexity and technical resource requirements
   - Evaluate system stability and risk of further degradation
   
4. TECHNICAL RESPONSE RECOMMENDATIONS:
   - Immediate technical actions to contain/resolve incident
   - System restoration procedures and sequence
   - Technical monitoring requirements during recovery
   - Preventive measures to avoid recurrence

DELIVERABLE: Technical analysis report with root cause, impact assessment, and technical response plan.""",
			expected_output="Comprehensive technical analysis including root cause identification, impact quantification, recovery complexity assessment, and technical response recommendations",
			agent=technical_agent,
		)
		
		# Phase 2B: Business Impact Analysis (Parallel) 
		business_task = CrewTask(
			description=f"""BUSINESS IMPACT ANALYSIS MISSION: Operational impact assessment and resource optimization.

PREREQUISITES: Receive evidence dossier from Intelligence Gathering Agent (察信).

BUSINESS ANALYSIS FRAMEWORK:
1. OPERATIONAL IMPACT ASSESSMENT:
   - Analyze which port operations are affected and severity levels
   - Assess customer/stakeholder impact (internal teams, external clients)
   - Quantify performance degradation using operational metrics
   - Evaluate resource utilization vs capacity constraints
   
2. BUSINESS CONTINUITY EVALUATION:
   - Identify available workarounds and alternative processes
   - Assess feasibility of temporary operational procedures
   - Prioritize service restoration based on business criticality
   - Evaluate compliance and regulatory implications
   
3. RESOURCE OPTIMIZATION ANALYSIS:
   - Determine personnel resource requirements for resolution
   - Assess system resource reallocation opportunities  
   - Estimate budget impact and cost optimization options
   - Evaluate vendor/contractor resource needs
   
4. STRATEGIC IMPACT ASSESSMENT:
   - Analyze long-term operational risks
   - Assess stakeholder relationship implications
   - Evaluate reputation and service level impacts
   - Recommend strategic communication approaches

DELIVERABLE: Business impact analysis with operational effects, continuity options, resource requirements, and strategic implications.""",
			expected_output="Comprehensive business analysis including operational impact quantification, continuity planning, resource optimization, and strategic implications assessment",
			agent=business_agent,
		)
		
		# Phase 2C: Communication Strategy (Parallel)
		communication_task = CrewTask(
			description=f"""COMMUNICATION COORDINATION MISSION: Stakeholder management and escalation pathway design.

PREREQUISITES: Receive evidence dossier from Intelligence Gathering Agent (察信).

COMMUNICATION STRATEGY FRAMEWORK:
1. STAKEHOLDER MAPPING:
   - Map all internal stakeholders (technical teams, operations, management)
   - Identify external parties (customers, vendors, regulatory bodies)
   - Classify contacts by priority and authority level (using contacts.json reference)
   - Determine communication dependencies and approval chains
   
2. COMMUNICATION STRATEGY DESIGN:
   - Craft appropriate messages for different audience types
   - Design communication timing and frequency optimization
   - Select optimal channels (email, phone, emergency alerts, dashboards)
   - Plan progressive disclosure based on incident evolution
   
3. ESCALATION PATHWAY FRAMEWORK:
   - Design escalation triggers and timeline thresholds
   - Map authority levels required for different decision types
   - Establish emergency bypass procedures for critical situations
   - Define escalation handoff protocols between teams
   
4. COORDINATION REQUIREMENTS:
   - Plan cross-team synchronization and status sharing
   - Schedule regular status update cycles
   - Design resolution confirmation and communication closure protocols
   - Establish feedback loops for communication effectiveness

DELIVERABLE: Communication strategy with stakeholder mapping, escalation pathways, and coordination protocols.""",
			expected_output="Comprehensive communication plan including stakeholder mapping, escalation pathway design, message strategy, and coordination protocols for effective incident management",
			agent=communication_agent,
		)
		
		# Phase 3: Strategic Synthesis
		strategic_task = CrewTask(
			description=f"""STRATEGIC SYNTHESIS MISSION: Integrate all specialist intelligence into unified response strategy.

PREREQUISITES: Receive analysis from Technical, Business, and Communication specialists.

STRATEGIC INTEGRATION FRAMEWORK:
1. MULTI-DOMAIN INTELLIGENCE INTEGRATION:
   - Synthesize technical root cause with business impact assessment
   - Integrate communication requirements with technical/business timelines
   - Resolve conflicts between specialist recommendations
   - Identify strategic patterns across all analysis domains
   
2. COMPREHENSIVE RESPONSE STRATEGY:
   - Design multi-phase response plan coordinating all domains
   - Optimize resource allocation across technical, operational, and communication needs
   - Synchronize timelines between technical recovery and business continuity
   - Balance immediate response with long-term strategic considerations
   
3. RISK MANAGEMENT INTEGRATION:
   - Synthesize risks identified across technical, business, and communication domains
   - Develop contingency plans for multiple scenario progressions
   - Design comprehensive monitoring framework covering all aspects
   - Establish success metrics spanning technical, operational, and stakeholder dimensions
   
4. DECISION SUPPORT PREPARATION:
   - Present integrated options with multi-domain trade-off analysis
   - Prioritize recommendations based on cross-domain impact assessment
   - Assess implementation feasibility across all specialist areas
   - Prepare comprehensive briefing for Emperor's final decision

DELIVERABLE: Integrated strategic response framework ready for imperial validation and decision.""",
			expected_output="Comprehensive strategic synthesis integrating technical, business, and communication analysis into unified response strategy with prioritized recommendations and implementation roadmap",
			agent=secretariat_strategy,
		)
		
		# Phase 4: Quality Validation
		validation_task = CrewTask(
			description=f"""MULTI-DOMAIN VALIDATION MISSION: Comprehensive verification across all specialist analyses.

PREREQUISITES: Receive strategic synthesis and all specialist analyses.

VALIDATION FRAMEWORK:
1. TECHNICAL VALIDATION:
   - Verify database evidence accuracy and technical analysis logic
   - Confirm root cause analysis methodology and supporting data
   - Validate technical impact assessments and recovery estimates
   - Cross-check technical recommendations against system capabilities
   
2. BUSINESS VALIDATION:
   - Confirm operational impact calculations and business metrics accuracy
   - Verify resource requirement estimates and feasibility
   - Validate stakeholder impact analysis and continuity plan viability
   - Check business recommendations against organizational constraints
   
3. COMMUNICATION VALIDATION:
   - Review stakeholder mapping completeness and contact accuracy
   - Verify escalation pathway feasibility and authority alignment
   - Confirm communication timeline synchronization with technical/business plans
   - Validate message strategy appropriateness for different audiences
   
4. STRATEGIC VALIDATION:
   - Cross-check strategic synthesis against all specialist inputs
   - Verify recommendation integration and conflict resolution
   - Confirm comprehensive coverage of all incident aspects
   - Validate success metrics and monitoring framework adequacy
   
5. INTEGRATION QUALITY ASSURANCE:
   - Ensure consistency across all specialist analyses
   - Identify any remaining gaps or conflicts
   - Verify feasibility of integrated response plan
   - Confirm readiness for imperial decision-making

DELIVERABLE: Comprehensive validation report confirming analysis quality and strategic readiness.""",
			expected_output="Multi-domain validation report confirming technical accuracy, business feasibility, communication viability, strategic integration quality, and overall readiness for final imperial decision",
			agent=secretariat_review,
		)
		
		# Phase 5: Imperial Decision
		decision_task = CrewTask(
			description=f"""IMPERIAL DECISION MISSION: Synthesize all specialist intelligence into comprehensive incident analysis.

PREREQUISITES: Receive validated strategic synthesis and all specialist intelligence.

IMPERIAL SYNTHESIS PROTOCOL:
1. COMPREHENSIVE INTELLIGENCE REVIEW:
   - Synthesize evidence from Intelligence Gathering (察信)
   - Integrate technical analysis from Technical Expert (工智)
   - Consider business impact from Business Analyst (金策)
   - Incorporate communication strategy from Protocol Master (信儀)
   - Review strategic framework from Strategy Minister (智文)
   - Validate against quality review from Validation Authority (明鏡)

2. INCIDENT CLASSIFICATION (CRITICAL):
   - Classify incident type precisely: Container Management, EDI Communication, PORTNET System, Vessel Operations, or Others
   - Determine severity level: High, Medium, or Low based on impact analysis
   - Identify root cause and affected systems from technical analysis
   - State classification clearly using exact terms above

3. COMPREHENSIVE ANALYSIS SUMMARY:
   - Provide detailed incident description based on all agent findings
   - Include technical root cause analysis from 工智
   - Include business impact assessment from 金策  
   - Include stakeholder communication plan from 信儀
   - Include strategic response framework from 智文
   - Include validation findings from 明鏡

4. STRUCTURED OUTPUT REQUIREMENTS:
   - State incident type clearly (use exact classification terms)
   - State severity level clearly (High/Medium/Low)
   - Provide comprehensive analysis summary
   - Include recommended actions and timelines

CRITICAL: Use precise classification terms as this determines escalation routing by the Escalation Manager.

Previous findings from specialist agents will be provided by the CrewAI workflow execution.""",
			expected_output="Comprehensive incident analysis with precise classification (Container Management/EDI Communication/PORTNET System/Vessel Operations/Others), severity level (High/Medium/Low), detailed findings from all agents, recommended actions, and timelines.",
			agent=emperor,
		)
		
		# Phase 6: Historical Solution Analysis
		solution_task = CrewTask(
			description=f"""HISTORICAL SOLUTION ANALYSIS MISSION: Extract proven solutions from RAG case history and knowledge base.

PREREQUISITES: Receive Emperor's comprehensive incident analysis with classification and RAG context.

SOLUTION ANALYSIS PROTOCOL:
1. INCIDENT CONTEXT ANALYSIS:
   - Review Emperor's incident classification and technical findings
   - Extract key incident characteristics (type, severity, systems affected)
   - Identify critical failure points and business impact areas

2. RAG CASE HISTORY EXAMINATION:
   - Analyze case_history entries for similar incident patterns
   - Look for incidents with matching keywords, systems, or failure modes
   - Extract successful resolution methods and their outcomes
   - Note resolution timelines and resource requirements from past cases

3. KNOWLEDGE BASE SYNTHESIS:
   - Review knowledge_base entries for best practices related to incident type
   - Extract standard procedures and recommended approaches
   - Identify preventive measures and long-term solutions

4. HISTORICAL PATTERN ANALYSIS:
   - Identify recurring incident patterns and their proven solutions
   - Extract lessons learned about what works and what doesn't
   - Analyze resolution timelines and success rates from historical data
   - Note any escalation patterns or resource requirements

5. SOLUTION RECOMMENDATION SYNTHESIS:
   - Combine historical success patterns with current incident specifics
   - Prioritize solutions based on historical success rates and current context
   - Include risk considerations based on past experiences
   - Provide realistic timeline expectations based on historical data

DELIVERABLE: Historical solution analysis with proven approaches, timeline expectations, and risk considerations based on institutional memory.""",
			expected_output="Comprehensive historical solution analysis including similar past incidents, proven resolution methods, timeline expectations, risk considerations, and recommended approach based on RAG case history and knowledge base patterns.",
			agent=solution_agent,
		)
		
		# Phase 7: Escalation Summary Generation
		escalation_task = CrewTask(
			description=f"""ESCALATION SUMMARY MISSION: Generate definitive escalation summary with precise contact selection and proper escalation paths.

PREREQUISITES: Receive Emperor's comprehensive incident analysis and Historical Solution Analysis.

ESCALATION GENERATION PROTOCOL:
1. ANALYSIS INTEGRATION:
   - Extract precise incident type from Emperor's analysis text
   - Extract severity level (High/Medium/Low) from impact assessment
   - Extract technical root cause and affected systems
   - Extract business impact and operational effects
   - Incorporate historical solution analysis and proven approaches

2. CONTACT SELECTION (Based on contacts.json):
   Container incidents → Container (CNTR) Module:
   - Primary: Mark Lee (mark.lee@psa123.com) - Product Ops Manager
   - Escalation: "Notify Product Duty immediately → escalate to Manager on-call → Engage SRE/Infra team if needed"
   
   EDI/API incidents → EDI/API (EA) Module:
   - Primary: Tom Tan (tom.tan@psa123.com) - EDI/API Support
   - Escalation: "Contact EDI/API team via on-call channel → escalate to Infra/SRE for API failures → Engage partner if issue persists"
   
   Vessel incidents → Vessel (VS) Module:
   - Primary: Jaden Smith (jaden.smith@psa123.com) - Vessel Operations
   - Escalation: "Notify Vessel Duty team → escalate to Senior Ops Manager → Engage Vessel Static team for diagnostics"
   
   Infrastructure/General incidents → Others Module:
   - Primary: Jacky Chan (jacky.chan@psa123.com) - Infra/SRE Support Lead
   - Escalation: "Engage Infra team immediately → Escalate to Jacky Chan (SRE) for urgent cases"

3. COMPREHENSIVE ESCALATION SUMMARY:
   Generate structured summary including:
   
   **INCIDENT ESCALATION SUMMARY**
   - Incident ID: INC-[YYYYMMDD-HHMMSS]
   - Incident Type: [From Emperor's classification]
   - Severity: [High/Medium/Low from analysis]
   - Primary Contact: [Correct person from contacts.json]
   
   **INCIDENT DETAILS:**
   [Emperor's technical analysis and root cause]
   
   **BUSINESS IMPACT:**
   [Operational effects and stakeholder impact]
   
   **HISTORICAL SOLUTION ANALYSIS:**
   [Include solution agent's findings about proven approaches]
   
   **RECOMMENDED ACTIONS:**
   - Immediate: [From Emperor's recommendations + historical proven methods]
   - Short-term: [Recovery steps + historical best practices]
   - Long-term: [Prevention measures + lessons learned]
   
   **ESCALATION PATH:**
   [Use exact escalation steps from contacts.json for the specific module]

4. QUALITY REQUIREMENTS:
   - Use ONLY contacts from contacts.json (Mark Lee, Tom Tan, Jaden Smith, Jacky Chan)
   - Use exact escalation steps from contacts.json for each module
   - Include historical solution analysis in the summary
   - Include ALL critical information from Emperor's analysis
   - Ensure professional formatting and clear action items

CRITICAL: Do NOT create fictional contacts. Use only the 4 real contacts from contacts.json.

Previous analysis from Emperor and Historical Solution Agent provides all needed context.""",
			expected_output="Professional escalation summary with specific contact person from contacts.json, incident details, business impact, historical solution analysis, recommended actions with timeline, and proper escalation procedures from contacts.json. Must include actual person name and email address based on incident type classification.",
			agent=escalation_agent,
		)

		logger.info("🏛️ Assembling Expanded Imperial Court crew with 8 agents and 7-phase workflow...")
		crew = Crew(
			agents=[
				intelligence_agent,     # Phase 1: Evidence gathering
				technical_agent,        # Phase 2A: Technical analysis  
				business_agent,         # Phase 2B: Business analysis
				communication_agent,    # Phase 2C: Communication strategy
				secretariat_strategy,   # Phase 3: Strategic synthesis
				secretariat_review,     # Phase 4: Multi-domain validation
				emperor,                # Phase 5: Imperial decision
				solution_agent,         # Phase 6: Historical solution analysis
				escalation_agent        # Phase 7: Escalation summary generation
			], 
			tasks=[
				intelligence_task,      # 1. Evidence collection
				technical_task,         # 2A. Technical deep dive
				business_task,          # 2B. Business impact
				communication_task,     # 2C. Communication strategy  
				strategic_task,         # 3. Strategic synthesis
				validation_task,        # 4. Quality validation
				decision_task,          # 5. Imperial decision
				solution_task,          # 6. Historical solution analysis
				escalation_task         # 7. Escalation summary generation
			],
			verbose=True
		)
		
		logger.info("🚀 INITIATING EXPANDED CREWAI WORKFLOW EXECUTION...")
		logger.info("   Phase 1: 察信 (Intelligence) - Comprehensive evidence gathering")
		logger.info("   Phase 2A: 工智 (Technical) - Deep technical analysis and root cause")
		logger.info("   Phase 2B: 金策 (Business) - Operational impact and resource assessment")
		logger.info("   Phase 2C: 信儀 (Communication) - Stakeholder management and escalation design")
		logger.info("   Phase 3: 智文 (Strategic) - Multi-domain synthesis and integration")
		logger.info("   Phase 4: 明鏡 (Validation) - Comprehensive quality validation")
		logger.info("   Phase 5: 太和智君 (Emperor) - Final decision and comprehensive analysis")
		logger.info("   Phase 6: 史官 (Solution Archivist) - Historical solution analysis from RAG context")
		logger.info("   Phase 7: 朝廷 (Escalation Manager) - Automated escalation summary with proper contacts")
		
		try:
			result_text = crew.kickoff()
			logger.info("✅ CREWAI WORKFLOW COMPLETED SUCCESSFULLY")
			logger.info(f"📜 Final Result Length: {len(str(result_text))} characters")
			
			# The escalation agent should have generated the proper escalation summary
			logger.info("🎫 Escalation summary generated by specialized agent")
			
			# Parse result to extract escalation information if structured properly
			# The result_text should now contain the escalation summary from the escalation agent
			result_str = str(result_text)
			
			# Extract basic information for response structure (fallback parsing)
			incident_type = "General"
			severity = "Medium"
			
			# Simple extraction for response structure - agent should handle details
			if "container" in result_str.lower():
				incident_type = "Container Management" 
			elif "edi" in result_str.lower():
				incident_type = "EDI Communication"
			elif "portnet" in result_str.lower():
				incident_type = "PORTNET System"
			elif "vessel" in result_str.lower():
				incident_type = "Vessel Operations"
			
			if "high" in result_str.lower():
				severity = "High"
			elif "low" in result_str.lower():
				severity = "Low"
			
			logger.info(f"   📋 Final classification: {incident_type} with {severity} severity")
			
			return {
				"emperor": AGENTS["emperor"]["name"],
				"incident_analysis": {
					"incident_type": incident_type,
					"severity": severity,
					"original_text": incident_text,
					"crew_analysis_used": True
				},
				"rag_results": {
					"case_history_count": len(rag_context.get("case_history", [])),
					"knowledge_base_count": len(rag_context.get("knowledge_base", [])),
					"case_history": rag_context.get("case_history", []),
					"knowledge_base": rag_context.get("knowledge_base", [])
				},
				"crew_output": str(result_text),
				"contact_information": {"generated_by": "escalation_agent"},
				"ticket_priority": f"P{'1' if severity == 'High' else '2' if severity == 'Medium' else '3'}",
				"workflow_phases": 7
			}
		except Exception as e:
			logger.error(f"❌ CrewAI execution failed: {e}")
			logger.warning("🔄 Falling back to mock mode...")
			# Fallback to mock if CrewAI fails
			return self._mock_run(incident)
