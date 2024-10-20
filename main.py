import streamlit as st
import logging
import yaml
from require_generator import RequirementGenerator
from file_manager import FileManager
import utils.header as header
import utils.sidebar as sidebar
import utils.footer as footer
import os

# 設定ファイルを読み込む
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# ログディレクトリとファイルパスを設定ファイルから取得
LOG_DIR = config['log']['directory']
LOG_FILE_PATH = os.path.join(LOG_DIR, config['log']['file'])

# ログディレクトリが存在しない場合は作成
os.makedirs(LOG_DIR, exist_ok=True)

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

requirement_generator = RequirementGenerator()
file_manager = FileManager(config)

# 他の関数も設定ファイルに基づいて更新

def generate_requirement(require_system, folder_name, feedback):
    with st.spinner('要件定義書を生成中...'):
        try:
            if feedback:
                requirements = st.session_state.generated_requirement
            else:
                requirements_filepath = config['templates']['requirements']
                requirements = file_manager.read_requirements(requirements_filepath)
                requirements = requirements.replace("{作りたいアプリ}", require_system)
                
            generated_requirement = requirement_generator.generate_requirement(require_system, requirements, feedback)
            
            with st.expander("要件定義書"):
                st.markdown(file_manager.replace_headings(generated_requirement))

            md_filename = folder_name +"/"+ "generated_requirement.md"
            file_manager.create_file(md_filename, generated_requirement)
            return generated_requirement
        except Exception as e:
            logger.error(f"Error during requirement generation: {e}")
            st.error("Error during requirement generation")

def generate_design_document(require_system, generated_requirement, folder_name):
    with st.spinner('詳細設計書を作成中...'):
        try:
            with st.expander("詳細設計書"):
                design_filepath = config['templates']['design']
                detail_desgin = file_manager.read_requirements(design_filepath)
                generated_detail_design = requirement_generator.generate_detail_design(require_system, generated_requirement, detail_desgin)
                st.markdown(file_manager.replace_headings(generated_detail_design))
                
            md_filename = folder_name + "/"+"generated_detail_desgin.md"
            file_manager.create_file(md_filename, generated_detail_design)

            return generated_detail_design
        except Exception as e:
            logger.error(f"Error during design document generation: {e}")
            st.error("Error during design document generation")

def process_and_display_files(require_system, generated_detail_design, folder_name):
    with st.spinner('ソースコードを生成中...'):
        try:
            with st.expander("ソースコード"):
                design_filepath = config['templates']['code']
                code_prompt = file_manager.read_requirements(design_filepath)
                generated_code = requirement_generator.generate_code(require_system, generated_detail_design, code_prompt)

                parsed_files = requirement_generator.parse_generated_code(generated_code)

                display_and_create_files(parsed_files, folder_name, file_manager)
        except Exception as e:
            logger.error(f"Error during source code generation: {e}")
            st.error("Error during source code generation")

def display_and_create_files(parsed_files, folder_name, file_manager):
    try:
        extension_to_language = file_manager.get_extention_language_mapping()
        for file in parsed_files:
            filename = folder_name +"/"+ file['filename']
            file_code = file['code']
            file_extension = filename.split('.')[-1]
            base_filename = file['filename'].split('/')[-1]
            language = 'docker' if base_filename == 'Dockerfile' else extension_to_language.get(file_extension, '')
            file_manager.create_file(filename, file_code)

            st.write(f"**Filename: {filename}**")
            st.code(file_code, language=language)
    except Exception as e:
        logger.error(f"Error during file creation/display: {e}")
        st.error("Error during file creation/display")

def create_and_download_zip(folder_name):
    try:
        zip_filename = folder_name.rstrip("/") + ".zip"
        file_manager.zip_folder(folder_name, folder_name.rstrip("/"))
        href = file_manager.get_binary_file_downloader_html(zip_filename)
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error during zip creation/download: {e}")
        st.error("Error during zip creation/download")

