import os, re
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import seaborn as sns

from snownlp import SnowNLP

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.family']='sans-serif' 
plt.rcParams['axes.unicode_minus'] = False

'''
@input: talk sentence.txt
@output: figure of analysis
'''
class Sentance_parser:

    path = ""

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        print('Start!!')
        return self

    def __exit__(self, exec_type, exc_value, tb):
        if exec_type:
            print('exec_type: ', exec_type)
            print('exec_value: ', exc_value)
            print('tb: ', tb)
        else:
            print('Done')

    def validate_date(self, date: str):
        try:
            datetime.strptime(date, '%Y/%m/%d')
            return True
        except ValueError:
            return False
    
    def validate_time(self, date: str):
        try:
            datetime.strptime(date, '%H:%M')
            return True
        except ValueError:
            return False

    def str_count(self, sentence: str):
        '''找出字符串中的中文字符的个数'''
        count_zh =  0
        for s in sentence:
            # 中文
            if s.isalpha():
                count_zh += 1

        return count_zh

    def parse(self):
    
        date_dict = {}
        current_date = ""

        with open(self.path) as f:
            for line in f.readlines():
                s = line.split('	')
                
                date_str = s[0][:10]
                time_str = s[0]
                if self.validate_date(date_str):
                    date_dict[date_str] = []
                    current_date = date_str
                elif self.validate_time(time_str):
                    # 匹配不是中文、大小写、数字的其他字符
                    cop =  re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
                    username = cop.sub('', s[1])
                    sentance = s[2]
                    date_dict[current_date].append({username: sentance})

        """
        data format: 
        
        date_dict -> 
        {
            date1: [
                { user1: sentance }, 
                { user2: sentance }, 
                ...
            ], 
            date2: [
                { user1: sentance }, 
                { user2: sentance }, 
                ...
            ],
            ...
        }
        """

        # print(date_dict)
        return date_dict


    '''
    @input: conversation
    @output: user and times of speak
    '''
    def user_sentence_count(self, talk_data):

        user_dict = {}

        # Get the total number of conversations
        total_conversations = sum(len(conversation_list) for conversation_list in talk_data.values())

        # Initialize the progress bar
        pbar = tqdm(total=total_conversations)

        for date, conversation_list in talk_data.items():
            for dictionary in conversation_list:
                for username in dictionary.keys():    
                    if username in user_dict: 
                        user_dict[username] += 1
                    else:
                        user_dict[username] = 1
                 # Update the progress bar manually
                pbar.update()

        # Close the progress bar
        pbar.close()

        return user_dict.keys(), user_dict.values()

    '''
    @input: conversation
    @output: user and speak context per each user
    '''
    def user_word_count(self, talk_data):

        user_dict = {}

        # Get the total number of conversations
        total_conversations = sum(len(conversation_list) for conversation_list in talk_data.values())

        # Initialize the progress bar
        pbar = tqdm(total=total_conversations)

        for date, conversation_list in talk_data.items():
            for dictionary in conversation_list:
                for username, context in dictionary.items():    

                    word_count = self.str_count(sentence=context)

                    if username in user_dict: 
                        user_dict[username] += word_count
                    else:
                        user_dict[username] = word_count

                # Update the progress bar manually
                pbar.update()

        # Close the progress bar
        pbar.close()
                    
        return user_dict.keys(), user_dict.values()

    '''
          Grade	    Interpretation
        0.0 - 0.2	Very Negative
        0.2 - 0.4	Negative
        0.4 - 0.6	Neutral
        0.6 - 0.8	Positive
        0.8 - 1.0	Very Positive
    '''
    def do_sentiment_analyze(self, text):
        s = SnowNLP(text)
        return s.sentiments
    
    '''
    @input: conversation
    @output: computed grade of user's sentiment with sentence said
    '''
    def user_sentiment_staticstic(self, talk_data):

        user_sentence_sentiments_grade_dict = {}

         # Get the total number of conversations
        total_conversations = sum(len(conversation_list) for conversation_list in talk_data.values())

        # Initialize the progress bar
        pbar = tqdm(total=total_conversations)

        for date, conversation_list in talk_data.items():
            for dictionary in conversation_list:
                for username, sentence in dictionary.items():    
                    if username in user_sentence_sentiments_grade_dict: 
                        user_sentence_sentiments_grade_dict[username].append(self.do_sentiment_analyze(sentence))
                    else:
                        user_sentence_sentiments_grade_dict[username] = [self.do_sentiment_analyze(sentence)]

                 # Update the progress bar manually
                pbar.update()

        # Close the progress bar
        pbar.close()

        return user_sentence_sentiments_grade_dict

    def generate_pie_fig(self, 
                save_path: str,
                figure_name: str,
                attr_list: list,
                value_list: list):
        
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        plt.cla()
        # plt.figure(figsize=(6,9)) 

        # separeted = (0, 0, 0, 0.3, 0.3, 0,0)    # 依據類別數量，分別設定要突出的區塊
        plt.pie(value_list, 
                autopct = "%1.1f%%", 
                # explode = separeted,            # 設定分隔的區塊位置
                labels = attr_list,
                startangle = 90, 
                pctdistance=0.9,
                textprops = {"fontsize" : 12}, 
                shadow=True)

        plt.tight_layout()
        plt.title(figure_name, {"fontsize" : 18})  # 設定標題及其文字大
        # plt.legend(loc="best")
        plt.savefig(f'{save_path}/{figure_name}',
                    bbox_inches='tight',           # 去除座標軸占用的空間
                    pad_inches=0.0)                # 去除所有白邊

    def generate_box_fig(self,
                        save_path: str,
                        figure_name: str,
                        talk_data: {}):
        
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        '''
        - data framelize dictionary
        - remark:
            Because the sentences of everyone said is not the same quntity, 
            i replace short list(represents each user all sentences) NAN with 
            not enough long length.
        '''
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in talk_data.items()]))
        
        # clean previous canvus
        plt.cla()
        
        plt.tight_layout()
        # draw
        sns.boxplot(data=df)
        plt.title(figure_name, {"fontsize" : 18})  # 設定標題及其文字大
        plt.savefig(f'{save_path}/{figure_name}',
                    bbox_inches='tight',           # 去除座標軸占用的空間
                    pad_inches=0.0)                # 去除所有白邊


if __name__ == '__main__':

    dataset_path = './dataset.txt'

    with Sentance_parser(dataset_path) as sp:
        talk_data = sp.parse()

        # sentiment analysis
        parsed_dict = sp.user_sentiment_staticstic(talk_data)
        sp.generate_box_fig(save_path='./figure',
                        figure_name='Sentiment Staticstic',
                        talk_data=parsed_dict)
        
        x, y = sp.user_sentence_count(talk_data)
        sp.generate_pie_fig(save_path='./figure', 
                            figure_name='Sentence Count', 
                            attr_list=x, 
                            value_list=y)

        x, y = sp.user_word_count(talk_data)
        sp.generate_pie_fig(save_path='./figure', 
                            figure_name='Word Count', 
                            attr_list=x, 
                            value_list=y)
        

