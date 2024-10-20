import streamlit as st


def head():
    st.sidebar.header(':nazar_amulet: :blue[Prompt]')

def bottom():

    st.markdown("""
        <style>
        .card {
            background-color: #0E1117;
            color: gray;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        a {
            color: gray !important;  /* リンク文字を黒に設定 */
            text-decoration: none;  /* 下線をなくす */
        }
        a:hover {
            color: gray;  /* ホバー時の色を指定（オプション） */
            text-decoration: none;  /* 下線をなくす */
        }   
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div class="card">
            🌚  Point : <p><small>
            動作環境(Windows等)や使用言語(Python,Node.js等)を指定して下さい。<br>
            </p>
            </small>
        </div>""", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div class="card">
        <small>
        🌑  Respect :<br>
        本アプリケーションは、
        要件定義生成AIである以下の製品・OSSを参考にしています。
        <br>
        <a href="https://www.babel-ai.com/">要件定義システム生成AI Babel</a> <br>
        <a href="https://github.com/dai-motoki/zoltraak">Zoltraak</a><br>
        <a href="https://gearindigo.app/">GEAR.indigo</a>
        </small>
        </div>""", unsafe_allow_html=True)


