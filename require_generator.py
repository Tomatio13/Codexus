import openai
from pydantic import BaseModel
import json
import os
import logging
from dotenv import load_dotenv
from os.path import join, dirname
import anthropic

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)

# Define data models using Pydantic
class FileName(BaseModel):
    filename: str

class Code(BaseModel):
    filename: str
    code: str

class GeneratedCode(BaseModel):
    source_file: list[Code]

class RequirementGenerator:
    def __init__(self):
        # Determine which provider to use based on environment variables
        self.provider = os.environ.get("PROVIDER")
        self.model = os.environ.get("MODEL")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.ollama_base_url=os.environ.get("OLLAMA_BASE_URL")
        self.ollama_max_tokens=os.environ.get("OLLAMA_MAX_TOKNES")

        if self.provider == "OPENAI":
            openai.api_key = self.openai_api_key
        elif self.provider == "ANTHROPIC":
            self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        elif self.provider =="OLLAMA":
            openai.base_url=self.ollama_base_url
            openai.api_key = "EMPTY"
        else:
            raise ValueError("Unknown PROVIDER specified in the environment variables.")
        
    @staticmethod
    def list_directories(base_directory: str) -> str:
        """List all directories in the base directory as a CSV string."""
        try:
            directories = [name for name in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, name))]
            csv_string = ",".join(directories)
            logger.info(f"Listed directories in {base_directory}")
            return csv_string
        except Exception as e:
            logger.error(f"Error listing directories in {base_directory}: {e}")
            return ""

    def _call_openai_api(self, model: str, messages: list, response_format: BaseModel = None, temperature: float = 0.3,max_tokens: int = 1000):
        """
        Helper method to call the OpenAI API.
        """
        try:
            if response_format:
                return openai.beta.chat.completions.parse(
                    model=model,
                    messages=messages,
                    response_format=response_format,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            return openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return None

    def _call_claude_api(self, model: str, messages: list, response_format: BaseModel = None, temperature: float = 0.3,max_tokens: int = 1000 ) -> dict:
        """
        ClaudeのAPIを呼び出すヘルパーメソッド。指定されたPydanticモデルでのレスポンス形式をsystemメッセージに組み込みます。
        """
        try:
            # response_modelを用いたsystemメッセージの置換
            if response_format:
                model_example = response_format.schema_json(indent=2)
                existing_content = messages[0].get("content", "")
                systems= f"{existing_content}\nレスポンスは以下の形式に従ってください:\n{model_example}"
            else:
                systems = messages[0].get("content", "")
            if messages:
                del messages[0]

            response = self.client.messages.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                system=systems
            )

            return response
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            return None

    def _call_ollama_api(self, model: str, messages: list, response_format: BaseModel = None, temperature: float = 0.3,max_tokens=256):
        """
        Helper method to call the OpenAI API.
        """
        try:
            if response_format:
                model_example = response_format.schema_json(indent=2)
                existing_content = messages[0].get("content", "")
                messages[0]["content"] = f"{existing_content}\nレスポンスは以下の形式に従ってください:\n{model_example}"

            return openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            return None
        
    def _call_api(self, messages: list, response_format: type = None, max_tokens: int = 8192, temperature: float = 0.3):
        """
        Call the appropriate API based on the provider.
        """
        if self.provider == "OPENAI":
            return self._call_openai_api(self.model, messages, response_format, temperature,max_tokens)
        elif self.provider == "ANTHROPIC":
            return self._call_claude_api(self.model, messages, response_format,temperature,max_tokens )
        elif self.provider == "OLLAMA":
            return self._call_ollama_api(self.model, messages, response_format,temperature,max_tokens=self.ollama_max_tokens )
        
    def _reponse_api(self,completion: dict,response_format: str):
        result=""
        if self.provider == "OPENAI":
            if response_format=="json":
                result = completion.choices[0].message.parsed.json()
            elif response_format=="parsed":
                result = completion.choices[0].message.parsed
            else:
                result = completion.choices[0].message.content
        elif self.provider=="ANTHROPIC":
            result = completion.content[0].text
            if response_format=="parsed":
                result = json.loads(result)
        elif self.provider=="OLLAMA":
            result = completion.choices[0].message.content
            if response_format=="parsed":
                result = json.loads(result)

        return result
        
    def generate_filename(self, requirements: str, base_directory: str) -> str:
        """Generate a non-conflicting filename based on requirements."""
        try:
            existing_directories = self.list_directories(base_directory)
            user_input = (
                f"目的：下記の「要件定義書」をベースとしての中身を要約したフォルダ名を生成してください。\n"
                f"条件：- ファイル名は、英数字・半角記号・小文字であること。\n"
                f"      - 文字列長さは20文字以内であること\n"
                f"      - 出力時にはファイル名のみを出力すること。\n"
                f"      - {existing_directories}は、カンマ区切りで既に存在するフォルダ名が記載されている。\n"
                f"        被らないように生成すること。\n"
                f"要件定義書：\n{requirements}\n"
            )
            completion = self._call_api(
                messages=[
                    {"role": "system", "content": "あなたは誠実で優秀なPythonプログラマです"},
                    {"role": "user", "content": user_input}
                ],
                response_format=FileName
            )
            if completion:
                json_data=self._reponse_api(completion,"json")
                data = json.loads(json_data)
                filename = os.path.join(base_directory, data.get("filename", ""))
                logger.info(f"Generated filename: {filename}")
                return filename
            return ""
        except Exception as e:
            logger.error(f"Error generating filename: {e}")
            return ""

    def generate_requirement(self, system_name: str, requirements: str, feedback: str = "") -> str:
        """Generate a requirement document based on specifications."""
        try:
            requirements = requirements.replace("{作りたいアプリ}", system_name)
            user_input = (
                f"目的：「設計書」を生成してください。\n"
                f"条件：Markdown形式で出力して下さい。図形を作成する際は、mermaidを利用して下さい。\n"
                f"要件定義書：\n{requirements}\n"
                f"フィードバック：\n{feedback}\n"
            )
            completion = self._call_api(
                messages=[
                    {"role": "system", "content": "あなたは誠実で優秀な日本人のシステム設計者です。"},
                    {"role": "user", "content": user_input}
                ]
            )
            if completion:
                generated_require=self._reponse_api(completion,"")
                if generated_require.startswith("```markdown") and generated_require.endswith("```"):
                    generated_require = generated_require[11:-3].strip()
                logger.info("Generated requirement document")
                return generated_require
            return ""
        except Exception as e:
            logger.error(f"Error generating requirement document: {e}")
            return ""

    def generate_detail_design(self, system_name: str, requirements: str, detail_design: str) -> str:
        """Generate a detailed design document."""
        try:
            detail_design = detail_design.replace("{作りたいアプリ}", system_name)
            user_input = (
                f"目的:以下のテンプレートを使用して詳細設計を作成します。\n"
                f"      要件定義に適した内容で埋めてください。\n"
                f"条件:Markdown形式で出力して下さい。図形を作成する際は、mermaidを利用して下さい。\n"
                f"      要件定義書の技術要件に記載されているプログラミング言語やOSS・製品に従って設計して下さい。\n"
                f"出力:生成した詳細設計書のみ出力して下さい。\n"
                f"要件定義書：\n{requirements}\n"
                f"詳細設計書：\n{detail_design}\n"
            )
            completion =self._call_api(
                messages=[
                    {"role": "system", "content": "あなたは誠実で優秀な日本人のシステム設計者です。"},
                    {"role": "user", "content": user_input}
                ]
            )
            if completion:
                generated_design=self._reponse_api(completion,"")
                if generated_design.startswith("```markdown") and generated_design.endswith("```"):
                    generated_design = generated_design[11:-3].strip()
                logger.info("Generated detail design document")
                return generated_design
            return ""
        except Exception as e:
            logger.error(f"Error generating detail design document: {e}")
            return ""

    def generate_code(self, system_name: str, detail_design: str, code_template: str) -> str:
        """Generate code based on a detail design and template."""
        try:
            user_input = code_template.replace("{作りたいアプリ}", system_name)
            user_input = user_input.replace("{生成された詳細設計書}", detail_design)
            completion = self._call_api(
                temperature=0.1,
                messages=[
                    {"role": "system", "content": "あなたは誠実で優秀な日本人のプログラマです。"},
                    {"role": "user", "content": user_input}
                ],
                response_format=GeneratedCode
            )
            if completion:
                if self.provider == "OPENAI":
                    generated_codes = self._reponse_api(completion, "parsed")
                    generated_codes_json = generated_codes.json()
                elif self.provider == "ANTHROPIC":
                    generated_codes_json = self._reponse_api(completion, "")

                logger.info("Generated code")
                return generated_codes_json
            return ""
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return ""

    @staticmethod
    def parse_generated_code(json_data: str) -> list:
        """Parse the generated code from JSON."""
        try:
            data = json.loads(json_data)
            source_files = data.get("source_file", [])
            parsed_files = [
                {"filename": file.get("filename", "unknown_file"), "code": file.get("code", "")}
                for file in source_files if "requirements.md" not in file.get("filename", "")
            ]
            logger.info("Parsed generated code")
            return parsed_files
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return []
