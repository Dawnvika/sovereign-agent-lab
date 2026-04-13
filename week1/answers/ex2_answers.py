"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [ 'check_pub_availability',
                       'calculate_catering_cost',
                       'get_edinburgh_weather',
                       'generate_event_flyer']

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = ""

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "FILL_ME_IN"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-74eb013d-f911-439c-a422-0fa44696493b_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for a tech event. Warm lighting, Scottish architecture background. Feature prominent, perfectly spelled text reading exactly: {event_theme}. Below it, add smaller clear text reading: {venue_name} - {guest_count} guests. Use clean modern typography. Do not add random unreadable letters."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The agent survived because the tool catches the API error and still returns a "success" message with a placeholder image, allowing the agent's main loop to continue working without crashing.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
{"success": true, "pub_name": "The Bow Bar", "address": "80 West Bow, Edinburgh", "capacity": 80, "vegan": true, "status": "full", "meets_all_constraints": false}
{"success": true, "pub_name": "The Haymarket Vaults", "address": "1 Dalry Road, Edinburgh", "capacity": 160, "vegan": true, "status": "available", "meets_all_constraints": true}
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = "I am not able to execute this task as it exceeds the limitations of the functions I have been given."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
While the agent safely passed the tests by not hallucinating and politely declining tasks outside its scope, there are still flaws. 
For example, in Scenario 1, it checked both The Haymarket Vaults and The Albanach, but there is no clear logic why it finally booked The Albanach. 
A real booking assistant needs stricter rules and better reasoning to avoid unpredictable choices when multiple venues match the requirements.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
Comparing the two approaches highlights the trade-off between flexibility and predictability. 
The LangGraph Mermaid diagram shows a single implicit loop: the LLM dynamically decides which tools to call and what path to take at runtime. It is highly flexible but acts as a "black box". 
Conversely, the Rasa CALM `flows.yml` file uses explicit, deterministic routing. Every step is hardcoded (e.g., collect guests, collect vegan count). The LLM simply extracts data to fill the slots, ensuring the agent's behavior is 100% predictable and auditable.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most unexpected thing was the severe visual hallucination on the generated flyer. 
Even though the agent correctly passed the exact prompt, the image model completely mangled the text out of the box, 
producing bizarre words like "meettup" and "160 girts guests". 
Additionally, it was surprising that when the agent checked multiple valid pubs (like The Albanach and The Haymarket Vaults), 
it picked one seemingly at random without explaining the logic behind its final choice.

"""
