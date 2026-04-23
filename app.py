import streamlit as st
import google.generativeai as genai
import re

# --- 1. 鍵の差し込み ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# スクリーンショットに表示されていた最新モデル名を指定
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- 2. 見た目の設定 ---
st.set_page_config(page_title="SNSリスク守護神", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(to right, #4b6cb7, #182848);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    .risk-box {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. メイン画面 ---
st.title("🛡️ SNSリスク守護神")
st.write("「必死に炎上を食い止める」最新AIが参上しました。")

user_input = st.text_area("✍️ 投稿の『下書き』をどうぞ:", placeholder="ここに入力した内容は、まだ誰にも見られません...", height=150)

if st.button("🚀 リスク診断を実行"):
    if user_input:
        with st.spinner('AIが必死に炎上を食い止めています...'):
            try:
                prompt = f"""
                あなたは伝説のSNSリスク管理エキスパートです。
                シニカルだけど愛のある口調で、以下の投稿を分析してください。

                【炎上期待値】0〜100の数値と理由
                【エキスパートの独り言】問題点の指摘
                【平和な世界線への書き換え】改善案
                【万が一の鎮火用テンプレート】謝罪文

                投稿文：{user_input}
                """

                response = model.generate_content(prompt)
                text = response.text

                # 数値を抽出して色分け
                score_match = re.search(r'\d+', text)
                score = int(score_match.group()) if score_match else 50

                if score <= 30: bg_color, status = "#28a745", "✅ ほぼ安全！"
                elif score <= 70: bg_color, status = "#ffc107", "⚠️ 要注意！"
                else: bg_color, status = "#dc3545", "🚫 激ヤバ！"

                st.markdown(f"""
                    <div class="risk-box" style="background-color: {bg_color};">
                        炎上リスク：{score}%<br>
                        <span style="font-size: 16px;">{status}</span>
                    </div>
                """, unsafe_allow_html=True)

                st.success("✅ 鑑定完了！")
                st.write(text)
                
            except Exception as e:
                st.error(f"エラーが発生しました。")
                st.info(f"詳細: {e}")
    else:
        st.warning("⚠️ 文章を入力してください")

st.caption("© 2026 SNSリスク守護神プロジェクト")