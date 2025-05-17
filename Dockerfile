# 1. Pythonベースの軽量イメージ
FROM python:3.10-slim

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. 必要なファイルをコピー
COPY requirements.txt ./
COPY app.py ./

# 4. Pythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt
#フォントをインストール
RUN apt-get update && apt-get install -y fonts-noto-cjk

# 5. Streamlitが使うポートを開ける
EXPOSE 8501

# 6. アプリを実行するコマンド
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]