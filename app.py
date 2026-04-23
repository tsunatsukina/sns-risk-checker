import streamlit as st
import google.generativeai as genai
import re

# ① ページの設定
st.set_page_config(
    page_title="SNS Risk Checker", 
    page_icon="🔥", 
    layout="centered"
)

# APIキーの設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🎨 画像を読み込む関数
@st.cache_data
def load_image():
    # ★ここをご自身のGitHubユーザー名に書き換えてください
    user_name = "tsunatsukina" 
    repo_name = "sns-risk-checker"
    file_name = "flame_cute.png"
    image_url = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/main/{file_name}"
    return image_url

# 画像の取得
try:
    char_image = load_image()
except:
    char_image = None

# ③ サイドバー
with st.sidebar:
    if char_image:
        st.image(char_image, width=150)
    st.title("About")
    st.write("投稿前のひと呼吸。AIと炎の騎士が、あなたのSNSライフを守ります。")

# メイン画面
if char_image:
    st.markdown(f'<div style="text-align: center;"><img src="{char_image}" width="100"></div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #333;'>SNS Risk Checker</h1>", unsafe_allow_html=True)

# 🎨 デザインCSS
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #FF8C00;
    color: white;
    border-radius: 12px;
    border: none;
    height: 3.5em;
    width: 100%;
    font-weight: bold;
    font-size: 1.1em;
}
.stTextArea textarea {
    border-radius: 12px;
}
.stAlert {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# 入力エリア
user_input = st.text_area("投稿予定の文章:", placeholder="チェックしたい内容を入力してください...", height=150)

# 診断ロジック
if st.button("リスクを徹底診断！"):
    if user_input:
        with st.spinner('Gemini 3 が慎重に確認中...'):
            try:
                # 【ここが最重要！】Gemini 3 Flash を指定
                model = genai.GenerativeModel("gemini-3-flash")
                
                prompt = (
                    "あなたはSNSリスク管理のプロフェッショナルです。以下の文章を分析し、必ず以下の形式で回答してください。\n\n"
                    "1. 【炎上リスク度】: 〇〇%\n"
                    "2. 【判定】: 安全・注意・危険の3段階\n"
                    "3. 【理由】: なぜそのリスクがあるのか、簡潔に。\n"
                    "4. 【改善案】: リスクを下げて、より良くなる言い換え案。\n"
                    "5. 【もしもの時の謝罪文】: 万が一批判を受けた際の謝罪例文。\n\n"
                    f"文章：{user_input}"
                )
                
                response = model.generate