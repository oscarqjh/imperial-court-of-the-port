from typing import Dict, Any

# Placeholders for agent definitions; later we can wire CrewAI Agent objects

AGENTS: Dict[str, Dict[str, Any]] = {
	"emperor": {
		"name": "太和智君",
		"role": "The Sage of Supreme Harmony",
	},
	"grand_secretariat_strategy": {
		"name": "智文",
		"org": "中書省",
	},
	"grand_secretariat_review": {
		"name": "明鏡",
		"org": "門下省",
	},
	"ministry_personnel": {"name": "行吏", "org": "吏部"},
	"ministry_finance": {"name": "金策", "org": "戶部"},
	"ministry_protocol": {"name": "信儀", "org": "禮部"},
	"ministry_defense": {"name": "安戍", "org": "兵部"},
	"ministry_justice": {"name": "清律", "org": "刑部"},
	"ministry_works": {"name": "工智", "org": "工部"},
	"censorate_chief": {"name": "公衡", "org": "御史中丞"},
	"censorate_field": {"name": "察信", "org": "監察御史"},
	"governor_south": {"name": "南策", "org": "江南總督"},
	"governor_north": {"name": "北衡", "org": "北直隸總督"},
	"eunuch_scribe": {"name": "筆宦"},
	"eunuch_messenger": {"name": "報宦"},
	"eunuch_maintenance": {"name": "維宦"},
	"eunuch_sentinel": {"name": "警宦"},
	"guard_cyber": {"name": "金衛"},
	"guard_internal": {"name": "銀衛"},
	"maid_data": {"name": "芳侍"},
}
