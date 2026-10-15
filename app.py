import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Foodcost Calculator", layout="wide")

st.title("🍽️ Foodcost Berekening App (1-op-1 Excel)")
st.write("Vul de gegevens in exact zoals in je Excel-kolommen.")

# Sessie-state voor het bijhouden van de producten in de tabel
if 'recept_lijnen' not in st.session_state:
    st.session_state.recept_lijnen = []

# Formulier aan de linkerkant voor invoer
st.sidebar.header("📥 Product Invoeren")

with st.sidebar.form(key='excel_form', clear_on_submit=True):
    vak_a = st.text_input("Leverancier (Vak A)")
    vak_b = st.text_input("Productomschrijving (Vak B)")
    
    # Aantal personen mag ook 0 of leeg zijn (zoals in jouw kerstomaatjes voorbeeld)
    vak_d = st.number_input("Aantal pers (Vak D)", min_value=0, value=0, step=1)
    
    vak_e = st.number_input("Inhoud van product / St/unit (Vak E)", min_value=0.0001, value=1.0000, step=0.0001, format="%.4f")
    vak_f = st.number_input("Aantal nodig voor één persoon / st/pers (Vak F)", min_value=0.0000, value=1.0000, step=0.0001, format="%.4f")
    vak_g = st.number_input("Prijs van het product op basis van inhoud (Vak G)", min_value=0.00, value=0.00, step=0.01, format="%.2f")
    
    submit_button = st.form_submit_button(label='Voeg lijn toe')

# Als er op de knop gedrukt wordt en er is een product ingevuld
if submit_button and vak_b:
    # EXACTE EXCEL FORMULES:
    # vak c = vak d / vak e * vak f
    vak_c = (vak_d / vak_e) * vak_f if vak_e > 0 else 0
    
    # vak h = vak c * vak g
    vak_h = vak_c * vak_g
    
    # vak i = vak g / vak e * vak f
    vak_i = (vak_g / vak_e) * vak_f if vak_e > 0 else 0
    
    # Opslaan in de lijst
    nieuwe_lijn = {
        "Leverancier (Vak A)": vak_a,
        "Product (Vak B)": vak_b,
        "Bestel qt (Vak C)": round(vak_c, 4),
        "Aantal pers (Vak D)": vak_d,
        "St/unit (Vak E)": vak_e,
        "st/pers (Vak F)": vak_f,
        "Prijs (Vak G)": round(vak_g, 2),
        "Totaal (Vak H)": round(vak_h, 2),
        "Stukprijs (Vak I)": round(vak_i, 6)
    }
    st.session_state.recept_lijnen.append(nieuwe_lijn)
    st.success(f"'{vak_b}' succesvol toegevoegd!")

# Het tonen van het overzicht en de totalen
if st.session_state.recept_lijnen:
    df = pd.DataFrame(st.session_state.recept_lijnen)
    
    # BEREKENING KOSTPRIJS GERECHT:
    # Alle lijnen waar iets ingegeven is: de stukprijs (Vak I) samentellen en vermenigvuldigen maal 4,3
    som_stukprijzen = df["Stukprijs (Vak I)"].sum()
    kostprijs_gerecht = som_stukprijzen * 4.3
    
    # Resultaat grote kaarten tonen
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Som van Stukprijzen (Vak I)", value=f"€ {som_stukprijzen:.4f}")
    with col2:
        st.metric(label="Kostprijs van het gerecht (Som x 4,3)", value=f"€ {kostprijs_gerecht:.2f}")
    
    st.subheader("📋 Actueel Recept")
    st.dataframe(df, use_container_width=True)
    
    # Wis knop
    if st.button("🧹 Recept volledig wissen"):
        st.session_state.recept_lijnen = []
        st.rerun()
else:
    st.info("Voeg producten toe via het linkerpaneel om de berekening live te zien.")
