from .template_markdown import *


multi_turn_prompts = {
    'task': '''You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous conversation history. Firstly, please analyze the purpose of the user in previous conversation history.''',
    'criteria': '''Now, we have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

Please generaet the two-tier detailed criteria list (of our provided criteria list is not empty, please expand ours).
    ''',
    'reference': '''Please generate the high-quality reference answer for the last user's query in previous conversation history, which perfectly satisify all the provided and generated criteria.''',
    'feedback':  '''Generate your detailed feedbacks consisting of multiple entries that analyze the errors in evaluated response, with the help of previous important information:
(1) task description (purpose of user in the conversation);
(2) two-tier criteria;
(3) high-quality reference (maybe empty)

Note that each sentence in evaluated response is marked with a citation symbol, like [S1] and [S2]. You could use this citation symbol to detect the position of errors in the evaluated response.''', 
    'summarization': '''Based on generated feedbacks, generate a summarization, which consists of overall description of evaluated response quality, and the final judgemen score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)'''
}


overall_prompts = [
    # dv4, dv5
    '''# Goal
You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous conversation history.

We have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

# Task

To generate the valuable feedback, you should follow these 4 steps to generate valuable and accurate critiques:
**Step 1:** analyze the purpose of the user role in the previous conversation history
**Step 2:** generate the two-tier detailed criteria list (if our provided criteria list is not empty, please expand ours)
**Step 3:** generate your high-quality reference answer for better critiques
**Step 4:** generate your detailed feedbacks, followed by a summarizaing containing the final judgemen score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)

# NOTICE
1. the last response in the conversation history contains the citation symbols for better critiques, like [S1] and [S2]. Do NOT critique on these citation symbols

# Output
Generate the your content in the clear markdown template format.
''',
    # d4v5 - 没有reference
    '''# Goal
You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous conversation history.

We have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

# Task

To generate the valuable feedback, you should follow these 3 steps to generate valuable and accurate critiques:
**Step 1:** analyze the purpose of the user role in the previous conversation history
**Step 2:** generate the two-tier detailed criteria list (if our provided criteria list is not empty, please expand ours)
**Step 3:** generate your detailed feedbacks, followed by a summarizaing containing the final judgemen score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)

# NOTICE
1. the last response in the conversation history contains the citation symbols for better critiques, like [S1] and [S2]. Do NOT critique on these citation symbols

# Output
Generate the your content in the clear markdown template format.
''',
    # d4v6 - 没有task description
    '''# Goal
You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous conversation history.

We have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

# Task

To generate the valuable feedback, you should follow these 3 steps to generate valuable and accurate critiques:
**Step 1:** generate the two-tier detailed criteria list (if our provided criteria list is not empty, please expand ours)
**Step 2:** generate your high-quality reference answer for better critiques
**Step 3:** generate your detailed feedbacks, followed by a summarizaing containing the final judgemen score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)

# NOTICE
1. the last response in the conversation history contains the citation symbols for better critiques, like [S1] and [S2]. Do NOT critique on these citation symbols

# Output
Generate the your content in the clear markdown template format.
''',
    # d4v12 - 没有criteria generation
    '''# Goal
You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous conversation history.

We have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

# Task

To generate the valuable feedback, you should follow these 3 steps to generate valuable and accurate critiques:
**Step 1:** analyze the purpose of the user role in the previous conversation history
**Step 2:** generate your high-quality reference answer for better critiques
**Step 3:** generate your detailed feedbacks, followed by a summarizaing containing the final judgemen score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)

# NOTICE
1. the last response in the conversation history contains the citation symbols for better critiques, like [S1] and [S2]. Do NOT critique on these citation symbols

# Output
Generate the your content in the clear markdown template format.
''',
    # dv5
    '''# Goal
Please analyze the quality feedback lists generated by multiple models.

# Multiple Feedback Lists
{multiple_feedback_list}

# Output
Generate the your content in the clear markdown template format.
'''
]
