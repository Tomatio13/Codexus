## 詳細設計の作成
以下のテンプレートを使用して{作りたいアプリ}の詳細設計書を作成します。
以下のコマンドスタックに従って進めてください。

# {作りたいアプリ}の詳細設計

## システムアーキテクチャ
- クライアントサーバーモデルの詳細
- フロントエンド（Webアプリ、モバイルアプリ）の構成
- バックエンドサーバーの構成
- マイクロサービスアーキテクチャ（該当する場合）
- アーキテクチャ図

## データベース設計
- エンティティ関係図（ER図）
- 主要エンティティのリスト
- 各エンティティの属性と関係性
- 主要テーブルの詳細設計
- DDL

## APIエンドポイント
- FastAPIを利用する場合に限り、FastAPIで実装するAPIエンドポイントを列挙
- 各エンドポイントのHTTPメソッド、パス、説明を記載
- ただし、必要がない場合は設計する必要はない。

## データモデル
- FastAPIで使用するデータモデル(SQLAlchemyモデル)を定義
- 各モデルの属性、リレーションシップを記述

## ファイル・フォルダ構成
- Markdown形式で省略なしのファイル・フォルダ構成を記述してください。ファイル名の後ろにファイルの概要を出力して下さい。
- 要件定義書に記載されている技術要件のOSSや製品に最適なディレクトリ構成を作成して下さい。
- docker-compose.ymlを作成して下さい。
- Dockerfileを作成して下さい。
- StreamlitとFastAPIを利用する場合に限り、フロントエンド(Streamlit)とバックエンド(FastAPI)のディレクトリ構成を分けて記述して下さい
- Streamlitを利用する場合に限り、Streamlitアプリケーションのディレクトリ構成のテンプレートです。
    ├── app.py: 全体を統合するpythonファイル
    ├── utils.py: 
    ├── templates/
    │   ├── header.py
    │   ├── sidebar.py
    │   └── footer.py
    ├── data/
    │   └── sample_data.csv
    ├── Dockerfile
    └── requirements.txt
- FastAPIを利用する場合に限り、FastAPIアプリケーションのディレクトリ構成のテンプレートです。
  ├── main.py
  ├── database.py
  ├── models/
  │    ├── models.py
  ├── Dockerfile
  └── requirements.txt
- Next.jsなどでnpmを必要とする場合、yarnコマンドではなく、npmコマンドを利用して下さい。
  また、その際はpackage-lock.jsonファイルを出力して下さい。
  また、shadcn/uiを利用できそうなら優先して利用して下さい。

## コンポーネント
    - Streamlitを利用する場合に限り、アプリケーションを構成する主要なStreamlitコンポーネントを列挙
    - 各コンポーネントの役割、入力と出力を記述してください

## データの流れ
    - ユーザー入力からデータ処理、結果表示までのデータの流れを説明
    - 必要に応じてデータフローダイアグラムを作成

## ユーザーインターフェース
    - アプリケーションの画面遷移図を作成
    - 各画面のワイヤーフレームまたはモックアップを用意
    - ユーザーインタラクションとイベントハンドリングについて説明

## 開発環境
    - 使用するOSSのバージョン
    - 必要なライブラリとそのバージョン
    - Pythonを利用する場合は、venv仮想環境を構築方法

## 実行方法
    - コンパイルが必要な場合はコンパイル方法を説明
    - Dockerを利用する場合は、ビルド方法やコンパイル方法を説明

## テスト
    - ユニットテストの方針を決定
    - 主要な機能についてテストケースを作成
    - テストデータの準備方法を説明

このプロンプトに従って、{作りたいアプリ}の要件定義、詳細設計、および各種図式を作成してください。
