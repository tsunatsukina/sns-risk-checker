import streamlit as st
import google.generativeai as genai
from PIL import Image  # 画像を扱うための道具

# ① ページの設定（アイコンも炎に！）
st.set_page_config(
    page_title="SNSリスク守護神「リトル・フレイム」", 
    page_icon="🔥", 
    layout="centered"
)

# 🎨 画像（炎のキャラクター）を読み込む関数
@st.cache_data  # 画像を高速に読み込むための設定
def load_image():
    # GitHub上の画像URLを指定します。
    # ※ 重要：'tsunatsukina' を実際のGitHubユーザー名に書き換えてください！
    user_name = "tsunatsukina" 
    repo_name = "sns-risk-checker" # リポジトリ名が違う場合はここも変更
    file_name = "flame_cute.png"
    image_url = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/main/{file_name}"
    return image_url

# 画像のURLを取得
try:
    flame_image = load_image()
except:
    # もし画像が読み込めなかった場合の予備（絵文字）
    flame_image = "🔥"

# ③ サイドバーの設定
with st.sidebar:
    # --- サイドバーのトップに画像を配置！ ---
    if isinstance(flame_image, str) and flame_image.startswith("http"):
        st.image(flame_image, width=150) 
    else:
        st.title(flame_image) # 予備の絵文字を表示
        
    st.title("💡 使い方")
    st.write("""
    1. 投稿したい文章を貼ります。
    2. 「診断する」を押します。
    3. AIとリトル・フレイムがチェック！
    """)
    st.divider()
    st.caption("powered by Gemini AI & Little Flame")

# メイン画面のタイトル周り
col1, col2 = st.columns([1, 4]) # 画面を横に分割して、画像とタイトルを並べる
with col1:
    # --- タイトルの横に画像を配置！ ---
    if isinstance(flame_image, str) and flame_image.startswith("http"):
        st.image(flame_image, width=80) 
with col2:
    st.title("🛡️ SNSリスク守護神")
    st.subheader("〜 リトル・フレイムがチェック！ 〜")

st.write("あなたの投稿、世界に出しても大丈夫？公開前にAIとリトル・フレイムが最終チェックします。")

# --- ポップにするためのCSS（おまじない） ---
# 炎に合わせてボタンの色を暖色系（赤オレンジ）に。
st.markdown("""
<style>
/* ボタンをポップな赤オレンジ色に */
div.stButton > button:first-child {
    background-color: #FF4500;
    color: white;
    border-radius: 20px;
    border: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
/* 入力欄を丸く */
.stTextArea textarea {
    border-radius: 15px;
}
</style>
""", unsafe_allow_stdio=True)

# (ここから下は、前のコードのAPI設定やボタンの部分をそのまま続けてください)