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
		
		# Simple keyword-based analysis for mock mode
		incident_type = "General"
		severity = "Medium"
		
		text_lower = incident_text.lower()
		if "email" in text_lower or "alr-" in text_lower:
			incident_type = "Email System"
		elif "container" in text_lower or "duplicate" in text_lower:
			incident_type = "Container Management"
		elif "portnet" in text_lower:
			incident_type = "PORTNET System"
		
		if "urgent" in text_lower or "critical" in text_lower:
			severity = "High"
		elif "low" in text_lower or "minor" in text_lower:
			severity = "Low"
		
		strategy = f"智文 analyzes {incident_type} incident with severity {severity}"
		review = f"明鏡 reviews policy for {incident_type} incidents using knowledge base"
		decision = f"太和智君 decides on resource allocation for {severity} priority incident"
		
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
				"original_text": incident_text
			},
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
				f"工智 to apply fix based on {len(rag_context.get('case_history', []))} similar cases",
				f"清律 to update policy using {len(rag_context.get('knowledge_base', []))} KB references",
			],
		}

	def _crewai_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		incident_text = incident.get("incident_text", "")
		rag_context = incident.get("rag_context", {})
		
		# Create agents with enhanced context
		emperor = CrewAgent(
			role="Emperor 太和智君",
			goal="Make final decision for port incidents based on analysis and historical precedent",
			backstory="Central decision-maker optimizing long-term resilience, reviews all ministry inputs and RAG context",
			verbose=True,
			temperature=0.2,
		)
		
		secretariat_strategy = CrewAgent(
			role="中書省 智文 - Strategic Analysis",
			goal="Analyze incident text to determine type, severity, and synthesize strategy using case history",
			backstory=f"Coordinates analysis using {len(rag_context.get('case_history', []))} similar historical cases",
			verbose=True,
			temperature=0.4,
		)
		
		secretariat_review = CrewAgent(
			role="門下省 明鏡 - Policy Review", 
			goal="Review analysis using knowledge base and ensure proper protocol adherence",
			backstory=f"Reviews policy compliance using {len(rag_context.get('knowledge_base', []))} knowledge base references",
			verbose=True,
			temperature=0.3,
		)

		# Create tasks with RAG context
		analysis_task = CrewTask(
			description=f"""Analyze this incident and determine type and severity:

INCIDENT TEXT:
{incident_text}

SIMILAR HISTORICAL CASES:
{rag_context.get('case_history_summary', 'No similar cases found')}

Tasks:
1. Classify incident type (e.g., Email System, Container Management, Network, Authentication)
2. Determine severity (High/Medium/Low) 
3. Recommend initial response strategy based on historical cases
4. Provide structured analysis in JSON format""",
			expected_output="JSON with incident_type, severity, analysis, and recommended_actions based on historical precedent",
			agent=secretariat_strategy,
		)
		
		review_task = CrewTask(
			description=f"""Review the incident analysis using knowledge base guidance:

KNOWLEDGE BASE GUIDANCE:
{rag_context.get('knowledge_base_summary', 'No relevant knowledge base entries found')}

Tasks:
1. Validate the incident classification against knowledge base
2. Check if recommended actions follow established protocols
3. Identify any policy gaps or improvements needed
4. Suggest refinements to the response plan""",
			expected_output="Policy review with validation notes, compliance check, and refined recommendations",
			agent=secretariat_review,
		)
		
		decision_task = CrewTask(
			description="""Make final decision on incident response:

Tasks:
1. Synthesize analysis and review into comprehensive response plan
2. Assign specific ministries/agents for execution  
3. Set priority and resource allocation
4. Provide structured response with clear action items""",
			expected_output="Final structured response plan with assigned agents, priorities, and action timeline",
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
