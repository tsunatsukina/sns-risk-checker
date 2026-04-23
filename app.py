import streamlit as st
import google.generativeai as genai
import re

# ① ページ設定
st.set_page_config(page_title="SNS Risk Checker", page_icon="🔥")

# APIキー設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🎨 画像読み込み（ユーザー名を書き換えてください）
@st.cache_data
def load_image():
    user_name = "tsunatsukina" 
    url = f"https://raw.githubusercontent.com/{user_name}/sns-risk-checker/main/flame_cute.png"
    return url

img_url = load_image()

# サイドバー
with st.sidebar:
    if img_url:
        st.image(img_url, width=150)
    else:
        st.write("🔥")
    st.title("About")
    st.write("SNS投稿前のリスク診断。")

# メイン画面
st.title("SNS Risk Checker")
if img_url:
    st.image(img_url, width=100)

user_input = st.text_area("投稿予定の文章:", placeholder="チェックしたい内容を入力...", height=150)

# 診断ボタン
if st.button("リスクを徹底診断！"):
    if user_input:
        with st.spinner('診断中...'):
            try:
                # 【ここを修正】v1beta環境でもっともエラーが出にくい指定方法です
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                
                prompt = f"SNSリスクをプロの視点で分析してください。以下の形式で回答して。1.【炎上リスク度】: 〇〇% 2.【判定】 3.【理由】 4.【改善案】 5.【謝罪文】\n文章：{user_input}"
                
                # API呼び出し
                response = model.generate_content(prompt)
                res = response.text

                # 数値抽出
                score = 0
                match = re.search(r'(\d+)%', res)
                if match:
                    score = int(match.group(1))

                # 判定表示
                if score >= 50:
                    st.error(f"### 🚨 リスク度 {score}%：炎上しちゃうよ！")
                elif score >= 30:
                    st.warning(f"### ⚠️ リスク度 {score}%：注意が必要だね")
                else:
                    st.success(f"### ✅ リスク度 {score}%：安心だね！")

                st.subheader("🔍 診断レポート")
                st.info(res)
                
            except Exception as e:
                # ここでエラーが出た場合、別のモデル名での接続を試みる
                st.error("モデルの接続でエラーが発生しました。予備の接続を試みてください。")
                st.code(f"Error Details: {e}")
    else:
        st.warning("文章を入力してください。")