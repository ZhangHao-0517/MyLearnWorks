import streamlit as st#导入streamlit库
from utils import generate_script#导入上节课创建的utils.py文件中的generate_script函数

st.title("🎬 视频脚本生成器")#给网页上加一个标题
#运行网站：点开终端，输入streamlit run +文件名字，比如我们是main.py文件下引用的streamlit库，我们就streamlit run main.py

with st.sidebar:#添加侧边栏，这行下面所有前边有缩进的内容都会出现在侧边栏下面
    api_key = st.text_input("请输入DeepSEEK API密钥：", type="password")#文字输入框，用deepseek_api_key这个变量去保存用户的输入
    st.markdown("[获取Deepseek API密钥](https://api-docs.deepseek.com/zh-cn/)")#在网页上添加markdown内容，超链接，这里是链接的markdown语法

#文字输入框，用streamlit的text_input组件，用名为subject的变量接收用户的输入，这里是视频主题
subject = st.text_input("💡 请输入视频的主题")
#数字输入框，用streamlit的number_input组件，直接就是浮点数类型，用名为video_length的变量接收用户的输入，这里是视频时长，是个浮点数
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
#用streamlit的slider组件，实现可以让用户可以拖拽的效果
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
#添加按钮，用streamlit的button函数，参数就是按钮上的文字
submit = st.button("生成脚本")

if submit and not api_key:#如果点击生成按钮但没输入密钥
    #展示提示信息，用streamlit的info函数
    st.info("请输入你的OpenAI API密钥")
    #streamlit的stop函数作用是执行到这里之后，之后的代码都不会执行啦
    st.stop()
if submit and not subject:#如果点击生成按钮但没输入视频主题
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:#如果点击生成按钮但视频时长小于0.1分钟
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit:#如果点击了生成按钮
    #with + streamlit的spinner组件，就会显示加载中的效果，只有对这段代码下面的缩进有效
    with st.spinner("AI正在思考中，请稍等..."):
        #标题和脚本内容分别赋值
        title, script = generate_script(subject, video_length, creativity, api_key)
    #streamlit的success用于展示成功运行的信息
    st.success("视频脚本已生成！")
    #streamlit的subheader用于展示副标题
    st.subheader("🔥 标题：")
    #streamlit的write用于吧括号里 参数写在下方
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
