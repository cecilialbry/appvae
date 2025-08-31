import streamlit as st
import json
import os
from datetime import date, datetime
import calendar

# -----------------------------------------------
# Fichiers JSON pour persistance
PLATS_FILE = "plats.json"
COMMANDES_FILE = "commandes.json"
MENUS_FILE = "menus_self.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -----------------------------------------------
# Initialisation session
if "mode" not in st.session_state:
    st.session_state.mode = "self"

# -----------------------------------------------
# Fonctions utilitaires
def ajouter_plat(plat):
    plats = load_json(PLATS_FILE)
    plats.append(plat)
    save_json(PLATS_FILE, plats)

def ajouter_menu_self(menu):
    menus = load_json(MENUS_FILE)
    menus.append(menu)
    save_json(MENUS_FILE, menus)

def supprimer_plat(nom, date_str):
    plats = load_json(PLATS_FILE)
    plats = [p for p in plats if not (p["nom"] == nom and p["date"] == date_str)]
    save_json(PLATS_FILE, plats)
    # Supprimer commandes liées
    commandes = load_json(COMMANDES_FILE)
    commandes = [c for c in commandes if not (c["plat"] == nom and c["date"] == date_str)]
    save_json(COMMANDES_FILE, commandes)

def supprimer_menu_self(date_str):
    menus = load_json(MENUS_FILE)
    menus = [m for m in menus if m["date"] != date_str]
    save_json(MENUS_FILE, menus)

# -----------------------------------------------
st.title("Gestion des ventes à emporter & Self pédagogique")

# Choix du mode
mode = st.radio("Mode actuel :", ["Self pédagogique", "Vente à emporter"])
st.session_state.mode = "self" if mode=="Self pédagogique" else "vae"

st.markdown("---")
# -----------------------------------------------
# Formulaire ajout plat à emporter
if st.session_state.mode == "vae":
    st.header("Ajouter un plat à emporter")
    with st.form("form_vae"):
        date_str = st.date_input("Date", value=date.today())
        nom = st.text_input("Nom du plat")
        prix = st.number_input("Prix (€)", min_value=0.0, step=0.01)
        parts = st.number_input("Nombre de parts", min_value=1, step=1)
        image = st.text_input("Image (URL)")
        description = st.text_input("Description")
        prof = st.text_input("Professeur responsable")
        submitted = st.form_submit_button("Ajouter le plat")
        if submitted:
            plat = {
                "date": date_str.isoformat(),
                "type": "vae",
                "nom": nom,
                "prix": prix,
                "parts": parts,
                "image": image,
                "description": description,
                "prof": prof
            }
            ajouter_plat(plat)
            st.success(f"Plat {nom} ajouté !")

# Formulaire ajout menu self
else:
    st.header("Ajouter un menu Self pédagogique")
    with st.form("form_self"):
        date_self = st.date_input("Date", value=date.today())
        entree = st.text_input("Entrée")
        image_entree = st.text_input("Image Entrée (URL)")
        plat_menu = st.text_input("Plat")
        image_plat = st.text_input("Image Plat (URL)")
        dessert = st.text_input("Dessert")
        image_dessert = st.text_input("Image Dessert (URL)")
        chef = st.text_input("Chef responsable")
        submitted = st.form_submit_button("Ajouter le menu")
        if submitted:
            menu = {
                "date": date_self.isoformat(),
                "entree": entree,
                "imageEntree": image_entree,
                "plat": plat_menu,
                "imagePlat": image_plat,
                "dessert": dessert,
                "imageDessert": image_dessert,
                "chef": chef
            }
            ajouter_menu_self(menu)
            st.success(f"Menu du {date_self} ajouté !")

st.markdown("---")

import streamlit as st
import json, os
from datetime import date, datetime
import calendar

# ---------- Fonctions JSON ----------
def load_json(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

PLATS_FILE = "plats.json"
MENUS_FILE = "menus_self.json"

import streamlit as st
import json, os
from datetime import date, datetime
import calendar

# ---------- Fonctions JSON ----------
def load_json(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

PLATS_FILE = "plats.json"
MENUS_FILE = "menus_self.json"

plats = load_json(PLATS_FILE)
menus = load_json(MENUS_FILE)

# ---------- Calendrier ----------
st.title("Calendrier interactif des plats & menus")

# Mois et année
today = date.today()
month_idx = st.selectbox("Mois", list(range(1, 13)), index=today.month-1)
year = st.number_input("Année", 2000, 2100, today.year)

# Premier jour et nombre de jours
first_weekday, nb_days = calendar.monthrange(year, month_idx)
decalage = (first_weekday + 6) % 7  # Décalage pour que lundi=0

# Construction du calendrier
st.write("Lun | Mar | Mer | Jeu | Ven | Sam | Dim")
st.markdown("---")

days_grid = [""]*decalage + list(range(1, nb_days+1))
for i in range(0, len(days_grid), 7):
    week = days_grid[i:i+7]
    cols = st.columns(7)
    for col, day in zip(cols, week):
        with col:
            if day != "":
                date_str = f"{year}-{month_idx:02d}-{day:02d}"
                # Bouton pour le jour
                if st.button(f"{day}", key=date_str):
                    st.session_state["selected_day"] = date_str

# Affichage des plats et menus pour le jour sélectionné
if "selected_day" in st.session_state:
    date_sel = st.session_state["selected_day"]
    st.markdown(f"## Plats et menus du {date_sel}")
    
    plats_jour = [p for p in plats if p["date"] == date_sel]
    menus_jour = [m for m in menus if m["date"] == date_sel]
    
    for p in plats_jour:
        st.write(f"**{p['nom']}** ({p['type']}) - {p['prix']}€ - Parts: {p['parts']}")
        if p.get("image"): st.image(p["image"], width=100)
    
    for m in menus_jour:
        st.write(f"🍽️ **{m['plat']}** | Entrée: {m['entree']} | Dessert: {m['dessert']} | Chef: {m['chef']}")
        if m.get("imageEntree"): st.image(m["imageEntree"], width=50)
        if m.get("imagePlat"): st.image(m["imagePlat"], width=50)
        if m.get("imageDessert"): st.image(m["imageDessert"], width=50)

# -----------------------------------------------
# Liste des plats existants avec suppression
st.markdown("---")
st.subheader("Plats existants")
plats = load_json(PLATS_FILE)
for p in plats:
    col1, col2 = st.columns([4,1])
    with col1:
        st.write(f"{p['date']} - {p['nom']} ({p['type']})")
    with col2:
        if st.button(f"Supprimer {p['nom']}", key=f"del_{p['nom']}_{p['date']}"):
            supprimer_plat(p['nom'], p['date'])
            st.experimental_rerun()

# Liste menus self existants
st.subheader("Menus self existants")
menus = load_json(MENUS_FILE)
for m in menus:
    col1, col2 = st.columns([4,1])
    with col1:
        st.write(f"{m['date']} - {m['plat']} ({m['entree']}/{m['dessert']})")
    with col2:
        if st.button(f"Supprimer {m['plat']}", key=f"del_menu_{m['plat']}_{m['date']}"):
            supprimer_menu_self(m['date'])
            st.experimental_rerun()
