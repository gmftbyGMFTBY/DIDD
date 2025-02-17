from .template_markdown import *

task_criteria_prompts = [
    """# Your Task Input
Now, you are a helpful assistant aiming to provide valuable critiques and analysis for the previous conversation history, thereby assisting in the analysis of the quality of subsequent responses in relation to this conversation history history.

Now, we have provided our criteria list (maybe empty) for you from different evaluation perspectives as below.
---
# Our Provided Criteria List
{my_criteria}
---

# Your Tasks
## 1. Analyze Task
Analyze and describe the primary purpose of user's query in conversation history. Do NOT generate very lengthy description, keep it concise and precise.
**If the conversation history contains multiple turns between assistant and human, MUST analyze the main purpose of the user's last query by considering the previous conversation history.**

## 2. Supplement and Decompose the Criteria
Generate the criteria list of the two-tier structure:
(1) The first-tier structure consists of primary criteria, i.e., the evaluation dimensions broadly conceptualized and distinct based on conversation history.
(2) The second-tier structure decomposes these primary evaluation dimensions into several fine-grained and precise criteria based on the information in conversation history.

**Note that our provided criteria list are only the primary criteria list (first-tier) without the fine-grained criteria definition (second-tier).**

### 2.1 If our provided criteria list is **EMPTY**

Please directly generate this two-tier criteria structure from scratch.
**Do NOT generate redundant criteria; keep the final criteria  
precise, helpful, and concise.**

### 2.2 If our provided criteria list is **NOT EMPTY**

Firstly, **you should keep all our provided criteria as the primary criteria in your final output.** 
You could expand other primary criteria not considered in our provided criteria but are essential for analyzing flaws in responses for previous conversation history.
**But NEVER expand primary criteria that conflict with our provided criteria.**
**NEVER generate criteria that are redundant with our provided criteria.**
**Do NOT miss any criteria that exists in our provided criteria list.**

Secondly, you should decompose these primary criteria into several fine-grained and precise criteria by considering the conversation history.

### 2.3 NOTICE!!!
**Keep the number of all fine-grained criteria within 15, and each primary criterion includes no more than 3 fine-grained criteria.**

# Output Template
Generate the task description and the two-tier structure criteria in following Markdown template. Do NOT add comment (//) in the template.
---
""" + task_and_criteria_markdown_template + '\n---',
    """# Your Task Input
Now, you are a helpful assistant aiming to provide valuable critiques and analysis for the previous conversation history, thereby assisting in the analysis of the quality of subsequent responses in relation to this conversation history history.

Now, we have provided our criteria list (maybe empty).
---
# Our Provided Criteria List
{my_criteria}
---

# Your Tasks
## 1. Analyze Task
Analyze and describe the primary purpose of user's query in conversation history. Do NOT generate very lengthy description, keep it concise and precise.
**If the conversation history contains multiple turns between assistant and human, MUST analyze the main purpose of the user's last query by considering the previous conversation history.**

## 2. Supplement and Decompose the Criteria
Generate the criteria list of the two-tier structure:
(1) The first-tier structure consists of primary criteria, i.e., the evaluation dimensions broadly conceptualized and distinct based on conversation history.
(2) The second-tier structure decomposes these primary evaluation dimensions into several fine-grained and precise criteria based on the information in conversation history.

**Note that our provided criteria list are only the primary criteria list (first-tier) without the fine-grained criteria definition (second-tier).**

# Output Template
Generate the task description and the two-tier structure criteria in following Markdown template. Do NOT add comment (//) in the template.
---
""" + task_and_criteria_markdown_template + '\n---',
    """# Your Task Input
Now, you are a helpful assistant aiming to provide valuable critiques and analysis for the previous conversation history, thereby assisting in the analysis of the quality of subsequent responses in relation to this conversation history history.

Now, we have provided our criteria list (maybe empty) for you from different evaluation perspectives as below.
---
# Our Provided Criteria List
{my_criteria}
---

# Your Tasks
## 1. Analyze Task
Analyze and describe the primary purpose of user's query in conversation history. Do NOT generate very lengthy description, keep it concise and precise.
**If the conversation history contains multiple turns between assistant and human, MUST analyze the main purpose of the user's last query by considering the previous conversation history.**

## 2. Supplement and Decompose the Criteria
Generate the criteria list of the two-tier structure:
(1) The first-tier structure consists of primary criteria, i.e., the evaluation dimensions broadly conceptualized and distinct based on conversation history.
(2) The second-tier structure decomposes these primary evaluation dimensions into several fine-grained and precise criteria based on the information in conversation history.

**Note that our provided criteria list are only the primary criteria list (first-tier) without the fine-grained criteria definition (second-tier).**

### 2.1 If our provided criteria list is **EMPTY**
Please directly generate this two-tier criteria structure from scratch.

### 2.2 If our provided criteria list is **NOT EMPTY**
Firstly, **you should keep all our provided criteria as the primary criteria in your final output.** , and generate primary criteria not considered in our provided criteria but are essential for analyzing flaws in responses for previous conversation history.
Secondly, you should decompose these primary criteria into several fine-grained and precise criteria by considering the conversation history.

### 2.3 NOTICE!!!
**Keep the number of all fine-grained criteria within 15, and each primary criterion includes no more than 3 fine-grained criteria.**

# Output Template
Generate the task description and the two-tier structure criteria in following Markdown template. Do NOT add comment (//) in the template.
---
""" + task_and_criteria_markdown_template + '\n---',
    """# Your Task Input
We have provided our criteria list for you from different evaluation perspectives as below.
---
# Our Provided Criteria List
{my_criteria}
---

# Your Tasks
## 1. Analyze Task
Analyze and describe the primary purpose of user's query in conversation history. Do NOT generate very lengthy description, keep it concise and precise.
**If the conversation history contains multiple turns between assistant and human, MUST analyze the main purpose of the user's last query by considering the previous conversation history.**

## 2. Supplement and Decompose the Criteria
Generate the criteria list of the two-tier structure:
(1) The first-tier structure consists of primary criteria, i.e., the evaluation dimensions broadly conceptualized and distinct based on conversation history.
(2) The second-tier structure decomposes these primary evaluation dimensions into several fine-grained and precise criteria based on the information in conversation history.

If our provided criteria list is **EMPTY**, please directly generate this two-tier criteria structure from scratch.
If our provided criteria list is **NOT EMPTY**, you should follow these two instrutions: 
(1) Firstly, **you should keep all our provided criteria as the primary criteria in your final output.** , and generate primary criteria not considered in our provided criteria but are essential for analyzing flaws in responses for previous conversation history.
(2) Secondly, you should decompose these primary criteria into several fine-grained and precise criteria by considering the conversation history.

# Output Template
Generate the task description and the two-tier structure criteria in following Markdown template.
---
""" + task_and_criteria_markdown_template + '\n---',
    '''# Task Input Provided
We have furnished you with a list of criteria from various evaluative standpoints, as outlined below.
---
# Criteria List Supplied by Us
{my_criteria}
---
# Your Assignments
## 1. Analyze the Task
Examine and succinctly detail the main objective of the user's inquiry within the dialogue history. Your description should be concise and to the point.
**In instances where the dialogue history encompasses multiple exchanges between the assistant and the user, it is imperative to consider the full context of the previous conversation when determining the primary purpose of the user's most recent query.**
## 2. Supplement and Break Down the Criteria
Produce a criteria list organized in a two-tier hierarchy:
(1) The first tier should comprise the principal criteria, which are the overarching evaluation dimensions identified from the dialogue history and should be distinct from one another.
(2) The second tier should further divide these principal evaluation dimensions into more detailed and specific criteria, based on the content of the dialogue history.
If the criteria list we have provided is **EMPTY**, you need to create the two-tier criteria structure from the ground up.
If the criteria list we have provided is **NOT EMPTY**, you must adhere to these two guidelines:
(1) Firstly, **all the criteria we have provided should be maintained as the primary criteria in your final submission**, and you should also identify and include any primary criteria that were not addressed in our list but are crucial for assessing the inadequacies in the responses from the previous conversation history.
(2) Secondly, you should elaborate on these primary criteria by breaking them down into more nuanced and precise sub-criteria, taking into account the dialogue history.
# Output Format
Compose the task description and the two-tiered criteria structure using the following Markdown template.
''' + task_and_criteria_markdown_template + '\n---',
    '''# Your Task Input
Currently, you are an assistant tasked with providing insightful critiques and analyses of the preceding conversation history, which will aid in assessing the quality of future responses in relation to this history.
We have furnished you with a list of criteria (which may be empty) from various evaluative standpoints, as outlined below.
---
# Our Provided Criteria List
{my_criteria}
---
# Your Tasks
## 1. Analyze Task
Evaluate and succinctly describe the main objective of the user's query within the conversation history. Your description should be concise and precise.
**If the conversation history includes multiple exchanges between the assistant and the user, it is essential to analyze the primary purpose of the user's most recent query in the context of the previous conversation history.**
## 2. Supplement and Decompose the Criteria
Develop a criteria list organized in a two-tier hierarchy:
(1) The first tier comprises the primary criteria, which are the broad evaluation dimensions identified from the conversation history and should be distinct from one another.
(2) The second tier breaks down these primary evaluation dimensions into several detailed and precise sub-criteria based on the information in the conversation history.
**Please note that the criteria list we have provided only includes the primary criteria (first tier) without the detailed sub-criteria definitions (second tier).**
### 2.1 If our provided criteria list is **EMPTY**
You should create the two-tier criteria structure from scratch.
**Avoid generating redundant criteria; ensure the final criteria are precise, helpful, and concise.**
### 2.2 If our provided criteria list is **NOT EMPTY**
Firstly, **you must retain all the criteria we have provided as the primary criteria in your final submission.**
You may introduce additional primary criteria not included in our provided list if they are crucial for analyzing flaws in responses from the previous conversation history.
**However, do not introduce primary criteria that conflict with those we have provided.**
**Do not generate criteria that duplicate our provided criteria.**
**Ensure you do not omit any criteria that are present in our provided criteria list.**
Secondly, decompose these primary criteria into several detailed and precise sub-criteria, taking into account the conversation history.
### 2.3 NOTICE!!!
**Limit the total number of sub-criteria to 15, and ensure that each primary criterion includes no more than 3 sub-criteria.**
# Output Template
Compose the task description and the two-tiered criteria structure using the following Markdown template. Do not include comments (//) in the template.
---
''' + task_and_criteria_markdown_template + '\n---',
    '''# Your Task Input
Currently, you are an assistant whose role is to offer valuable critiques and analysis of the earlier conversation history, which will aid in evaluating the quality of future responses in light of this conversation history.
We have provided you with a list of criteria (which might be empty) from various evaluation perspectives, as detailed below.
---
# Our Provided Criteria List
{my_criteria}
---
# Your Tasks
## 1. Analyze Task
Examine and concisely describe the main objective of the user's query within the conversation history. Your description should be succinct and precise.
**If the conversation history includes multiple exchanges between the assistant and the user, it is essential to analyze the primary purpose of the user's most recent query in the context of the previous conversation history.**
## 2. Supplement and Decompose the Criteria
Develop a criteria list organized in a two-tier hierarchy:
(1) The first tier comprises the primary criteria, which are the broad evaluation dimensions identified from the conversation history and should be distinct from one another.
(2) The second tier breaks down these primary evaluation dimensions into several detailed and precise sub-criteria based on the information in the conversation history.
**Note that the criteria list we have provided only includes the primary criteria (first tier) without the detailed sub-criteria definitions (second tier).**
### 2.1 If our provided criteria list is **EMPTY**
Please create this two-tier criteria structure from the beginning.
### 2.2 If our provided criteria list is **NOT EMPTY**
Firstly, **you must retain all the criteria we have provided as the primary criteria in your final submission.** Additionally, generate primary criteria not included in our provided criteria but are essential for analyzing flaws in responses from the previous conversation history.
Secondly, decompose these primary criteria into several detailed and precise sub-criteria by considering the conversation history.
### 2.3 NOTICE!!!
**Limit the total number of sub-criteria to 15, and ensure that each primary criterion includes no more than 3 sub-criteria.**
# Output Template
Create the task description and the two-tiered criteria structure using the following Markdown template. Do not include comments (//) in the template.
---
''' + task_and_criteria_markdown_template + '\n---',
    '''# Task Input Provided
We have provided you with a list of criteria from various evaluative standpoints, as outlined below.
---
# Criteria List Supplied by Us
{my_criteria}
---
# Your Assignments
## 1. Analyze the Converation history
Examine and succinctly detail the main objective of the user's inquiry within the dialogue history. Your description should be concise and to the point.
**In instances where the dialogue history encompasses multiple exchanges between the assistant and the user, it is imperative to consider the full context of the previous conversation when determining the primary purpose of the user's most recent query.**
## 2. Supplement and Break Down the Criteria
Produce a criteria list organized in a two-tier hierarchy:
(1) The first tier should comprise the principal criteria, which are the overarching evaluation dimensions identified from the dialogue history and should be distinct from one another.
(2) The second tier should further divide these principal evaluation dimensions into more detailed and specific criteria, based on the content of the dialogue history.
If the criteria list we have provided is **EMPTY**, you need to create the two-tier criteria structure from the ground up.
If the criteria list we have provided is **NOT EMPTY**, you must adhere to these two guidelines:
(1) Firstly, **all the criteria we have provided should be maintained as the primary criteria in your final submission**, and you should also identify and include any primary criteria that were not addressed in our list but are crucial for assessing the inadequacies in the responses from the previous conversation history.
(2) Secondly, you should elaborate on these primary criteria by breaking them down into more nuanced and precise sub-criteria, taking into account the dialogue history.
# Output Format
Compose the task description and the two-tiered criteria structure using the following Markdown template.
''' + task_and_criteria_markdown_template + '\n---',
    '''# Input
We have provided you with a list of criteria from various evaluative standpoints, as outlined below.
---
# Provided Criteria List
{my_criteria}
---

# Your Assignments

Produce a criteria list organized in a two-tier hierarchy:
(1) The first tier should comprise the principal criteria, which are the overarching evaluation dimensions identified from the dialogue history and should be distinct from one another.
(2) The second tier should further divide these principal evaluation dimensions into more detailed and specific criteria, based on the content of the dialogue history.
If the criteria list we have provided is **EMPTY**, you need to create the two-tier criteria structure from the ground up.

# Output Format
Compose the task description and the two-tiered criteria structure in a Markdown format.
'''
]

