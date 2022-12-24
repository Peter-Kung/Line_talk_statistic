import os
import matplotlib
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
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
                    username = s[1]
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

        for date, conversation_list in talk_data.items():
            for dictionary in conversation_list:
                for username in dictionary.keys():    
                    if username in user_dict: 
                        user_dict[username]+=1
                    else:
                        user_dict[username] = 1

        return user_dict.keys(), user_dict.values()

    def user_word_count(self, talk_data):

        user_dict = {}

        for date, conversation_list in talk_data.items():
            for dictionary in conversation_list:
                for username, context in dictionary.items():    

                    word_count = self.str_count(sentence=context)

                    if username in user_dict: 
                        user_dict[username] += word_count
                    else:
                        user_dict[username] = word_count
                    
        return user_dict.keys(), user_dict.values()

    def str_count(self, sentence: str):
        '''找出字符串中的中文字符的个数'''
        count_zh =  0
        for s in sentence:
            # 中文
            if s.isalpha():
                count_zh += 1

        return count_zh

    def generate_pie_fig(self, 
                save_path: str,
                figure_name: str,
                attr_list: list,
                value_list: list):
        
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        plt.cla()
        plt.figure(figsize=(6,9)) 

        # separeted = (0, 0, 0, 0.3, 0.3, 0,0)    # 依據類別數量，分別設定要突出的區塊
        plt.pie(value_list, 
                autopct = "%1.1f%%", 
                # explode = separeted,            # 設定分隔的區塊位置
                labels = attr_list,
                startangle = 90, 
                pctdistance=0.9,
                textprops = {"fontsize" : 12}, 
                shadow=True)

        plt.axis('equal')                          # 使圓餅圖比例相等
        plt.title(figure_name, {"fontsize" : 18})  # 設定標題及其文字大
        plt.legend(loc="best")
        plt.savefig(f'{save_path}/{figure_name}',
                    bbox_inches='tight',           # 去除座標軸占用的空間
                    pad_inches=0.0)                # 去除所有白邊)
        

if __name__ == '__main__':

    dataset_path = './dataset.txt'

    # plt.figure(figsize=(5, 6.5))    
    plt.figure(figsize=(6,9)) 

    with Sentance_parser(dataset_path) as sp:
        talk_data = sp.parse()
        x, y = sp.user_sentence_count(talk_data)
        sp.generate_pie_fig(save_path='./figure', 
                            figure_name='sentence_count', 
                            attr_list=x, 
                            value_list=y)

        x, y = sp.user_word_count(talk_data)
        sp.generate_pie_fig(save_path='./figure', 
                            figure_name='word_count', 
                            attr_list=x, 
                            value_list=y)