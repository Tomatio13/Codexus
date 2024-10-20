import streamlit as st

def show():
    st.sidebar.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2E2E2E;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }
        </style>
        <div class="footer">
            &copy; 2024 @Tomatio13
        </div>
        """,
        unsafe_allow_html=True
    )