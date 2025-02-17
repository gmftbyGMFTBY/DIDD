from .template_markdown import *

reference_prompts = [
    '''# Task Goal
Good! Your task is to generate a high-quality response for the **conversation history (before we provided the criteria list)**, which perfectly satisfies all the generated **first-tier and second-tier** criteria in last turn. 
    
# NOTICE!!!
1. **The conversation history here represents the conversations before we provided the criteria list. Do NOT respond to the last utterance.**
2. **Do NOT generate any explanation or analysis about your generated response.**''',
    '''Your goal is to craft a high-quality reply for the **dialogue history (occurring prior to our issuance of the criteria catalog)**, one that flawlessly aligns with all the established criteria from the previous interaction.''',
    '''Great job! Your objective is to craft a good response for the dialogue history, guaranteeing that it fulfills all the requirements of both Tier 1 and Tier 2 criteria mentioned in the preceding turn.''',
    '''Your task is to generate a high-quality response for the **conversation history (before we provided the criteria list)**, which perfectly satisfies all the generated **first-tier and second-tier** criteria in last turn. **The conversation history here represents the conversations before we provided the criteria list. Do NOT respond to the last utterance.**''',
    '''Your task is to generate a high-quality response for the **conversation history (before we provided the criteria list)**, which perfectly satisfies all the generated **first-tier and second-tier** criteria in last turn. Do NOT generaet any explanation.''',
    '''# Objective
Well done! Your goal is to craft an exceptional reply for the **dialogue history (occurring prior to our issuance of the criteria list)**, one that flawlessly aligns with all the established **primary and secondary** criteria from the previous interaction.
# ATTENTION!!!
1. **The dialogue history in this context refers to the exchanges that took place before we furnished the criteria list. Do NOT address the most recent comment.**
2. **Do NOT provide any commentary or rationale regarding your composed response.*
''',
    '''# Task Objective
Excellent! Your mission is to produce a top-tier response for the **dialogue transcript (up until the point where we supplied the criteria list)**, ensuring it meets all the **Tier 1 and Tier 2** criteria outlined in the previous round.
# IMPORTANT!!!
1. **The dialogue transcript refers to the exchanges that occurred prior to our provision of the criteria list. Do NOT address the most recent statement.**
2. **Do NOT offer any justification or critique of your crafted response.**
''',
    '''# Your Task
Great! Your objective is to create a high-quality response for the **dialogue history (up until we presented the criteria list)** that flawlessly meets all the **Tier 1 and Tier 2** criteria established in the previous round.
# CAUTION!!!
1. **The conversation history in this context refers to the dialogues that took place before we provided the criteria list. Do NOT reply to the latest statement.**
2. **Do NOT provide any commentary or analysis for the response you generate.**
''',
    '''Your task is to create a high-quality response for the **dialogue history** that fullfil all the criteria.
'''
]
