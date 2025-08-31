import streamlit as st
import datetime
import json
import os

# Fichiers JSON pour stocker les données
PLATS_FILE = "plats.json"
MENUS_FILE = "menus_self.json"

# Fonctions pour sauvegarder et charger les données
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

# Créer un calendrier simple
start_date = datetime.date(annee, mois, 1)
_, nb_jours = divmod((datetime.date(annee + (mois // 12), ((mois % 12) + 1), 1) - start_date).days, 1)
jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

st.write(f"### {start_date.strftime('%B %Y')}")

# Afficher les jours de la semaine
cols = st.columns(7)
for idx, jour in enumerate(jours_semaine):
    cols[idx].markdown(f"**{jour}**")

# Affichage des jours et des plats/menus
first_weekday = (start_date.weekday() + 1) % 7  # Lundi = 0
cols = st.columns(7)
for _ in range(first_weekday):
    st.write("")

for day in range(1, nb_jours + 1):
    date_str = f"{annee}-{mois:02d}-{day:02d}"
    plats_jour = [p for p in plats if p["date"] == date_str]
    menus_jour = [m for m in menus_self if m["date"] == date_str]

    st.markdown(f"### {day} {start_date.strftime('%B')}")

    # Plats
    for idx, p in enumerate(plats_jour):
        with st.expander(f"Plat : {p['nom']}"):
            st.text_input("Nom", value=p['nom'], key=f"nom_{date_str}_{idx}")
            st.number_input("Prix (€)", value=p['prix'], key=f"prix_{date_str}_{idx}")
            st.number_input("Parts", value=p['parts'], step=1, key=f"parts_{date_str}_{idx}")
            st.text_area("Description", value=p['description'], key=f"desc_{date_str}_{idx}")
            st.text_input("Image URL", value=p['image'], key=f"img_{date_str}_{idx}")
            st.text_input("Professeur", value=p['prof'], key=f"prof_{date_str}_{idx}")

            if st.button("Enregistrer modifications", key=f"modif_{date_str}_{idx}"):
                p['nom'] = st.session_state[f"nom_{date_str}_{idx}"]
                p['prix'] = st.session_state[f"prix_{date_str}_{idx}"]
                p['parts'] = st.session_state[f"parts_{date_str}_{idx}"]
                p['description'] = st.session_state[f"desc_{date_str}_{idx}"]
                p['image'] = st.session_state[f"img_{date_str}_{idx}"]
                p['prof'] = st.session_state[f"prof_{date_str}_{idx}"]
                save_json(PLATS_FILE, plats)
                st.success("Plat modifié !")
                st.experimental_rerun()

            if st.button("Supprimer ce plat", key=f"supprimer_{date_str}_{idx}"):
                plats.remove(p)
                save_json(PLATS_FILE, plats)
                st.success("Plat supprimé !")
                st.experimental_rerun()

    # Menus self
    for idx, m in enumerate(menus_jour):
        with st.expander(f"Menu Self : {m['plat']}"):
            st.text_input("Entrée", value=m['entree'], key=f"entree_{date_str}_{idx}")
            st.text_input("Image entrée", value=m.get('imageEntree',''), key=f"img_entree_{date_str}_{idx}")
            st.text_input("Plat", value=m['plat'], key=f"plat_{date_str}_{idx}")
            st.text_input("Image plat", value=m.get('imagePlat',''), key=f"img_plat_{date_str}_{idx}")
            st.text_input("Dessert", value=m['dessert'], key=f"dessert_{date_str}_{idx}")
            st.text_input("Image dessert", value=m.get('imageDessert',''), key=f"img_dessert_{date_str}_{idx}")
            st.text_input("Chef", value=m['chef'], key=f"chef_{date_str}_{idx}")

            if st.button("Enregistrer modifications", key=f"modif_self_{date_str}_{idx}"):
                m['entree'] = st.session_state[f"entree_{date_str}_{idx}"]
                m['imageEntree'] = st.session_state[f"img_entree_{date_str}_{idx}"]
                m['plat'] = st.session_state[f"plat_{date_str}_{idx}"]
                m['imagePlat'] = st.session_state[f"img_plat_{date_str}_{idx}"]
                m['dessert'] = st.session_state[f"dessert_{date_str}_{idx}"]
                m['imageDessert'] = st.session_state[f"img_dessert_{date_str}_{idx}"]
                m['chef'] = st.session_state[f"chef_{date_str}_{idx}"]
                save_json(MENUS_FILE, menus_self)
                st.success("Menu modifié !")
                st.experimental_rerun()

            if st.button("Supprimer ce menu", key=f"supprimer_self_{date_str}_{idx}"):
                menus_self.remove(m)
                save_json(MENUS_FILE, menus_self)
                st.success("Menu supprimé !")
                st.experimental_rerun()
