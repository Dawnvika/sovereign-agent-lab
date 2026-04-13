"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", 
    "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "It seems there are no currently available Edinburgh venues that can accommodate 300 people with vegan options. Would you like me to:\n1. Search for venues with a lower minimum capacity?\n2. Look for venues without vegan requirements?\n3. Check for availability at a specific date/time?\n\nLet me know how you'd like to proceed."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
# What changed in the output? What didn't?
# Min 30 words.
EX4_EXPERIMENT_RESULT = """
When I updated the venue status in `mcp_venue_server.py`, the agent's output changed to recommend the only remaining available venue. 
Because there was only one match left, the agent's internal reasoning also changed: 
it no longer had to compare options to decide which was the 'best' fit.
However, I did not need to update the agent's actual code file (`exercise4_mcp_client.py`) at all. 
The agent dynamically read the new live data from the shared MCP server, 
proving that we can manage data independently from the agent's logic.
For Query 2 the agent correctly identified that there are 0 matching venues, informed the user, 
and gracefully offered 3 alternatives to adjust the search (like reducing capacity or changing dietary needs).
"""
# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 4   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides a universal, standardized bridge between agents and tools. 
It allows entirely different agent frameworks (like LangGraph and Rasa) to connect 
to the exact same live server and dynamically discover its capabilities. 
If we add a new tool or fix a bug on the server, 
all connected agents instantly inherit the new logic without requiring any code changes or redeployments on the agent side.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner: A thinking model that sits upstream of the ReAct loop to break down ambiguous tasks into subgoals. It lives in the autonomous-loop half.
- The Executor: Evolved from our Week 1 LangGraph agent, it dynamically acts on the subgoals using tools like web search. It lives inside the autonomous-loop half.
- The Shared MCP Tool Server: A centralized server providing all capabilities (venue lookups, calendar, etc.) to any connected agent. It lives in the shared layer between both halves.
- The Handoff Bridge: A protocol that delegates tasks back and forth, transferring control when the autonomous loop needs a human conversation. It lives in the shared layer connecting the two halves.
- The Structured Confirmation Agent: Evolved from our Week 1 Rasa CALM agent, it runs strict, auditable business rules (and a RAG knowledge base) for high-stakes tasks like calling the pub manager. It lives in the structured-agent half.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
For the research phase, we can use the LangGraph agent. 
It is a creative problem-solver that can dynamically recover from errors (like the Pydantic schema validation we saw) 
and suggest alternatives when a venue is full. 

For the confirmation call, we must use the Rasa CALM agent because it strictly follows rules. 
Swapping them would be a disaster. 
If LangGraph handled the call, it might hallucinate details 
(like when it invented "160 girts" on the flyer or lost the conversation context after I asked about parking). 
If Rasa handled the research, its rigid tracks would crash as soon as a search returned 0 matches, 
because it lacks the free-thinking ability to suggest alternatives.
"""