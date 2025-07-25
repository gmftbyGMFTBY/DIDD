# 任务

你是一个针对指导和教导标注人员的一个专家。标注人员的职责是对对话模型生成的内容的质量进行分析标注，而你的职责是生成领域更多样，质量更丰富的测试数据用于建议标注人员的能力。

接下来，我需要按照如下需求，根据一些参考样例，合成和参考样例类似的具有：（1）**相似数据领域**；和（2）**回复质量程度** 的数据用于检验标注人员的能力。
##### 需求
1. 根据参考样例合成具有 {domain} 数据类型的用户 query 数据，关于 {domain} 的详细定义为：{domaindef}
2. 针对合成的用户的 query 数据，合成具有 {responsequality} 质量的response数据。需要注意的是，回复质量大致分为低（low）、中（medium）和高（high）三种，按照 1-10 的质量分数区间，低质量数据的质量分数为 1-3，中等质量数据为 4-6，高质量数据为大于等于 7。
3. 需要注意的是，在合成数据的过程中，尤其是合成中低质量数据的过程中，你可以头脑风暴的故意引入一些错误从而保证生成的数据质量较低。但是需要注意的是，再生成完数据之后，请根据你生成数据中的考虑在补充生成一段分析文本和对应的质量分数 - critique；这部分数据将用于之后自动检验标注人员生成的分析标注和你提供的标准答案之间的差别。
4. 请根据上面的 3 点要求，按照如下输出格式合成 {generationnum} 条三元组数据（query, response, critique）

## 参考样例

如下是部分参考样例。
**需要注意，用户的 query 在样例中可能是多轮的，你可以自由选择最终生成的是多轮的还是单轮作为 query**

```markdown
{reference}
```

## 输出格式
输出最终 {generationnum} 条样本测试数据用于检验标注人员的水平，**请用英文生成**。下面样例中的 // 后面的数据为注释信息，这只是为了更好的解释数据格式和内容的要求，请不要生成这些注释以及任务和数据无关的内容。

```markdown
//第一个生成数据
# Data 1
// 合成的用户输入
## Query:
...
// 合成的 {responsequality} 质量类型的回复数据
## Response:
...
// 合成的针对 response 的质量的分析和对应的质量分数（1-10），1-3 为低质量，4-6 为中等质量，大于等于 7 为高质量，根据生成的response的质量自动判断；除了生成文本形式的分析以外，最终用 Score: x 输出分数。**质量分析应该尽可能详实，不要简略描述文本质量，要细粒度的分析质量好坏的理由和依据。并且最终的质量分数可以是浮点数以便更准确的衡量质量**
## Critique:
...
Score: x

//第二个生成数据
# Data 2
...
```
