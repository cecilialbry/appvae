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
import streamlit as st
import datetime
import json
import os

# Fichiers JSON pour stocker les données
PLATS_FILE = "plats.json"
MENUS_FILE = "menus_self.json"

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

plats = load_json(PLATS_FILE)
menus_self = load_json(MENUS_FILE)

st.title("Calendrier des plats et menus")

# Choix du mois et de l'année
col1, col2 = st.columns(2)
with col1:
    mois = st.number_input("Mois", min_value=1, max_value=12, value=datetime.date.today().month)
with col2:
    annee = st.number_input("Année", min_value=2000, max_value=2100, value=datetime.date.today().year)

# Création du calendrier
start_date = datetime.date(annee, mois, 1)
nb_jours = (datetime.date(annee + (mois // 12), ((mois % 12) + 1), 1) - start_date).days
jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

st.write(f"### {start_date.strftime('%B %Y')}")

# Afficher les jours de la semaine
cols = st.columns(7)
for idx, jour in enumerate(jours_semaine):
    cols[idx].markdown(f"**{jour}**")

first_weekday = (start_date.weekday() + 1) % 7  # Lundi = 0
current_col = 0

# Ajouter des cases vides pour le premier jour
cols = st.columns(7)
for _ in range(first_weekday):
    cols[current_col].write("")
    current_col += 1

# Affichage des jours avec plats et menus
for day in range(1, nb_jours + 1):
    if current_col >= 7:
        cols = st.columns(7)
        current_col = 0

    date_str = f"{annee}-{mois:02d}-{day:02d}"
    plats_jour = [p for p in plats if p["date"] == date_str]
    menus_jour = [m for m in menus_self if m["date"] == date_str]

    with st.container():
        cols[current_col].markdown(f"**{day}**")

        # Plats cliquables
        for idx, p in enumerate(plats_jour):
            if cols[current_col].button(p["nom"], key=f"{date_str}_plat_{idx}"):
                with st.modal(f"Plat : {p['nom']}"):
                    nom = st.text_input("Nom", value=p['nom'])
                    prix = st.number_input("Prix (€)", value=p['prix'])
                    parts = st.number_input("Parts", value=p['parts'], step=1)
                    desc = st.text_area("Description", value=p['description'])
                    image = st.text_input("Image URL", value=p['image'])
                    prof = st.text_input("Professeur", value=p['prof'])

                    if st.button("Enregistrer modifications", key=f"modif_{date_str}_{idx}"):
                        p.update({
                            "nom": nom,
                            "prix": prix,
                            "parts": parts,
                            "description": desc,
                            "image": image,
                            "prof": prof
                        })
                        save_json(PLATS_FILE, plats)
                        st.success("Plat modifié !")
                        st.experimental_rerun()

                    if st.button("Supprimer ce plat", key=f"supprimer_{date_str}_{idx}"):
                        plats.remove(p)
                        save_json(PLATS_FILE, plats)
                        st.success("Plat supprimé !")
                        st.experimental_rerun()

        # Menus cliquables
        for idx, m in enumerate(menus_jour):
            if cols[current_col].button(m["plat"], key=f"{date_str}_menu_{idx}"):
                with st.modal(f"Menu Self : {m['plat']}"):
                    entree = st.text_input("Entrée", value=m['entree'])
                    image_entree = st.text_input("Image entrée", value=m.get("imageEntree", ""))
                    plat_name = st.text_input("Plat", value=m['plat'])
                    image_plat = st.text_input("Image plat", value=m.get("imagePlat", ""))
                    dessert = st.text_input("Dessert", value=m['dessert'])
                    image_dessert = st.text_input("Image dessert", value=m.get("imageDessert", ""))
                    chef = st.text_input("Chef", value=m['chef'])

                    if st.button("Enregistrer modifications", key=f"modif_self_{date_str}_{idx}"):
                        m.update({
                            "entree": entree,
                            "imageEntree": image_entree,
                            "plat": plat_name,
                            "imagePlat": image_plat,
                            "dessert": dessert,
                            "imageDessert": image_dessert,
                            "chef": chef
                        })
                        save_json(MENUS_FILE, menus_self)
                        st.success("Menu modifié !")
                        st.experimental_rerun()

                    if st.button("Supprimer ce menu", key=f"supprimer_self_{date_str}_{idx}"):
                        menus_self.remove(m)
                        save_json(MENUS_FILE, menus_self)
                        st.success("Menu supprimé !")
                        st.experimental_rerun()

    current_col += 1
