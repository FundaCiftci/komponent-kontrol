
import streamlit as st
import pandas as pd
import random
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def speak_text(text):
    unique = random.randint(0, 999999)
    st.components.v1.html(f'''
        <script>
        var msg = new SpeechSynthesisUtterance("{text} {unique}");
        msg.text = "{text}";
        window.speechSynthesis.speak(msg);
        </script>
    ''', height=0)

# Ayakkabı ve istisna listelerini burada kısa tuttuk, uygulamada tam halini kullan
ayakkabi_modelleri = ["Shoes", "Slippers", "Boots"]
istisnalar = ["Toy", "Umbrella", "Notebook"]

st.set_page_config(page_title="Komponent Kontrol", layout="wide")
st.title("👟 Komponent Kontrol Uygulaması")

uploaded_file = st.file_uploader("📁 Excel dosyanı yükle (.xlsx)", type=["xlsx"])

if "kontroller" not in st.session_state:
    st.session_state.kontroller = []

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, dtype=str)
    selected_df = None

    for sheet_name, df in all_sheets.items():
        if all(k in df.columns for k in ['TemaTakipNo', 'KomponentId', 'ModelTanim']):
            selected_df = df.copy()
            break

    if selected_df is not None:
        df = selected_df
        df['KomponentId'] = pd.to_numeric(df['KomponentId'], errors='coerce')
        df['Renk'] = ''

        df.loc[(df['KomponentId'] > 0) & (~df['ModelTanim'].isin(istisnalar)), 'Renk'] = 'Sarı'
        df.loc[df['ModelTanim'].isin(ayakkabi_modelleri), 'Renk'] = 'Sarı'

        ttn_input = st.text_input("🎯 TemaTakipNo gir (sadece numara):")

        if ttn_input:
            ttn_input = ttn_input.strip()
            mask = df['TemaTakipNo'] == ttn_input

            if mask.any():
                kontrol_var = (
                    ((df.loc[mask, 'KomponentId'] > 0) & (~df.loc[mask, 'ModelTanim'].isin(istisnalar))).any()
                    or (df.loc[mask, 'ModelTanim'].isin(ayakkabi_modelleri)).any()
                )
                if kontrol_var:
                    speak_text("Kontrol et")
                    df.loc[mask & (df['Renk'] == 'Sarı'), 'Renk'] = 'Kırmızı'
                    st.session_state.kontroller.append(ttn_input)
            else:
                st.error("Bu TemaTakipNo bulunamadı!")

        # JSON hatası önleyici temizlik
        df = df.replace({pd.NA: '', None: '', float('inf'): '', float('-inf'): ''})
        df = df.fillna('')

        renk_kodu = JsCode("""
        function(params) {
            if (params.data.Renk === 'Kırmızı') {
                return {'backgroundColor': '#ff4d4d', 'color': 'white'};
            } else if (params.data.Renk === 'Sarı') {
                return {'backgroundColor': '#fff176'};
            }
        }
        """)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("Renk", cellStyle=renk_kodu)
        gb.configure_pagination()
        grid_options = gb.build()

        st.markdown("### 📋 Tüm Liste (Renkli Takip)")
        AgGrid(df, gridOptions=grid_options, height=600, theme="streamlit")
    else:
        st.error("TemaTakipNo, KomponentId ve ModelTanim sütunları eksik.")
