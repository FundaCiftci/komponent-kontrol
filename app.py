
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("🔍 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'TemaTakipNo' in df.columns and 'KomponentId' in df.columns:
        # Sarı boyanacak satırları belirle
        df['Renk'] = ''
        df.loc[df['KomponentId'] > 0, 'Renk'] = 'Sarı'

        st.success("Dosya başarıyla yüklendi ve tarandı.")
        st.dataframe(df)

        ttn_input = st.text_input("TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = str(ttn_input).strip()
            if (df['TemaTakipNo'].astype(str) == ttn_input).any():
                # KomponentId > 0 olan eşleşmeler var mı kontrol et
                mask = (df['TemaTakipNo'].astype(str) == ttn_input)
                if (df.loc[mask, 'KomponentId'] > 0).any():
                    df.loc[mask, 'Renk'] = 'Kırmızı'
                    st.warning("Komponent var 🚨")
                st.dataframe(df)
            else:
                st.error("Bu TemaTakipNo bulunamadı!")
    else:
        st.error("Excel dosyanda 'TemaTakipNo' ve 'KomponentId' sütunları olmalı.")
