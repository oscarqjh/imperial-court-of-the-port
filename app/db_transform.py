from __future__ import annotations

import re


def transform_mysql_to_postgres(sql: str) -> str:
	# Remove database/session directives
	sql = re.sub(r"(?im)^\s*CREATE\s+DATABASE[\s\S]*?;\s*", "", sql)
	sql = re.sub(r"(?im)^\s*USE\s+\w+;\s*", "", sql)
	sql = re.sub(r"(?im)^\s*SET\s+FOREIGN_KEY_CHECKS\s*=\s*\d+;\s*", "", sql)

	# Remove ENGINE and trailing table options
	sql = re.sub(r"(?i)\)\s*ENGINE=InnoDB;", ") ;", sql)

	# Types and functions
	sql = re.sub(r"(?i)\bMEDIUMTEXT\b", "TEXT", sql)
	sql = re.sub(r"(?i)\bDATETIME\b", "TIMESTAMP", sql)
	sql = re.sub(r"(?i)\bJSON\b", "JSONB", sql)
	sql = re.sub(r"(?i)\bENUM\([^)]*\)", "TEXT", sql)
	sql = re.sub(r"(?i)\bUNSIGNED\b", "", sql)
	sql = re.sub(r"(?i)JSON_OBJECT\s*\(", "jsonb_build_object(", sql)
	sql = re.sub(r"(?i)NOW\s*\(\s*\)", "now()", sql)
	sql = re.sub(r"(?i)INTERVAL\s+1\s+SECOND", "interval '1 second'", sql)

	# AUTO_INCREMENT fields → SERIAL types
	def _auto_inc_repl(match: re.Match[str]) -> str:
		col = match.group(1)
		return f"{col} BIGSERIAL"

	sql = re.sub(r"(?i)\b(\w+)\b\s+BIGINT\s+AUTO_INCREMENT", _auto_inc_repl, sql)
	sql = re.sub(r"(?i)\b(\w+)\b\s+BIGINT\s+PRIMARY\s+KEY\s+AUTO_INCREMENT", lambda m: f"{m.group(1)} BIGSERIAL PRIMARY KEY", sql)

	# Drop inline KEY/INDEX definitions (robust)
	sql = re.sub(r"(?im)^\s*KEY\s+[^\n]*\n?", "", sql)
	# Convert UNIQUE KEY to UNIQUE and keep
	sql = re.sub(r"(?im)^\s*UNIQUE\s+KEY\s+([^(\s]+)\s*\(([^)]*)\)\s*,?\s*$", lambda m: f"UNIQUE ({m.group(2)})", sql)
	# Ensure UNIQUE lines end with a comma if followed by more table elements
	sql = re.sub(r"(?m)^(\s*UNIQUE\s*\([^\)]+\))\s*$", r"\1,", sql)

	# Convert MySQL generated columns to PostgreSQL GENERATED ALWAYS AS
	# e.g.,  col VARCHAR(20) AS (expr) STORED  ->  col VARCHAR(20) GENERATED ALWAYS AS (expr) STORED
	sql = re.sub(r"(?im)^(\s*\w+\s+\w+\s+[^,\n]*?)\sAS\s*\(", r"\1 GENERATED ALWAYS AS (", sql)

	# Views needing rewrite: vw_edi_last using window functions
	if "CREATE VIEW vw_edi_last" in sql:
		sql = re.sub(
			r"(?is)DROP\s+VIEW\s+IF\s+EXISTS\s+vw_edi_last;\s*CREATE\s+VIEW\s+vw_edi_last\s+AS[\s\S]*?;",
			"""
DROP VIEW IF EXISTS vw_edi_last;
CREATE VIEW vw_edi_last AS
WITH last_edi AS (
  SELECT e.container_id, e.message_type, e.status, e.sent_at,
         ROW_NUMBER() OVER (PARTITION BY e.container_id ORDER BY e.sent_at DESC) AS rn
  FROM edi_message e
)
SELECT c.cntr_no,
       l.sent_at AS last_edi_time,
       l.message_type AS last_edi_type,
       l.status AS last_edi_status
FROM last_edi l
JOIN container c ON c.container_id = l.container_id
WHERE l.rn = 1;
;""",
			sql,
		)

	# Clean dangling commas before closing parens
	sql = re.sub(r",\s*\)\s*;", ") ;", sql)

	# Collapse multiple blank lines
	sql = re.sub(r"\n{3,}", "\n\n", sql)
	return sql
