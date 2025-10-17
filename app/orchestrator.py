import os
from typing import Dict, Any

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

	def run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		if not self.crewai_available:
			logger.info("Running in MOCK_MODE; returning synthesized results")
			return self._mock_run(incident)
		return self._crewai_run(incident)

	def _mock_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		strategy = f"Secretariat(智文) synthesizes inputs for {incident.get('incident_type')}"
		review = "門下省(明鏡) validates policy and ethics"
		decision = "太和智君 approves resource allocation and response"
		try:
			recent = list_recent_edi_messages(5)
			recent_edi = [{"message_type": r.get("message_type"), "sent_at": r.get("sent_at")} for r in recent]
		except Exception:
			recent_edi = []
		return {
			"emperor": AGENTS["emperor"]["name"],
			"steps": [strategy, review, decision],
			"recent_edi": recent_edi,
			"recommendations": [
				"Deploy 安戍 to contain incident",
				"工智 to apply fix and auto-heal",
				"清律 to propose prevention policy",
			],
		}

	def _crewai_run(self, incident: Dict[str, Any]) -> Dict[str, Any]:
		emperor = CrewAgent(
			role="Emperor 太和智君",
			goal="Make final decision for port incidents",
			backstory="Central decision-maker optimizing long-term resilience",
			temperature=0.2,
		)
		secretariat_strategy = CrewAgent(
			role="中書省 智文",
			goal="Synthesize reports into concise advisories",
			backstory="Coordinates ministries to produce strategy brief",
			temperature=0.4,
		)
		secretariat_review = CrewAgent(
			role="門下省 明鏡",
			goal="Policy review and ethical reasoning",
			backstory="Ensures transparency and correctness",
			temperature=0.3,
		)

		strategy_task = CrewTask(
			description=f"Analyze incident: {incident}",
			expected_output="A concise advisory with recommended ministries and actions",
			agent=secretariat_strategy,
		)
		review_task = CrewTask(
			description="Review the advisory for risks, costs, and ethics; suggest refinements",
			expected_output="A reviewed plan with risk notes",
			agent=secretariat_review,
		)
		decision_task = CrewTask(
			description="Make the final decision and structured response plan",
			expected_output="JSON-like structured plan with steps, recommended agents, and rationale",
			agent=emperor,
		)

		crew = Crew(agents=[secretariat_strategy, secretariat_review, emperor], tasks=[strategy_task, review_task, decision_task])
		result_text = crew.kickoff()
		return {"emperor": AGENTS["emperor"]["name"], "crew_output": str(result_text)}