def process_requirements_and_generate_documents(require_system, folder_name, feedback):
    try:
        st.session_state.generated_requirement = generate_requirement(require_system, folder_name, feedback)
        st.session_state.generated_detail_design = generate_design_document(require_system, st.session_state.generated_requirement, folder_name)
        process_and_display_files(require_system, st.session_state.generated_detail_design, folder_name)
        create_and_download_zip(folder_name)
        st.session_state.show_feedback_input = True
    except Exception as e:
        logger.error(f"Error during the full process: {e}")
        st.error("Error during the full process")

def handle_uploaded_requirement_file(uploaded_file):
    try:
        require_text = uploaded_file.getvalue().decode("utf-8")
        st.session_state.generated_requirement = require_text
        first_line = require_text.split('\n')[0]
        st.session_state.require_system = first_line
        st.session_state.folder_name = requirement_generator.generate_filename(st.session_state.require_system, config['output']['base_directory'])

        with st.expander("アップロード済み要件定義書"):
            st.markdown(file_manager.replace_headings(require_text))

        st.session_state.generated_detail_design = generate_design_document(st.session_state.require_system, st.session_state.generated_requirement, st.session_state.folder_name)
        process_and_display_files(st.session_state.require_system, st.session_state.generated_detail_design, st.session_state.folder_name)
        create_and_download_zip(st.session_state.folder_name)
        st.session_state.show_feedback_input = True
    except Exception as e:
        logger.error(f"Error handling uploaded requirement file: {e}")
        st.error("Error handling uploaded requirement file")

def main():
    st.set_page_config(page_title="SourceCodeIsCool", layout="wide", page_icon=":wind_blowing_face:")

    # ヘッダー表示
    header.show()
    sidebar.head()

    # サイドバー
    input_method = st.sidebar.selectbox("入力方法を選択してください：", ("プロンプト", "ファイルアップロード"))

    if input_method == "プロンプト":
        st.session_state.require_system = st.sidebar.text_area("作りたいシステムの概要を記入して下さい：", value="", height=300)
        uploaded_requirement = None
    elif input_method == "ファイルアップロード":
        uploaded_requirement = st.sidebar.file_uploader("要件定義書をアップロード", type=["md"])
        st.session_state.require_system = ""
        
    if st.sidebar.button(":blue[Generate]"):
        try:
            # st.session_stateの初期化
            st.session_state.folder_name = ""
            st.session_state.generated_requirement = ""
            st.session_state.generated_detail_design = ""
            st.session_state.show_feedback_input = False
            st.session_state.feedback = ""

            if input_method == "ファイルアップロード" and uploaded_requirement:
                handle_uploaded_requirement_file(uploaded_requirement)
            elif input_method == "プロンプト" and st.session_state.require_system:
                st.session_state.folder_name = requirement_generator.generate_filename(st.session_state.require_system, config['output']['base_directory'])
                process_requirements_and_generate_documents(st.session_state.require_system, st.session_state.folder_name, "")
            else:
                st.error("入力方法を選択してください。")

        except Exception as e:
            logger.error(f"Error during initialization or file name generation: {e}")
            st.error("Error during initialization or file name generation")

    # 条件確認を行い二重生成の回避とフィードバック入力表示の管理
    if "generated_requirement" in st.session_state and st.session_state.generated_requirement:
        # フィードバック入力を表示
        if st.session_state.show_feedback_input:
            try:
                feedback_text = st.chat_input("要件定義書の修正内容があれば記入して下さい。")
                st.session_state.feedback = feedback_text
                if st.session_state.feedback:
                    file_manager.delete_folder(st.session_state.folder_name)
                    process_requirements_and_generate_documents(st.session_state.require_system, st.session_state.folder_name, st.session_state.feedback)
                    st.session_state.feedback = ""
            except Exception as e:
                logger.error(f"Error during feedback processing: {e}")
                st.error("Error during feedback processing")

    sidebar.bottom()
    footer.show()

if __name__ == "__main__":
    if 'require_system' not in st.session_state:
        st.session_state.require_system = ""
    if 'folder_name' not in st.session_state:
        st.session_state.folder_name = ""
    if 'generated_requirement' not in st.session_state:
        st.session_state.generated_requirement = ""
    if 'generated_detail_design' not in st.session_state:
        st.session_state.generated_detail_design = ""
    if 'show_feedback_input' not in st.session_state:
        st.session_state.show_feedback_input = False
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
    # ログインチェック
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    main()
