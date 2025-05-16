# app.py
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Hiragino Sans'
from sqlalchemy import create_engine

# .envファイルの読み込み
load_dotenv()

# 環境変数から接続URLを取得
db_url = os.environ.get("DB_URL")

@st.cache_data
def load_data_from_postgres():
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM users;", engine)
    return df

st.title("統計解析アプリ")

data_source = st.sidebar.selectbox(
    "データの取得元を選んでください",
    ("CSVファイル", "PostgreSQL")
)

df = None  # 初期化
uploaded_file = None

# データの読み込み：CSV or PostgreSQL
if data_source == "CSVファイル":
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

elif data_source == "PostgreSQL":
    df = load_data_from_postgres()

if df is not None:

    # サイドバーで表示機能を選択
    st.sidebar.title("表示する内容を選択")
    show_preview = st.sidebar.checkbox("データのプレビュー", value=True)
    show_stats = st.sidebar.checkbox("基本統計量", value=True)
    show_missing = st.sidebar.checkbox("欠損値の確認", value=True)
    show_hist = st.sidebar.checkbox("ヒストグラム", value=True)
    show_corr = st.sidebar.checkbox("相関行列ヒートマップ", value=True)
    show_scatter = st.sidebar.checkbox("散布図", value=True)

    # それぞれの機能を条件に応じて表示
    if show_preview:
        st.subheader("データのプレビュー")
        st.write(df.head())

    if show_stats:
        st.subheader("基本統計量（日本語）")
        desc = df.describe().rename(index={
            'count': '件数',
            'mean': '平均',
            'std': '標準偏差',
            'min': '最小値',
            '25%': '第1四分位数',
            '50%': '中央値',
            '75%': '第3四分位数',
            'max': '最大値'
        })
        st.write(desc)

    if show_missing:
        st.subheader("欠損値の確認")
        st.write(df.isnull().sum())

    if show_hist:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            col = st.sidebar.selectbox("ヒストグラムのカラム選択", numeric_cols)
            if col:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(
                    df[col],
                    kde=True,
                    ax=ax,
                    color="#5DADE2",
                    edgecolor="white",
                    linewidth=1.5,
                    alpha=0.9
                )
                sns.kdeplot(
                    df[col],
                    ax=ax,
                    color="#2E86C1",
                    linewidth=2,
                )
                ax.set_ylabel("件数")
                ax.set_xlabel(col)
                ax.set_title(f"{col} のヒストグラム", fontsize=14, fontweight='bold')
                ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
                ax.set_facecolor("#fdfdfd")
                st.pyplot(fig)
        
    if show_corr:
        st.subheader("相関行列ヒートマップ")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="mako", fmt=".2f", square=True, ax=ax)
            ax.set_title("数値カラム間の相関係数")
            st.pyplot(fig)
        else:
            st.info("相関行列を表示するには数値カラムが2つ以上必要です。")

    if show_scatter:
        st.subheader("散布図")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) >= 2:
            x_col = st.sidebar.selectbox("X軸のカラム", numeric_cols, key="scatter_x")
            y_col = st.sidebar.selectbox("Y軸のカラム", numeric_cols, key="scatter_y")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax, color="#48C9B0", s=70, edgecolor="gray")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{x_col} vs {y_col} の散布図")
            ax.grid(True, linestyle="--", alpha=0.4)
            st.pyplot(fig)
        else:
            st.info("散布図を表示するには数値カラムが2つ以上必要です。")

    else:
        st.info("数値型のカラムがありません。")

