#from .template_markdown import *


### 现在的multi-turn prompts并不能直接用于做对guidelines的消融实验
multi_turn_prompts_ = {
    'initial_input': [
        '''You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous **conversation history**.

The response is here:
---
{response}
---

The conversation history is here:
---
{conversation_history}
---
''',
    ],
    'task': [
        'What is the purpose of the user in the conversation history',
        'Please analyze the purpose of the user in previous conversation history, which is benefical for us to respond.',
        'Plesae summarize the purpose of user.'
    ],
    'criteria': [
        '''Now, we have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

Please generate the two-tier detailed criteria list (of our provided criteria list is not empty, please expand ours).
    ''',
        'Please generate the detailed criteria for this task (conversation history)',
    ],
    'reference': [
        "Please generate the high-quality reference answer for the last user's query in previous conversation history, which perfectly satisify all the provided criteria.",
        'Please generate your answer for the conversation history that fulfill user query',
        'Respond to the given conversation history',
    ], 
    'feedback':  [
        '''Generate your detailed feedbacks consisting of multiple entries that analyze the errors in evaluated response, with the help of previous important information:
(1) task description (purpose of user in the conversation);
(2) two-tier criteria;
(3) high-quality reference (maybe empty)

Note that each sentence in evaluated response is marked with a citation symbol, like [S1] and [S2]. You could use this citation symbol to detect the position of errors in the evaluated response.

Each entry in the feedback should consists of:
(1) the location of the error (citation symol)
(2) the description of the error
(3) the severity of this error
(4) the suggestion for revising it
''',
        'Please generate the detailed feedback that analyze flaws in the evaluated responses. Note that feedback should contains the detailed information, like the location, description, severity and the suggestion for each error/flaw.',
        'Please generate the detailed feedback',
    ],
    'summarization': [
        '''Based on generated feedbacks, generate a summarization, which consists of overall description of evaluated response quality over the criteria, and the final judgement score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)''',
        'Please summarize your feedback and give a judgment score ranging from 1 to 10.'
    ]
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

### 现在的multi-turn prompts并不能直接用于做对guidelines的消融实验
multi_turn_prompts_v3 = {
    'initial_input': [
        '''You are a helpful assistant aiming to provide valuable critiques and analysis for the **last response** in the previous **conversation history**.
The conversation history is here:
---
{conversation_history}
---
''',
    ],
    'task': [
        'What is the purpose of the user in the conversation history',
        'Please analyze the purpose of the user in previous conversation history, which is benefical for us to respond.',
        'Plesae summarize the purpose of user.'
    ],
    'criteria': [
        '''Now, we have provided our criteria list for you from different evaluation perspective as below
---
# Our Provided Criteria List
{my_criteria}
---

Please generate the two-tier detailed criteria list (of our provided criteria list is not empty, please expand ours).
    ''',
        'Please generate the detailed criteria for this task (conversation history)',
    ],
    'reference': [
        "Please generate the high-quality reference answer for the last user's query in previous conversation history, which perfectly satisify all the provided criteria.",
        'Please generate your answer for the conversation history that fulfill user query',
        'Respond to the given conversation history',
    ], 
    'feedback':  [
        '''Generate your detailed feedbacks consisting of multiple entries that analyze the errors in evaluated response, with the help of previous important information:
(1) task description (purpose of user in the conversation);
(2) two-tier criteria;
(3) high-quality reference (maybe empty)

The evaluated response is here:
---
{response}
---

Note that each sentence in evaluated response is marked with a citation symbol, like [S1] and [S2]. You could use this citation symbol to detect the position of errors in the evaluated response.

Each entry in the feedback should consists of:
(1) the location of the error (citation symol)
(2) the description of the error
(3) the severity of this error
(4) the suggestion for revising it
''',
        'Please generate the detailed feedback that analyze flaws in the evaluated responses. Note that feedback should contains the detailed information, like the location, description, severity and the suggestion for each error/flaw.\nThe evaluated response is here:\n---\n{response}\n---\n',
        'Please generate the detailed feedback. The evaluated response is here:\n---\n{response}\n---\n',
    ],
    'summarization': [
        '''Based on generated feedbacks, generate a summarization, which consists of overall description of evaluated response quality over the criteria, and the final judgement score (ranging from 1 to 10, where higher score denotes better quaulity of evaluated response.)''',
        'Please summarize your feedback and give a judgment score ranging from 1 to 10.'
    ]
}



