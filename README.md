# Line Talk Statistic

## User Guide
- Prepare the chat record in line with txt file format.
- Replace dataset path in `__main__`.
- The program could generate chart about room information each user.

## Feature
- Compare speak ratio in the chat room
- Compare word of speak ratio in the chat room
- Compare setiment grade for each user in the char room

## Setiment Analysis
In this feature,  class `Sentance_parser` use snowNLP package, and use `sentiments()` to determine each sentence's setiment grade. In the end, class `Sentance_parser` sum up all grades and plot box graph, providing graph data could be analyzed by user.

Here is the table of sentiment grade level:

|  Sentiment Grade | Interpretation |
 | -------- | -------- |
 |0.0 - 0.2 | Very Negative |
 |0.2 - 0.4 | Negative |
 |0.4 - 0.6 | Neutral |
 |0.6 - 0.8 | Positive |
 |0.8 - 1.0 | Very Positive |

## Remark
If you need chineese word in your graph, please follow this article:
https://www.twblogs.net/a/5d70dbebbd9eee541c33feb9
