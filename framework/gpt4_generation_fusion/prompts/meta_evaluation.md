# 任务

你是一个针对指导和教导标注人员的一个专家。标注人员的职责是对对话模型生成的内容的质量进行分析标注，而你的职责是生成领域更多样，质量更丰富的测试数据用于建议标注人员的能力。

现在，标注人员已经依据你给出的测试数据撰写了他们针对用户输入（query）的待评估回复（response）的质量分析（predictio-critique）。现在你的目的是依据你在测试样例中给出的query, response和标注分析参考答案（critique），对这些标注人员生成的质量分析prediction-critique 的质量进行判断。
query， response，你的标准 critique 和标注人员生成的 prediction-critique 如下所示

## 数据

### 1. Query
{query}
### 2. Response
{response}
### 3. Critique (你的参考答案分析内容)
{critique}
### 4. Prediction-Critique (标注人员生成的分析内容，需要依据参考答案 critique 对其质量进行判断)
{predictioncritique}

## 需求和输出格式
1. 请你根据 critique 的质量对 prediction-critique 的质量进行判断，仔细判断 prediction-critique 中的文本表述是否和参考答案一致，以及最终得到的 1-10 的打分分数是否和参考答案中的打分分数是相对来说比较吻合的（追求完全吻合的打分分数是不现实的，因此这个分数的差异如果不大可以认为是吻合的）
2. 根据上面的判断需求，将 prediction-critique 的质量分为两个等级：（1）存在错误 - 0：prediction-critique 错误的分析了 responose 质量，其分析和参考分析完全不匹配且打分差异过大；或者prediction-critique 和 critique 在文本表述上部分匹配，但是包含一些错误分析内容；（1）吻合 - 1：prediction-critique和 critique 的分析完全一致，打分分数差异较小；或者prediction-critique和 critique 分析近似，存在的部分差异可以认为影响不大；亦或者如果 prediction-critique 和参考 critique 不一致，但是 prediction-critique 质量更好，分析更合理。
3. 请首先生成你关于 prediction-critique 质量的文本判断描述(用中文)，然后在最后按照如下格式附上你选择的打分（0/1）```Quality：x```；其中 x 是 0/1 分别标上上面提到的 2 个 prediciton-critique 的质量等级。
