from __future__ import annotations

from typing import List
import re

try:
	import tiktoken  # type: ignore
	ENC = tiktoken.get_encoding("cl100k_base")
except Exception:  # fallback: approximate tokenization by words
	ENC = None


def normalize_whitespace(text: str) -> str:
	text = text.replace("\r", "\n")
	text = re.sub(r"\n{2,}", "\n\n", text)
	text = re.sub(r"[\t ]+", " ", text)
	return text.strip()


def count_tokens(text: str) -> int:
	if ENC is None:
		return max(1, len(text.split()))
	return len(ENC.encode(text))


def smart_chunk(text: str, max_tokens: int = 400, overlap_tokens: int = 60) -> List[str]:
	text = normalize_whitespace(text)
	if count_tokens(text) <= max_tokens:
		return [text]

	# Prefer to split by paragraphs, then sentences
	paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
	chunks: List[str] = []
	current: List[str] = []
	current_tokens = 0

	def flush() -> None:
		nonlocal current, current_tokens
		if not current:
			return
		joined = "\n".join(current).strip()
		if joined:
			chunks.append(joined)
		current = []
		current_tokens = 0

	for para in paragraphs:
		para_tokens = count_tokens(para)
		if para_tokens > max_tokens:
			# split paragraph into sentences heuristically
			sentences = re.split(r"(?<=[.!?])\s+", para)
			for sent in sentences:
				sent = sent.strip()
				if not sent:
					continue
				ts = count_tokens(sent)
				if current_tokens + ts > max_tokens:
					flush()
				current.append(sent)
				current_tokens += ts
			else:
				if current_tokens + para_tokens > max_tokens:
					flush()
				current.append(para)
				current_tokens += para_tokens

	flush()

	# add overlaps
	if overlap_tokens > 0 and chunks:
		overlapped: List[str] = []
		prev_tail = ""
		for ch in chunks:
			if prev_tail:
				overlapped.append((prev_tail + "\n" + ch).strip())
			else:
				overlapped.append(ch)
			# compute tail for next overlap
			if ENC is None:
				words = ch.split()
				prev_tail = " ".join(words[-overlap_tokens:]) if words else ""
			else:
				ids = ENC.encode(ch)
				tail_ids = ids[-overlap_tokens:]
				prev_tail = ENC.decode(tail_ids)
		return overlapped

	return chunks
