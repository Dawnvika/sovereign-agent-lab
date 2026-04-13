"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                           
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                             
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                    
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                           
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                           
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                             
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                    
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                                                                           
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300."   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                           
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                             
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                              
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes                                                                                                                                                                    
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                           
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes                                                                                                                                                                    
Thank you — booking confirmed. 160 guests, 0 requiring vegan meals, £0 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
When asked about parking, CALM paused the active booking flow to handle the out-of-scope request. 
After resuming the booking, it completely skipped the question about vegan meals. 
Furthermore, it hallucinated in the final summary, incorrectly stating "0 vegan meals" and a "£0 deposit", 
despite my explicit input of £200."""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Both agents successfully refused to answer the out-of-scope question. 
However, LangGraph simply stopped and dropped the conversation entirely. 
Rasa CALM handled it much more gracefully as a manageable "interruption": 
it paused the current flow, delivered the refusal, and then prompted to resume the booking. 
Interestingly, CALM struggled to extract the remaining slots accurately after the interruption (recording 0 vegan and £0 deposit),
showing that LLM state recovery isn't perfect yet.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
The uncommented code is an environment-dependent guard checking if the system time is past 16:45. 
Since I tested it outside this time window, it didn't trigger naturally. 
To force the test, I changed the condition to `if True:` (or a guaranteed time), restarted the action server, 
and verified that the agent escalated a perfectly valid booking request due to "insufficient time".
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
This change makes the bot speak more naturally, but it becomes less predictable.
What we gain: The LLM easily understands the user. 
It can find information in normal sentences (for example, turning "about 50 need vegan" into the number 50) 
without needing complex code or hundreds of training examples. 
It can also change topics easily, like when it paused the booking to answer my question about "parking".
What we lose and why we still need Python: We lose 100% control. 
As we saw in the "parking" test, the LLM forgot our conversation after the interruption. 
It made up wrong numbers (recording 0 vegan meals and a £0 deposit instead of £200). 
Because LLMs can forget things and make mistakes, we still must use Python (actions.py) for strict business rules, 
like the £300 limit or the 16:45 time limit. 
The old system never made up facts, so now CALM needs Python as a safety net."""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
LangGraph is a free thinker that can choose tools and make up answers. 
Rasa CALM is different. It is a strict worker that only follows the rules in `flows.yml` and cannot invent new actions.

We saw this difference in our tests. 
In Exercise 2, LangGraph hallucinated bad text like "160 girts" on the flyer and chose a pub randomly. 
But in Exercise 3, Rasa CALM was safe. When I asked about "parking", it didn't invent a story. 
It simply said it couldn't help and went back to the booking. Also, our Python rules strictly stopped the bad £500 deposit.

For a business, this strictness is exactly what we need. 
Setting up Rasa takes a lot of time and files, but this hard work gives us safety. 
The bot strictly follows company rules and never goes off-topic.
"""
