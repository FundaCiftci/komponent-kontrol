import streamlit as st
import pandas as pd

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("🔍 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if 'TemaTakipNo' in df.columns and 'KomponentId' in df.columns:
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['Renk'] = ''
        df.loc[df['KomponentId'] > 0, 'Renk'] = 'Sarı'

        st.success("Uygun sayfa bulundu ve yüklendi: {}".format(sheet_name))
        st.dataframe(df)

        ttn_input = st.text_input("TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = str(ttn_input).strip()
            if (df['TemaTakipNo'].astype(str) == ttn_input).any():
                mask = (df['TemaTakipNo'].astype(str) == ttn_input)
                if (df.loc[mask, 'KomponentId'] > 0).any():
                    df.loc[mask, 'Renk'] = 'Kırmızı'
                    st.warning("Komponent var 🚨")
                st.dataframe(df)
            else:
                st.error("Bu TemaTakipNo bulunamadı!")
    else:
        st.error("Hiçbir sayfada 'TemaTakipNo' ve 'KomponentId' sütunları birlikte bulunamadı.")
