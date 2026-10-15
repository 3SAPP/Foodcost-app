import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Foodcost Calculator", layout="wide", initial_sidebar_state="expanded")

st.title("🍽️ Foodcost Berekening App")
st.write("Bereken de kostprijs van je gerecht op basis van je ingrediënten.")

# Onthoud de ingrediënten zolang de app open staat
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []

# Zijbalk voor het invoeren van ingrediënten
st.sidebar.header("➕ Ingrediënt Toevoegen")

with st.sidebar.form(key='ingredient_form', clear_on_submit=True):
    leverancier = st.text_input("Leverancier (Vak A)")
    product = st.text_input("Productomschrijving (Vak B)")
    aantal_pers = st.number_input("Aantal personen (Vak D)", min_value=1, value=1)
    st_unit = st.number_input("Inhoud van product / St/unit (Vak E)", min_value=0.001, value=1.000, step=0.001, format="%.3f")
    st_pers = st.number_input("Nodig per persoon / st/pers (Vak F)", min_value=0.000, value=1.000, step=0.001, format="%.3f")
    prijs = st.number_input("Prijs van het product (Vak G)", min_value=0.00, value=0.00, step=0.01, format="%.2f")
    
    # De gecorrigeerde knop-functie
    submit_button = st.form_submit_button(label='Voeg toe aan recept')

# Logica wanneer er op de knop geklikt wordt
if submit_button and product:
    # Berekeningen gebaseerd op jouw exacte Excel-formules
    bestel_qt = (aantal_pers / st_unit) * st_pers if st_unit > 0 else 0
    totaalprijs = bestel_qt * prijs
    stukprijs_per_pers = (prijs / st_unit) * st_pers if st_unit > 0 else 0
    
    # Gegevens opslaan in een lijst
    new_ingredient = {
        "Leverancier": leverancier,
        "Product": product,
        "Bestel qt": round(bestel_qt, 4),
        "Aantal pers": aantal_pers,
        "St/unit": st_unit,
        "st/pers": st_pers,
        "Prijs": round(prijs, 2),
        "Totaal": round(totaalprijs, 2),
        "Stukprijs p.p.": round(stukprijs_per_pers, 4)
    }
    st.session_state.ingredients.append(new_ingredient)
    st.success(f"'{product}' succesvol toegevoegd!")

# Recept overzicht en totalen tonen
if st.session_state.ingredients:
    df = pd.DataFrame(st.session_state.ingredients)
    
    # Eindberekening: Tel alle stukprijzen op en doe maal 4.3
    som_stukprijzen = df["Stukprijs p.p."].sum()
    totale_kostprijs = som_stukprijzen * 4.3
    
    # Dashboard kaarten bovenaan tonen
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Som Stukprijzen p.p.", value=f"€ {som_stukprijzen:.4f}")
    with col2:
        st.metric(label="Totale Kostprijs Gerecht (Som x 4.3)", value=f"€ {totale_kostprijs:.2f}")
        
    st.subheader("📋 Recept Overzicht")
    st.dataframe(df, use_container_width=True)
    
    # Knop om de lijst leeg te maken
    if st.button("🧹 Hele recept wissen"):
        st.session_state.ingredients = []
        st.rerun()
else:
    st.info("Voeg ingrediënten toe via het linkerpaneel om de berekening te starten.")
