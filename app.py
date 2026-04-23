import streamlit as st
import google.generativeai as genai
import re

# ① ページ設定
st.set_page_config(page_title="SNS Risk Checker", page_icon="🔥")

# APIキー設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🎨 画像読み込み
@st.cache_data
def load_image():
    # ★ここを自分のGitHubユーザー名に変えてください
    user_name = "tsunatsukina" 
    url = f"https://raw.githubusercontent.com/{user_name}/sns-risk-checker/main/flame_cute.png"
    return url

# サイドバーの表示（ここを修正しました）
img_url = load_image()
with st.sidebar:
    if img_url:
        st.image(img_url, width=150)
    else:
        st.write("🔥")
    st.title("About")
    st.write("投稿前のリスクチェック。")

# メイン画面
st.title("SNS Risk Checker")
if img_url:
    st.image(img_url, width=100)

# 入力欄
user_input = st.text_area("投稿予定の文章:", placeholder="チェックしたい内容を入力...", height=150)

# 診断ボタン
if st.button("リスクを徹底診断！"):
    if user_input:
        with st.spinner('確認中...'):
            try:
                # 安定版の1.5-flashを使用
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"SNSリスクを分析して。1.【炎上リスク度】: 〇〇% 2.【判定】 3.【理由】 4.【改善案】 5.【謝罪文】の形式で。文章：{user_input}"
                response = model.generate_content(prompt)
                res = response.text

                # 数値の取り出し
                score = 0
                match = re.search(r'(\d+)%', res)
                if match:
                    score = int(match.group(1))

                # 警告の表示
                if score >= 50:
                    st.error(f"### 🚨 リスク度 {score}%：炎上しちゃうよ！")
                elif score >= 30:
                    st.warning(f"### ⚠️ リスク度 {score}%：注意が必要だね")
                else:
                    st.success(f"### ✅ リスク度 {score}%：安心だね！")

                st.subheader("🔍 診断レポート")
                st.info(res)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("文章を入力してください。")