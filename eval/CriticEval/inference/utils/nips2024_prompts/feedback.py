from .template_markdown import *

feedback_prompts = [
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---
## NOTICE!!!
1. **The conversation history here represents the conversations before we provided the criteria list.**
2. **The evaluated response contains citation symbols, like [S1] and [S2] ([S1] means sentence 1), which represent the ID of their preceding sentences and are helpful for our following analysis.**

# Task Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria, and high-quality reference response**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw. 

## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) **Do NOT critique and analyze the sentences that are free from any flaws**;
(3) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(4) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.

Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---

# Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria, and high-quality reference response**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw.

## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(3) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.

# Output Format
Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the response to be evaluated that responds to the conversation history as below.
---
{evaluated_response}
---
# Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria, and high-quality reference response**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw.
## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(3) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.
# Output Format
Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---
# Goal
Your current task involves creating several feedback items for **the evaluated response, taking into account the conversation history, the two-tiered criteria structure, and the high-quality reference response**. 
The feedback should identify and examine each flaw within the response.
Each flaw entry should include: (1) the citation marker for the sentence; (2) a description of the flaw; (3) the type of criteria the flaw relates to; (4) the level of severity of the flaw; (5) a suggestion for how to revise the flaw.
## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only serve to highlight the preceding sentence in the response**;
(2) Each feedback entry should address only one criterion. **Do NOT include multiple criteria in a single feedback entry. If a sentence has multiple flaws, please create separate feedback entries for each**.
(3) Each flaw in the feedback entry should correspond to a specific **detailed second-tier criterion. Only use the primary first-tier criterion if none of its associated second-tier criteria are applicable.**.
# Output Format
Please provide your answers using the following Markdown template. Do NOT add any comments (//) to the template.
---
''' + feedback_markdown_template + '\n---',
    '''Your task is to generate multiple feedback entries for **following evaluated response based on the previous conversation history, two-tier structure criteria, and high-quality reference response**. 

---
{evaluated_response}
---

Please answer in following Markdown format template.
'''
]

feedback_no_ref_prompts = [
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---
## NOTICE!!!
1. **The conversation history here represents the conversations before we provided the criteria list.**
2. **The evaluated response contains citation symbols, like [S1] and [S2] ([S1] means sentence 1), which represent the ID of their preceding sentences and are helpful for our following analysis.**

# Task Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw. 

## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) **Do NOT critique and analyze the sentences that are free from any flaws**;
(3) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(4) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.

Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---

# Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw.

## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(3) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.

# Output Format
Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the response to be evaluated that responds to the conversation history as below.
---
{evaluated_response}
---
# Goal
Now, your task is to generate multiple feedback entries for **this evaluated response based on the conversation history, two-tier structure criteria**. 
Precisely, the feedback should locate and analyze all the flaw units in the response.
Each flaw unit consists of: (1) the citation symbol of the sentence; (2) the flaw's description; (3) the flaw's criteria type; (4) the severity of the flaw; (5) and the revision suggestion for the flaw.
## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only highlight its preceding sentence in the response**;
(2) Each feedback entry contains only one criteria. **Do NOT add multiple criteria in one feedback entry. If you think the sentence have multiple flaws, please list them into multiple feedback entries**.
(3) Each flaw in the feedback entry should follow one **fine-grained second-tier criterion. Only select the primary first-tier criteria when all its second-tier fine-grained criteria are inappropriate.**.
# Output Format
Please answer in following Markdown format template. Do NOT add comment (//) in the template.
---
''' + feedback_markdown_template + '\n---',
    '''# Task Input
We provide the evaluated response that responds to the conversation history as below.
---
{evaluated_response}
---
# Goal
Your current task involves creating several feedback items for **the evaluated response, taking into account the conversation history, the two-tiered criteria structure.
The feedback should identify and examine each flaw within the response.
Each flaw entry should include: (1) the citation marker for the sentence; (2) a description of the flaw; (3) the type of criteria the flaw relates to; (4) the level of severity of the flaw; (5) a suggestion for how to revise the flaw.
## Please Strictly Abide by Following Rules:
(1) **Please Do NOT critique and analyze these citation symbols, like [S1] and [S2], since they only serve to highlight the preceding sentence in the response**;
(2) Each feedback entry should address only one criterion. **Do NOT include multiple criteria in a single feedback entry. If a sentence has multiple flaws, please create separate feedback entries for each**.
(3) Each flaw in the feedback entry should correspond to a specific **detailed second-tier criterion. Only use the primary first-tier criterion if none of its associated second-tier criteria are applicable.**.
# Output Format
Please provide your answers using the following Markdown template. Do NOT add any comments (//) to the template.
---
''' + feedback_markdown_template + '\n---',
    '''Your task is to generate multiple feedback entries for **following evaluated response based on the previous conversation history, two-tier structure criteria**. 

---
{evaluated_response}
---

Please answer in following Markdown format template.
'''
]
