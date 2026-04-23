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
    user_name = "tsunatsukina" 
    return f"https://raw.githubusercontent.com/{user_name}/sns-risk-checker/main/flame_cute.png"

img_url = load_image()

# サイドバー
with st.sidebar:
    if img_url:
        st.image(img_url, width=150)
    st.title("About")
    st.write("SNS投稿前のリスク診断。")

# メイン画面
st.title("SNS Risk Checker")

user_input = st.text_area("投稿予定の文章:", placeholder="チェックしたい内容を入力...", height=150)

# 診断ボタン
if st.button("リスクを徹底診断！"):
    if user_input:
        with st.spinner('診断中...'):
            try:
                # 【新戦略】利用可能なモデルをリストから自動取得
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # gemini-3があれば優先、なければ1.5、それもなければリストの最初を使用
                target_model = next((m for m in available_models if "gemini-3" in m), 
                               next((m for m in available_models if "gemini-1.5-flash" in m), available_models[0]))
                
                model = genai.GenerativeModel(target_model)
                
                prompt = (
                    "SNSリスクを分析してください。以下の形式で回答すること。\n"
                    "1.【炎上リスク度】: 〇〇%\n"
                    "2.【判定】: 安全・注意・危険\n"
                    "3.【理由】: 理由を詳しく\n"
                    "4.【改善案】: 言い換え案\n"
                    "5.【謝罪文】: 例文\n\n"
                    f"文章：{user_input}"
                )
                
                response = model.generate_content(prompt)
                res = response.text

                # 数値抽出
                score = 0
                match = re.search(r'(\d+)%', res)
                if match:
                    score = int(match.group(1))

                # 判定表示（ポップな色分け）
                if score >= 50:
                    st.error(f"### 🚨 リスク度 {score}%：炎上しちゃうよ！")
                elif score >= 30:
                    st.warning(f"### ⚠️ リスク度 {score}%：注意が必要だね")
                else:
                    st.success(f"### ✅ リスク度 {score}%：安心だね！")

                st.subheader("🔍 診断レポート")
                st.info(res)
                
            except Exception as e:
                st.error("システムエラーが発生しました。")
                st.code(f"Error: {e}")
    else:
        st.warning("文章を入力してください。")