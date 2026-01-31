import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import load_apps_dataset
from src.utils import apply_custom_css
from src.test import fetch_playstore, fetch_youtube_api, fetch_youtube_no_api
from src.processor import get_sentiment

st.set_page_config(
    page_title="Dashboard",
    page_icon="https://cdn-icons-png.flaticon.com/128/11264/11264792.png",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'> Dashboard Analisis Sentimen Lanjutan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Analisis Sentimen Lanjutan secara real-time dari berbagai platform digital</p>", unsafe_allow_html=True)
st.divider()
APPS_LIST = load_apps_dataset()

st.sidebar.header("Pengaturan Sumber Data")
source = st.sidebar.selectbox("Pilih Platform", ["Google Play Store", "YouTube", "Demo YT (No API)"])

target_input = ""
yt_api_key = ""

if source == "Google Play Store":
    app_choice = st.sidebar.selectbox("Pilih Aplikasi", sorted(APPS_LIST.keys()))
    target_input = APPS_LIST[app_choice]
elif source == "YouTube":
    yt_api_key = st.sidebar.text_input("Masukkan YouTube API Key", type="password")
    target_input = st.sidebar.text_input("Masukkan Video ID", placeholder="Contoh: F9dwQP4sbKI")
else: 
    target_input = st.sidebar.text_input("Masukkan URL YouTube", placeholder="https://www.youtube.com/watch?v=...")

if st.sidebar.button("Mulai Analisis"):
    if not target_input:
        st.error("Input tidak boleh kosong!")
        st.stop()

    df = pd.DataFrame()
    
    with st.status(f"Sedang mengambil data dari {source}...", expanded=True) as status:
        st.write("Menghubungkan ke server...")
        if source == "Google Play Store":
            df = fetch_playstore(target_input)
        elif source == "YouTube":
            if not yt_api_key: 
                st.error("API Key dibutuhkan!"); st.stop()
            df = fetch_youtube_api(target_input, yt_api_key)
        else:
            df = fetch_youtube_no_api(target_input)
        
        if df is not None and not df.empty:
            st.write("Data berhasil diambil. Memulai proses...")
            sentiments = []
            for i, row in df.iterrows():
                sentiments.append(get_sentiment(row['Content']))
            df['Sentiment'] = sentiments
            status.update(label="Analisis Selesai!", state="complete", expanded=False)
        else:
            status.update(label="Gagal mengambil data.", state="error")
            st.error("Data tidak ditemukan atau limit tercapai. Silakan coba lagi nanti.")
            st.stop()

    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Visualisasi Sentimen")
        counts = df['Sentiment'].value_counts().reindex(['Negative', 'Neutral', 'Positive'], fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#ff4b4b', '#afb8c1', '#00c853']
        counts.plot(kind='bar', color=colors, ax=ax)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel("Jumlah")
        plt.xticks(rotation=0)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Statistik Ringkas")
        st.metric("Total Komentar/Review", len(df))
        st.write(counts)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Hasil Analisis (CSV)", csv, "sentiment.csv", "text/csv", use_container_width=True)

    st.divider()
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        <hr style='border: none; border-top: 1px solid #eee; margin-bottom: 20px;'>
        <p>
            © 2026 | Dashboard Analisis Sentimen | 
            Built with <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="20"> 
            | <a href="https://github.com/yanas-logs" target="_blank" style="color: #4b8bbe; text-decoration: none;">yanas-logs</a>
        </p>
        
    </div>
    """, 
    unsafe_allow_html=True
)