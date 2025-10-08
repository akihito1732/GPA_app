# gpa_app.py

import streamlit as st
import pandas as pd

st.title("GPA計算します！")

st.write("""
このアプリでは、CSVファイルをアップロードしてGPAを計算できます。  
※成績ルール: S=4, A=3, B=2, C=1, 不可=0, 放棄=0, 保留=0  
※「合格」はGPA計算に含まれません
""")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルを選択してください", type="csv")

if uploaded_file is not None:
    # CSVを読み込む
    df = pd.read_csv(uploaded_file)

    # 「合格」を除外
    df_gpa = df[df["評価"] != "合"].copy()

    # 「評価」が空白・NaNの行を除外
    df_gpa = df_gpa[df_gpa["評価"].notna() & (df["評価"].str.strip() != "")]

    # 評価文字列を整形
    df_gpa["評価"] = df_gpa["評価"].astype(str).str.strip().str.upper()

    # 成績と点数の対応表
    grade_points = {"Ｓ":4, "Ａ":3, "Ｂ":2, "Ｃ":1, "不可":0, "放棄":0, "保留":0}

    # 成績を点数に変換
    df_gpa["点数"] = df_gpa["評価"].map(grade_points)

    # GPA計算
    total_points = (df_gpa["点数"] * df_gpa["単位数"]).sum()
    total_credits = df_gpa["単位数"].sum()

    if total_credits == 0:
        st.warning("GPAを計算できる科目がありません。")
    else:
        gpa = total_points / total_credits
        st.success(f"あなたのGPAは：{gpa:.2f}")
        st.write("📄 詳細データ:")
        st.dataframe(df_gpa)
