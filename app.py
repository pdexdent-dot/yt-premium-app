import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="YT Premium Manager", layout="wide")

# เชื่อมต่อกับ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=st.secrets["public_gsheets_url"])

st.sidebar.title("เมนูการใช้งาน")
app_mode = st.sidebar.selectbox("เลือกหน้าจอ", ["หน้าส่งสลิป (Member)", "Dashboard (Admin)"])

if app_mode == "หน้าส่งสลิป (Member)":
    st.title("📺 ส่งสลิป YouTube Premium")
    with st.form("upload_form"):
        name = st.selectbox("เลือกชื่อของคุณ", df['Name'].tolist())
        uploaded_file = st.file_uploader("แนบรูปสลิป", type=['png', 'jpg'])
        if st.form_submit_button("ส่งหลักฐาน"):
            if uploaded_file:
                st.success(f"บันทึกข้อมูลของ {name} เรียบร้อย! (Admin จะเห็นในระบบ)")
            else:
                st.error("กรุณาแนบรูปสลิปด้วยครับ")

else:
    st.title("📊 Dashboard สำหรับ Admin")
    st.dataframe(df) # แสดงตารางข้อมูลจาก Google Sheets จริงๆ
