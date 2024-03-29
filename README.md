# Line Talk Statistic

## Prerequisites
- Donwload chat content in txt file from LINE chat room.
- Chatting context could be downloaded via setting view in chat room.

## User Guide
- Prepare the chat record in line with txt file format.
- Replace dataset path in `__main__`.
- The program could generate chart about room information each user.

## Features
- Compare speak ratio in the chat room.
- Compare word of speak ratio in the chat room.
- Compare setiment grade for each user in the chat room.

## Setiment Analysis
In this feature,  class `Sentance_parser` use snowNLP package, and use `sentiments()` to determine each sentence's setiment grade. In the end, class `Sentance_parser` assembles all grades into a list and plot box graph, providing graph data could be analyzed by user.

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

[word font](http://www.font5.com.cn/font_download.php?id=151&part=1237887120)

[Setting](https://andy6804tw.github.io/2022/06/17/colab-plt-chinese/)

## Reference
[Seaborn](https://ithelp.ithome.com.tw/articles/10234188)

[ICT-Python-101](https://github.com/willismax/ICT-Python-101/blob/master/13.Python%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90%E6%87%89%E7%94%A8-%E8%AA%9E%E6%84%8F%E5%88%86%E6%9E%90%E7%AF%87NLP.ipynb)

[tqdm](https://blog.csdn.net/qq_40666028/article/details/79335961)

[ChatGPT](https://openai.com/blog/chatgpt/)