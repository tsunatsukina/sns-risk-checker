import streamlit as st
import google.generativeai as genai

# ① ページの設定
st.set_page_config(
    page_title="SNSリスク守護神「リトル・フレイム」", 
    page_icon="🔥", 
    layout="centered"
)

# APIキーの設定（Secretsから読み込み）
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🎨 画像（炎のキャラクター）を読み込む関数
@st.cache_data
def load_image():
    # tsunatsukina
    user_name = "tsunatsukina" 
    repo_name = "sns-risk-checker"
    file_name = "flame_cute.png"
    image_url = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/main/{file_name}"
    return image_url

# 画像のURLを取得
try:
    flame_image = load_image()
except:
    flame_image = "🔥"

# ③ サイドバーの設定
with st.sidebar:
    if isinstance(flame_image, str) and flame_image.startswith("http"):
        st.image(flame_image, width=150) 
    else:
        st.title("🔥")
        
    st.title("💡 使い方")
    st.write("""
    1. 下の入力欄に投稿したい文章を貼るよ。
    2. 「診断する」ボタンを押すよ。
    3. AIとリトル・フレイムが炎上リスクをチェックするよ！
    """)
    st.divider()
    st.caption("powered by Gemini AI & Little Flame")

# メイン画面のタイトル周り
col1, col2 = st.columns([1, 4])
with col1:
    if isinstance(flame_image, str) and flame_image.startswith("http"):
        st.image(flame_image, width=80) 
with col2:
    st.title("🛡️ SNSリスク守護神")
    st.subheader("〜 リトル・フレイムが守るよ〜 〜")

st.write("あなたの投稿、世界に出しても大丈夫？公開前にリトル・フレイムが最終チェックします。")

# 入力エリア
user_input = st.text_area("投稿予定の文章を入力してください:", placeholder="ここに文章をペーストしてね")

# 🎨 ポップなボタンとデザインのCSS（修正済み）
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #FF4500;
    color: white;
    border-radius: 20px;
    border: none;
    height: 3em;
    width: 100%;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.stTextArea textarea {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# 診断ロジック
if st.