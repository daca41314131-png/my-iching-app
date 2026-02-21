import streamlit as st
import re
import random
import pandas as pd

# --- 1. 介面極致清理 ---
st.set_page_config(page_title="數位易經能量鑑定所", page_icon="🔮", layout="centered")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display:none !important;} [data-testid="stSidebarNav"] {display: none;}
    button[data-testid="stBaseButton-secondary"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. 深度大師文本與全球語系引擎 ---
# 這裡展示如何擴展至 108 國語言的結構
def get_content(lang_name):
    # 此字典可持續增加至 108 種語言
    db = {
        "繁體中文": {
            "title": "數位易經能量鑑定所",
            "opening": "「信士您好，觀您所測之號碼，其數位磁場如同宿命之迴響。」",
            "warning": "【核心磁場警告】：您原始號碼中的能量共振點目前正處於『能量斷層』。這種波長會導致財源如漏斗般流失，且容易在關鍵決策時產生干擾。",
            "remedy_intro": "【大師化解心法】：此組化解碼是根據易經八大星曜之『生氣』與『天醫』交互演算而成，能將您混亂的數位磁場重新校準至繁榮頻率。",
            "diet": "【靈性能量指引】：建議多食**深綠色蔬果**以強化貴人場，並避開辛辣物以保持靈台清明。",
            "usage": "【使用說明】：請將此碼設為手機解鎖密碼。每日清晨對著此數字冥想 3 分鐘，持續 21 天，即可見能量轉變。",
            "remedy_label": "✨ 建議開運化解碼：",
            "btn_text": "💳 支付 1 USD 解鎖大師報告",
            "cols": ["區段", "星號磁場", "能量分數"]
        },
        "English": {
            "title": "Digital I-Ching Energy Lab",
            "opening": "Greetings. Your number resonates with cosmic frequencies reflecting your destiny.",
            "warning": "[Energy Fault Alert]: The vibrations in your number are experiencing a 'Dynamic Fracture', draining your prosperity and focus.",
            "remedy_intro": "[The Art of Remedy]: This code uses 'Sheng-Qi' and 'Tian-Yi' stars to realign your digital field to abundance.",
            "diet": "[Spiritual Diet]: Consume more **dark green vegetables** to boost your 'Noble' energy field.",
            "usage": "[How to Use]: Set this code as your phone password and meditate on it for 3 minutes every morning for 21 days.",
            "remedy_label": "✨ Recommended Remedy Code:",
            "btn_text": "💳 Pay 1 USD to Unlock Analysis",
            "cols": ["Section", "Star Energy", "Score"]
        }
        # 可依此格式加入 日語、法語、德語等 108 種語系
    }
    return db.get(lang_name, db["English"])

# --- 3. 側邊欄控制 ---
selected_lang = st.sidebar.selectbox("🌐 Language / 語言", ["繁體中文", "English", "日本語", "Français", "Deutsch", "Español"])
L = get_content(selected_lang)

st.sidebar.divider()
st.sidebar.subheader("📝 鑑定資料填寫")
raw_input = st.sidebar.text_input("輸入號碼 (手機、身分證、生日、車牌)：")

# --- 4. 演算邏輯 ---
def analyze(nums):
    # 簡化展示八星演算邏輯
    pairs = [nums[i:i+2] for i in range(len(nums)-1)]
    return [{"p": p, "s": "感應中...", "v": random.randint(-20, 20)} for p in pairs]

# --- 5. 主畫面呈現與支付導向 ---
st.title("🔮 " + L["title"])

if raw_input:
    # 偵測支付成功參數 (由 PayPal 自動導向帶回)
    # 只要網址後方帶有 ?pay=success，網頁就會自動刷新顯示專業內容
    is_paid = st.query_params.get("pay") == "success"

    if is_paid:
        # --- 專業分析網頁 (支付後自動呈現) ---
        st.success("✅ 支付成功！大師已為您解開磁場封印。")
        st.markdown(f"### {L['opening']}")
        
        # 深度解說內容
        st.warning(L["warning"])
        st.markdown(f"#### {L['remedy_intro']}")
        
        # 開運化解碼
        remedy_code = "".join(random.choices("136849", k=8))
        st.info(f"{L['remedy_label']} **{remedy_code}** (預期能級：98.5)")
        
        # 生活指引
        st.write(L["diet"])
        st.write(L["usage"])
        
        # 詳細表格
        with st.expander("📊 查看詳細能量數據"):
            df = pd.DataFrame(analyze(raw_input))
            df.columns = L["cols"]
            st.table(df)
            
    else:
        # --- 原始等待網頁 (支付前) ---
        st.info(f"📍 鑑定標的：{raw_input}")
        st.write("鑑定數據已演算完畢。由於涉及天機，專業化解方案需解鎖後查閱。")
        
        # 支付按鈕：點擊後會開啟 PayPal 分頁，支付完會自動跳回此頁並帶入參數
        st.link_button(L["btn_text"], "https://www.paypal.com/ncp/payment/ZAN2GMGB4Y4JE")
        
        st.caption("命理分析僅供參考，心誠則靈。支付後網頁將自動載入大師報告。")
else:
    st.info("👈 請於左側選單輸入您的號碼，開始鑑定。")