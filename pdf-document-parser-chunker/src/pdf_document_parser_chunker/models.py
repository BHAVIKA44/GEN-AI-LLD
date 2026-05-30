from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedDocument:
    source_path: str
    text: str


@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    text: str
