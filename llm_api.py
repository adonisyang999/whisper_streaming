import qianfan #百度-千帆大模型SDK
import re
import dashscope # 阿里-通义大模型SDK
from http import HTTPStatus
# todo 增加response服务调用失败检查
# 文心一言官方文档：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/3lmokh7n6#%E3%80%90%E4%B8%8D%E6%8E%A8%E8%8D%90%E3%80%91%E4%BD%BF%E7%94%A8%E5%BA%94%E7%94%A8aksk%E8%B0%83%E7%94%A8%E6%B5%81%E7%A8%8B
# 通义千问官方文档：https://help.aliyun.com/zh/dashscope/developer-reference/api-details?spm=a2c4g.11186623.0.0.160d46c1hVUsfg
class ChatBot():
    def __init__(self, model_type):
        '''model_type: 1.文心一言4.0模型 2.千问通义模型'''
        self.history_message = [] # 存储历史对话消息
        self.model_type = model_type
        if model_type == 1:
            self.chat_completion = qianfan.ChatCompletion(ak="lCSKCdpUaXrHmCNGLZqNKQMR"
                                                          ,sk="obgxYHuT0mQnL1ZSRrAE5eGTOonznnN2") # API_KEY,Secret_KEY
        elif model_type == 2:
            dashscope.api_key = "sk-2553f243955f43ab8be24ff431d9091f"
        else:
            raise Exception("model_type error")

    def initialize(self):
        self.history_message = []
        init_content = "聊天定位：你是一个玩具店的机器人，用户会描述他想要的娃娃的特征，你需要判断出用户想要的是哪个娃娃，然后按照格式{chat:[content],return:[object]}进行输出，[content]部分为你和用户交互的内容，[object]部分输出用户想要的玩偶。你的语调要友善亲人。 场景描述：有4个娃娃，分别是[编号：A，描述：一只灰白相间的狗],[编号：B，描述：一只蓝白相间的狗],[编号：C，描述：一只橙色的老鼠],[编号：D，描述：一只黄色的鸭子]。 单轮示例： 输入：{我想要那只可达鸭} 输出：{chat:[根据你的描述，送给你这只鸭子，祝你开心。],return:[D]} 多轮示例： 输入：{我想要那个小狗} 输出：{chat:[小狗有灰⾊的和蓝⾊的，你更喜欢哪⼀个呢？],return:[]} 输入：{随便哪⼀个都好} 输出：{chat:[那我送你灰⾊的小狗，希望你喜欢它],return:[A]} 限制：1. 每个娃娃被送出后数量都会减少。2. 检查所需娃娃是否存在。 3. 如果无法准确判断用户想要的娃娃，不要编造结果，要多轮对话继续询问用户。 4. 直到最后确定要送的娃娃才给[object]赋值，否则[object]都为空。 下面我将给出实际的输入，你准备好回答了吗，你的回答必须必须按照格式{chat:[content],return:[object]}。"
        self.send_message(init_content)

    def send_message(self,content):
        # 存储对话信息
        self.history_message.append({
            "role": "user",
            "content": content
        })
        # 指定特定模型
        if self.model_type == 1:# 文心一言4.0模型 ERNIE-4.0-8K
            resp = self.chat_completion.do(model="ERNIE-4.0-8K",
                                           messages=self.history_message,
                                           max_output_tokens=100)
            result = resp["body"]['result']
        elif self.model_type == 2:# 千问通义2.5模型 qwen-max
            response = dashscope.Generation.call(model="qwen-max",
                                                 messages=self.history_message,
                                                 max_tokens=100,
                                                 result_format='message')
            result = response.output.choices[0]['message']['content']
        else:
            raise Exception("model_type error")

        # 解析回复格式
        valid = self.check_format(result)
        if not valid :
            print(f"invalid response:{result}")
            result = ' '

        self.history_message.append({
            "role": "assistant",
            "content": result
        })

        return result

    def check_format(self,result):
        '''查找result字符串是否包含由{}框柱的子字符串，如果包含则返回True，否则返回False'''
        pattern = r'^\{chat:(.*?)return:(.*?)\}$'
        match = re.search(pattern, result)
        if match:
            chat_content = match.group(1)  # 第一个捕获组，即 chat 后面的内容
            return_content = match.group(2)  # 第二个捕获组，即 return 后面的内容
            # print("格式输出结果:",chat_content,return_content)
            return True
        else:
            return False



if __name__ == '__main__':
    bot = ChatBot(model_type=2)
    bot.initialize()
    while 1:
        content = input("用户：")
        result = bot.send_message(content)
        print("机器人：", result)