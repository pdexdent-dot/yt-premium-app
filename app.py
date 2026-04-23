import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="YT Premium Manager", layout="wide")

# จำลองฐานข้อมูล (ในอนาคตเชื่อมกับ Google Sheets ได้ง่ายๆ)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame({
        'Name': ['Jutarut', 'Somchai', 'Mana', 'Piti'],
        'Status': ['ยังไม่ได้จ่าย', 'ยังไม่ได้จ่าย', 'จ่ายแล้ว', 'ยังไม่ได้จ่าย'],
        'Slip': [None, None, None, None]
    })

# --- UI SIDEBAR ---
st.sidebar.title("เมนูการใช้งาน")
app_mode = st.sidebar.selectbox("เลือกหน้าจอ", ["หน้าส่งสลิป (Member)", "Dashboard (Admin)"])

# --- MEMBER PAGE ---
if app_mode == "หน้าส่งสลิป (Member)":
    st.title("📺 ส่งสลิป YouTube Premium")
    
    with st.form("upload_form", clear_on_submit=True):
        name = st.selectbox("เลือกชื่อของคุณ", st.session_state.db['Name'])
        uploaded_file = st.file_uploader("แนบรูปสลิปการโอนเงิน", type=['png', 'jpg', 'jpeg'])
        submit = st.form_submit_button("ส่งหลักฐาน")
        
        if submit and uploaded_file:
            # อัปเดตสถานะในจำลองฐานข้อมูล
            idx = st.session_state.db.index[st.session_state.db['Name'] == name].tolist()[0]
            st.session_state.db.at[idx, 'Status'] = 'รอตรวจสอบ'
            st.session_state.db.at[idx, 'Slip'] = uploaded_file
            st.success("ส่งข้อมูลสำเร็จ! รอ Admin ตรวจสอบนะครับ")

# --- ADMIN PAGE ---
else:
    st.title("📊 Dashboard สำหรับ Admin")
    
    # สรุปภาพรวม
    col1, col2, col3 = st.columns(3)
    paid_count = len(st.session_state.db[st.session_state.db['Status'] == 'จ่ายแล้ว'])
    pending_count = len(st.session_state.db[st.session_state.db['Status'] == 'รอตรวจสอบ'])
    
    col1.metric("จ่ายแล้ว", f"{paid_count} คน")
    col2.metric("รอตรวจสอบ", f"{pending_count} คน")
    col3.metric("ค้างจ่าย", f"{len(st.session_state.db) - paid_count} คน")
    
    st.divider()
    
    # ตารางจัดการข้อมูล
    st.subheader("จัดการการอนุมัติ")
    for index, row in st.session_state.db.iterrows():
        cols = st.columns([2, 2, 2, 2])
        cols[0].write(row['Name'])
        
        # แสดง Badge สถานะ
        if row['Status'] == 'จ่ายแล้ว':
            cols[1].success(row['Status'])
        elif row['Status'] == 'รอตรวจสอบ':
            cols[1].warning(row['Status'])
        else:
            cols[1].error(row['Status'])
            
        # ปุ่มกดดูสลิปและอนุมัติ
        if row['Status'] == 'รอตรวจสอบ':
            if cols[2].button("ตรวจสลิป", key=f"v_{index}"):
                st.image(row['Slip'], caption=f"สลิปของ {row['Name']}", width=300)
            if cols[3].button("✅ อนุมัติ", key=f"a_{index}"):
                st.session_state.db.at[index, 'Status'] = 'จ่ายแล้ว'
                st.rerun()
