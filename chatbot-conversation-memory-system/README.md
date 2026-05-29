# Problem Statement

Implement a conversation memory system for a chatbot (sliding window, summary, buffer).

# Requirements

## Functional requirements
- Support buffer memory (full history).
- Support sliding window memory (last N turns).
- Support summary memory (running summary + recent turns).
- Expose consistent memory API.

## Non-functional requirements
- Small, interview-ready implementation.
- Clean abstraction and easy strategy swap.
- Deterministic behavior for testing.

## Assumptions
- One conversation per memory instance.
- Turn = user message + assistant message.
- Summary can be heuristic in this round.

# Design Overview

Main components:
- `ConversationMemory` interface contract.
- `BufferMemory` full history strategy.
- `SlidingWindowMemory` bounded context strategy.
- `SummaryMemory` compressed context strategy.

Data flow:
1. Chatbot writes each turn via `add_turn`.
2. Before next model call, chatbot requests `get_context`.
3. Chosen strategy controls what context is returned.

# Class / Module Design

- `models.py`: `Message`, `Turn`
- `interfaces.py`: `ConversationMemory`
- `memory.py`:
  - `BufferMemory`
  - `SlidingWindowMemory`
  - `SummaryMemory`

# Technology Selection Rationale

- LangChain: Not used.
  - Why: problem is focused on memory strategy logic; direct code is clearer for 1-hour LLD.
  - Tradeoff: fewer immediate integrations with chain abstractions.
- LangGraph: Not used.
  - Why: no complex workflow/state machine beyond local memory state.
  - Tradeoff: less orchestration scaffolding for future multi-node agents.
- RAG/Vector DB/Agents: Not used.
  - Why: out of scope for this problem statement.

# Error Handling

- Validate strategy configuration (`window_size`, `recent_turns`).
- `clear()` safely resets internal state.

# Testing Strategy

- Buffer strategy returns full conversation.
- Sliding window strategy drops old turns.
- Summary strategy returns system summary + recent turns.
- Clear behavior resets state.

# Tradeoffs

- Summary is heuristic and deterministic, not LLM-generated.
- No token-aware truncation yet.
- No persistence (in-memory only).

# How to Run

Install:
```bash
cd chatbot-conversation-memory-system
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
