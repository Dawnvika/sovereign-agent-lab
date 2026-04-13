"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
I observed that the Llama-3.3-70B model answered correctly across all three formatting conditions because of its high baseline capability on short, clean datasets. 
However, I also noticed a difference in token usage: PLAIN used 180 tokens, while XML used 251 and SANDWICH used 289. 
This is a crucial trade-off: while advanced formatting provides a safety net for accuracy, it increases the token count, which will lead to higher operational API costs in production.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms is the most dangerous distractor because it satisfies two out of three constraints 
(capacity is 160 and vegan=yes). It only fails on status (full). A model skimming for keywords 
might stop reading too early and pick it.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C was run to test the smaller 8B model because the 70B model was perfect. 
I noticed that the results changed: now all three answers are identical, 
returning 'The Haymarket Vaults' every time. This shows that the small model 
is very consistent and can find the correct answer despite the distractors 
and different formatting.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when you are dealing with very long texts, highly complex instructions, 
or models that struggle with attention. However, this experiment also showed that modern small models (like 8B) 
have become incredibly good at information extraction on short contexts. Even so, using structures like XML 
or the Sandwich method is a crucial safety net to guarantee accuracy when building reliable agents.
Ultimately, engineers must balance this need for structural safety against the increased API costs caused by higher token consumption.
"""
