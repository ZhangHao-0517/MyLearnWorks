from langchain.prompts import ChatPromptTemplate#定义出第一个和第三个任务所需的提示模版
from langchain_openai import ChatOpenAI#导入聊天模型
#import os

#创建generate_script这个函数，可以通过调用它来得到视频的标题和脚本内容
def generate_script(subject, video_length, creativity, api_key):
    #视频的主题：subject，视频的时长：video_length,视频脚本的创造性：creativity,API密钥：api_key，因为这次使用用户的密钥而非自己的token
    # 从AI获得标题的提示模版：title_template
    title_template = ChatPromptTemplate.from_messages(
        [
            #消息提示模版包含：从AI获得的标题
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )

    #从AI获得脚本内容的提示模版:script_template
    script_template = ChatPromptTemplate.from_messages(
        [
            #消息提示模版包含：从AI获得的标题，从用户那里获得的时长信息
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             """)
        ]
    )

    #我们定义一个模型，给它命名为model
    """
    model：使用的模型，这里我们使用——"deepseek-chat"
    deepseek_api_key：deepseek的密钥——api_key
    base_url：基地址参数，可以决定我们客户端发送请求的目标服务器地址——"https://api.deepseek.com/v1"
    temperature：创造性——creativity
    """
    model = ChatOpenAI(model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
    temperature = creativity)

    #我们用链，获得标题，
    title_chain = title_template | model#这个链名为title_chain，用于得到视频标题的链
    script_chain = script_template | model#这个链名为script_chain，用于得到脚本

    title = title_chain.invoke({"subject": subject}).content#通过Ai得到的视频标题，存放于变量title中

    # 通过Ai得到的视频内容，存放于变量script中
    script = script_chain.invoke({"title": title, "duration": video_length}).content

    return  title, script#返回得到的视频标题和视频内容

#print(generate_script("sora模型", 1, 0.7, os.getenv("DEEPSEEK_API_KEY")))