import streamlit as st
import google.generativeai as genai
import re

# ① ページ設定
st.set_page_config(page_title="SNS Risk Checker", page_icon="🔥")

# APIキー設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🎨 画像読み込み（ユーザー名は自分のものに変えてね）
@st.cache_data
def load_image():
    user_name = "tsunatsukina" 
    url = f"https://raw.githubusercontent.com/{user_name}/sns-risk-checker/main/flame_cute.png"
    return url

# サイドバーとメイン表示
img = load_image()
with st.sidebar:
    st.image(img, width=150) if img else st.write("🔥")
    st.title("About")
    st.write("SNSライフを守る騎士だにょ…あ、失礼。守護神です。")

st.markdown("<h1 style='text-align: center;'>SNS Risk Checker</h1>", unsafe_allow_html=True)
if img: st.markdown(f'<div style="text-align: center;"><img src="{img}" width="100"></div>', unsafe_allow_html=True)

# 入力欄
user_input = st.text_area("投稿予定の文章:", placeholder="チェックしたい内容を入力...", height=150)

# 診断ロジック
if st.button("リスクを徹底診断！"):
    if user_input:
        with st.spinner('確認中...'):
            try:
                # 1.5-flashなら404エラーが出にくいのでこちらで固定します
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"SNSリスクを分析して。1.【炎上リスク度】: 〇〇% 2.【判定】 3.【理由】 4.【改善案】 5.【謝罪文】の形式で。文章：{user_input}"
                response = model.generate_content(prompt)
                res = response.text

                # ％を抽出して判定
                score = int(re.search(r'(\d+)%', res).group(1)) if re.search(r'(\d+)%', res) else 0

                if score >= 50:
                    st.error(f"### 🚨 リスク度 {score}%：炎上しちゃうよ！")
                elif score >= 30:
                    st.warning(f"### ⚠️ リスク度 {score}%：注意が必要だね")
                else:
                    st.success(f"### ✅ リスク度 {score}%：安心だね！")

                st.subheader("🔍 診断レポート")
                st.info(res)
            except Exception as e:
                st.error(f"エラーだにょ…いや、エラーです: {e}")
    else:
        st.warning("文章を入力してください。")