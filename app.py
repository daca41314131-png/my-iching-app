import streamlit as st
import re
import requests
import random
import pandas as pd

# --- 1. 多國語言字典設定 ---
LANGUAGES = {
    "繁體中文": {
        "title": "🔮 數字易經能量分析 (專業版)",
        "input_label": "請輸入欲分析的號碼 (手機或身分證)：",
        "score_label": "能量總評分",
        "lock_msg": "🔒 分析報告已鎖定",
        "unlock_benefit": "為了保護您的隱私與提供最精準的深度解析，請支付後查看：\n- 能量總評分 (吉凶鑑定)\n- 逐段數字磁場解析 (八星明細)\n- 專屬化解方案與對比報表",
        "pay_btn": "💳 支付 1 USD 解鎖完整報告",
        "paid_success": "✅ 付款成功！已為您解鎖完整分析報告",
        "detail_table": "📊 原始號碼磁場分佈表",
        "advice_title": "💡 深度解析建議",
        "solution_title": "🛠️ 專屬數位化解方案",
        "solution_msg": "系統已根據您號碼的長度與結構，演算出最佳對沖化解碼。",
        "remedy_code": "✨ 建議化解碼：",
        "remedy_score": "📈 化解碼預計能量分數：",
        "remedy_table": "📋 化解碼磁場解析報表",
        "footer": "免責聲明：本分析僅供娛樂參考，生活幸福仍需靠自身努力。",
        "col_section": "區段", "col_star": "星號", "col_score": "分數"
    },
    "English": {
        "title": "🔮 Digital I-Ching Analysis (Pro)",
        "input_label": "Enter the number to analyze (Phone or ID):",
        "score_label": "Total Energy Score",
        "lock_msg": "🔒 Analysis Report Locked",
        "unlock_benefit": "To provide the most accurate deep analysis, please pay to view:\n- Total Energy Score (Lucky/Unlucky)\n- Segmented energy analysis (8 Stars details)\n- Customized remedy report and comparison",
        "pay_btn": "💳 Pay 1 USD to Unlock Full Report",
        "paid_success": "✅ Payment Successful! Full report unlocked.",
        "detail_table": "📊 Original Number Energy Distribution",
        "advice_title": "💡 Deep Insight & Advice",
        "solution_title": "🛠️ Customized Remedy Solution",
        "solution_msg": "We have calculated the optimal remedy code based on your number structure.",
        "remedy_code": "✨ Suggested Remedy Code:",
        "remedy_score": "📈 Estimated Remedy Score:",
        "remedy_table": "📋 Remedy Code Analysis Report",
        "footer": "Disclaimer: This analysis is for entertainment only.",
        "col_section": "Section", "col_star": "Star", "col_score": "Score"
    }
}

# --- 2. 核心邏輯類別 ---
class DigitalIChingPro:
    def __init__(self):
        self.star_config = {
            "天醫(財運/Wealth)": {"pairs": ["13", "31", "68", "86", "49", "94", "27", "72"], "score": 20},
            "生氣(貴人/Noble)": {"pairs": ["14", "41", "67", "76", "39", "93", "28", "82"], "score": 15},
            "延年(事業/Carrer)": {"pairs": ["19", "91", "78", "87", "34", "43", "26", "62"], "score": 15},
            "伏位(平穩/Stable)": {"pairs": ["11", "22", "33", "44", "66", "77", "88", "99"], "score": 10},
            "絕命(凶/Risky)": {"pairs": ["12", "21", "69", "96", "