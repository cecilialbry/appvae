const weekdays = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'];
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

let mode = localStorage.getItem('mode') || 'self';

const events = JSON.parse(localStorage.getItem('plats') || '[]');



function setMode(newMode) {
  mode = newMode;
  localStorage.setItem('mode', mode);
  showCalendar();
}


function choisirMode(mode) {
  localStorage.setItem("mode", mode);
  document.getElementById("mode-actuel").innerText = "Mode actuel : " + (mode === "self" ? "Self pédagogique" : "Vente à emporter");
  console.log("Mode sélectionné :", mode);
}


function commander(date, plat, prix, idCommande) {
  const nom = prompt(`Commande pour le ${date}\nPlat : ${plat}\n\nEntre ton nom :`);
  if (!nom) return;

  const partsStr = prompt("Combien de parts souhaites-tu ?");
  const parts = parseInt(partsStr);
  if (isNaN(parts) || parts <= 0) {
    alert("Nombre invalide.");
    return;
  }

  const commande = {
    id: idCommande,
    date: date,
    type: localStorage.getItem("mode") || "self",
    plat: plat,
    prix: parseFloat(prix),
    nomClient: nom,
    quantite: parts
  };

  const commandesExistantes = JSON.parse(localStorage.getItem("commandes") || "[]");
  commandesExistantes.push(commande);
  localStorage.setItem("commandes", JSON.stringify(commandesExistantes));

  alert(`Commande enregistrée !\n${parts} part(s) de ${plat} pour ${nom}`);
}
function afficherPlats() {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const mode = localStorage.getItem("mode") || "self";
  const div = document.getElementById("liste-plats");
  div.innerHTML = "";

  const platsFiltres = plats.filter(p => p.type === mode);

  platsFiltres.forEach((plat, index) => {
    const bloc = document.createElement("div");
    bloc.style.border = "1px solid #ccc";
    bloc.style.padding = "10px";
    bloc.style.marginBottom = "10px";

    bloc.innerHTML = `
      <strong>${plat.date} — ${plat.nom}</strong><br>
      ${plat.prix} € — ${plat.parts} parts<br>
      <img src="${plat.image}" alt="${plat.nom}" style="height:50px;"><br><br>
      <button onclick="modifierPlat(${index})">Modifier</button>
      <button onclick="supprimerPlat(${index})">Supprimer</button>
    `;

    div.appendChild(bloc);
  });
}
function afficherCalendrierAdmin(mois, annee) {
  const calendrier = document.getElementById("calendrier-admin");
  calendrier.innerHTML = "";

  const joursSemaine = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];
  for (const jour of joursSemaine) {
    const cell = document.createElement("div");
    cell.className = "jour-semaine";
    cell.innerText = jour;
    calendrier.appendChild(cell);
  }

  const premierJour = new Date(annee, mois, 1).getDay();
  const nbJours = new Date(annee, mois + 1, 0).getDate();

  const decalage = premierJour === 0 ? 6 : premierJour - 1;
  for (let i = 0; i < decalage; i++) {
    const cell = document.createElement("div");
    cell.className = "jour-vide";
    calendrier.appendChild(cell);
  }

  const plats = JSON.parse(localStorage.getItem("plats") || "[]");

  for (let jour = 1; jour <= nbJours; jour++) {
    const cell = document.createElement("div");
    cell.className = "jour";
    const dateStr = `${annee}-${(mois + 1).toString().padStart(2, "0")}-${jour.toString().padStart(2, "0")}`;
    const divNum = document.createElement("div");
    divNum.className = "numero-jour";
    divNum.innerText = jour;
    cell.appendChild(divNum);

    const platsDuJour = plats.filter(p => p.date === dateStr);
    platsDuJour.forEach(plat => {
      const divPlat = document.createElement("div");
      divPlat.className = "plat-admin";
      divPlat.innerText = plat.nom;
      divPlat.onclick = () => ouvrirModaleAdmin(plat);
      cell.appendChild(divPlat);
    });

    calendrier.appendChild(cell);
  }
}

document.getElementById("mois-prec").addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  afficherCalendrierAdmin(currentMonth, currentYear);
});

document.getElementById("mois-suiv").addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  afficherCalendrierAdmin(currentMonth, currentYear);
});

function supprimerPlat(index) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const mode = localStorage.getItem("mode") || "self";

  const platsFiltres = plats.filter(p => p.type === mode);
  const platASupprimer = platsFiltres[index];

  const nouvelleListe = plats.filter(p => !(p.type === mode && p.date === platASupprimer.date && p.nom === platASupprimer.nom));
  localStorage.setItem("plats", JSON.stringify(nouvelleListe));
  alert("Plat supprimé !");
  afficherPlats();
}

function modifierPlat(index) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const mode = localStorage.getItem("mode") || "self";

  const platsFiltres = plats.filter(p => p.type === mode);
  const plat = platsFiltres[index];

  const nouveauPrix = prompt("Nouveau prix (€) :", plat.prix);
  const nouvellesParts = prompt("Nouveau nombre de parts :", plat.parts);

  if (nouveauPrix !== null && nouvellesParts !== null) {
    // mise à jour dans la liste originale
    const idx = plats.findIndex(p => p.type === mode && p.date === plat.date && p.nom === plat.nom);
    plats[idx].prix = parseFloat(nouveauPrix);
    plats[idx].parts = parseInt(nouvellesParts);
    localStorage.setItem("plats", JSON.stringify(plats));
    alert("Plat modifié !");
    afficherPlats();
  }
}
window.addEventListener("DOMContentLoaded", () => {
  const mode = localStorage.getItem("mode") || "self";
  localStorage.setItem("mode", mode);
  document.getElementById("mode-actuel").innerText =
    "Mode actuel : " + (mode === "self" ? "Self pédagogique" : "Vente à emporter");

  afficherPlats();
  afficherCalendrierAdmin(currentMonth, currentYear);
});

function getPlatById(platId) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  return plats.find(p => `${p.date}-${p.nom}`.replace(/\s/g, '_') === platId);
}

function modifierPlatDepuisJour(platId) {
  const plat = getPlatById(platId);
  if (!plat) return;

  const nouveauPrix = prompt("Nouveau prix (€) :", plat.prix);
  const nouvellesParts = prompt("Nouveau nombre de parts :", plat.parts);
  if (nouveauPrix && nouvellesParts) {
    plat.prix = parseFloat(nouveauPrix);
    plat.parts = parseInt(nouvellesParts);

    const plats = JSON.parse(localStorage.getItem("plats") || "[]");
    const idx = plats.findIndex(p => p.date === plat.date && p.nom === plat.nom);
    plats[idx] = plat;
    localStorage.setItem("plats", JSON.stringify(plats));
    alert("Plat modifié !");
    afficherCalendrierAdmin(currentMonth, currentYear);
  }
}

function supprimerPlatDepuisJour(platId) {
  const plat = getPlatById(platId);
  if (!plat) return;

  if (confirm(`Supprimer le plat "${plat.nom}" du ${plat.date} ? Toutes les commandes associées seront aussi supprimées.`)) {
    let plats = JSON.parse(localStorage.getItem("plats") || "[]");
    plats = plats.filter(p => !(p.date === plat.date && p.nom === plat.nom));
    localStorage.setItem("plats", JSON.stringify(plats));

    let commandes = JSON.parse(localStorage.getItem("commandes") || "[]");
    commandes = commandes.filter(c => !(c.date === plat.date && c.plat === plat.nom));
    localStorage.setItem("commandes", JSON.stringify(commandes));

    alert("Plat et commandes supprimés.");
    afficherCalendrierAdmin(currentMonth, currentYear);
  }
}

function voirCommandesDepuisJour(platId) {
  const plat = getPlatById(platId);
  if (!plat) return;

  const commandes = JSON.parse(localStorage.getItem("commandes") || "[]")
    .filter(c => c.date === plat.date && c.plat === plat.nom);

  if (commandes.length === 0) {
    alert("Aucune commande pour ce plat.");
    return;
  }

  let texte = `Commandes pour ${plat.nom} (${plat.date}) :\n\n`;

  commandes.forEach((c, i) => {
    texte += `${i + 1}. ${c.nomClient} - ${c.quantite} part(s)\n`;
  });

  alert(texte);
}
function gererPlatDepuisCalendrier(platId) {
  const [date, nom] = platId.split('___');
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const plat = plats.find(p => p.date === date && p.nom === nom);
  if (!plat) return alert("Plat introuvable.");

  const action = prompt(
    `Plat : ${plat.nom} (${plat.date})\nPrix : ${plat.prix} € — ${plat.parts} parts\n\nQue veux-tu faire ?\n1. Modifier\n2. Supprimer\n3. Voir les commandes\n\nEntre le chiffre correspondant :`
  );

  if (action === "1") {
    const nouveauPrix = prompt("Nouveau prix (€) :", plat.prix);
    const nouvellesParts = prompt("Nouveau nombre de parts :", plat.parts);
    if (nouveauPrix && nouvellesParts) {
      plat.prix = parseFloat(nouveauPrix);
      plat.parts = parseInt(nouvellesParts);

      const index = plats.findIndex(p => p.date === plat.date && p.nom === plat.nom);
      plats[index] = plat;
      localStorage.setItem("plats", JSON.stringify(plats));
      alert("Plat modifié !");
      afficherCalendrierAdmin(currentMonth, currentYear);
    }
  } else if (action === "2") {
    if (confirm("Supprimer ce plat ? Cela supprimera aussi les commandes associées.")) {
      const newPlats = plats.filter(p => !(p.date === plat.date && p.nom === plat.nom));
      localStorage.setItem("plats", JSON.stringify(newPlats));

      let commandes = JSON.parse(localStorage.getItem("commandes") || "[]");
      commandes = commandes.filter(c => !(c.date === plat.date && c.plat === plat.nom));
      localStorage.setItem("commandes", JSON.stringify(commandes));

      alert("Plat et commandes supprimés.");
      afficherCalendrierAdmin(currentMonth, currentYear);
    }
  } else if (action === "3") {
    const commandes = JSON.parse(localStorage.getItem("commandes") || "[]")
      .filter(c => c.date === plat.date && c.plat === plat.nom);
    if (commandes.length === 0) return alert("Aucune commande pour ce plat.");

    let texte = `Commandes pour ${plat.nom} (${plat.date}) :\n\n`;
    commandes.forEach((c, i) => {
      texte += `${i + 1}. ${c.nomClient} — ${c.quantite} part(s)\n`;
    });
    alert(texte);
  }
}
function ouvrirModaleAdmin(plat) {
  // 1) Génère le HTML avec des IDs fixed
  const html = `
    <h2 style="text-align:center;">${plat.nom}</h2>
    <p><strong>Date :</strong> ${plat.date}</p>
    <p><strong>Prix :</strong> ${plat.prix} €</p>
    <p><strong>Parts restantes :</strong> ${plat.parts}</p>
    <p><strong>Description :</strong> ${plat.description}</p>
    ${plat.prof ? `<p><strong>Professeur :</strong> ${plat.prof}</p>` : ""}
    <img src="${plat.image}" style="max-width: 100%; margin-top: 10px;"><br><br>

    <div style="text-align:center; margin-bottom:15px;">
      <button id="btn-modifier-plat">✏️ Modifier le plat</button>
      <button id="btn-supprimer-plat" style="margin-left:10px;">🗑️ Supprimer le plat</button>
    </div>

    <hr>
    <h3>Commandes associées :</h3>
    ${(() => {
      const commandes = JSON.parse(localStorage.getItem("commandes")||"[]")
        .filter(c => c.date===plat.date && c.plat===plat.nom);
      if (commandes.length===0) return "<p>Aucune commande.</p>";
      return commandes.map(c=>
        `<div style="border:1px solid #ccc; padding:5px; margin:5px;">
           ${c.nomClient} — ${c.quantite} part(s)
         </div>`
      ).join("");
    })()}
  `;

  // 2) Injecte dans la modale, affiche-la
  const container = document.getElementById("modal-admin-content");
  container.innerHTML = html;
  document.getElementById("modal-admin").style.display = "block";

  // 3) Attache les événements en JS
  document
    .getElementById("btn-supprimer-plat")
    .addEventListener("click", () => {
      supprimerPlatDepuisModale(plat.date, plat.nom);
    });

  document
    .getElementById("btn-modifier-plat")
    .addEventListener("click", () => {
      modifierPlatDepuisModale(plat.date, plat.nom);
    });
}

function supprimerPlatDepuisModale(date, nom) {
  if (confirm(`Voulez-vous vraiment supprimer le plat "${nom}" du ${date} ?`)) {
    let plats = JSON.parse(localStorage.getItem("plats")) || [];
    plats = plats.filter(plat => !(plat.date === date && plat.nom === nom));
    localStorage.setItem("plats", JSON.stringify(plats));
    fermerModaleAdmin();
    afficherCalendrierAdmin(currentMonth, currentYear);
 // recharge le calendrier côté admin
    alert("Plat supprimé !");
  }
}


function modifierPlatDepuisModale(date, nom) {
  const plats = JSON.parse(localStorage.getItem("plats")) || [];
  const plat = plats.find(p => p.date === date && p.nom === nom);
  if (!plat) return alert("Plat introuvable.");

  const contenu = `
    <h2>Modifier le plat</h2>
    <label>Nom : <input id="mod-nom" value="${plat.nom}"></label><br><br>
    <label>Prix : <input type="number" id="mod-prix" value="${plat.prix}"></label><br><br>
    <label>Parts : <input type="number" id="mod-parts" value="${plat.parts}"></label><br><br>
    <label>Description : <textarea id="mod-desc">${plat.description}</textarea></label><br><br>
    <button onclick="enregistrerModifications('${date}', \`${nom}\`)">💾 Enregistrer</button>
    <button onclick="ouvrirModaleAdmin(${JSON.stringify(plat)})" style="margin-left:10px;">↩️ Annuler</button>
  `;

  document.getElementById("modal-admin-content").innerHTML = contenu;
}
function enregistrerModifications(date, nomOriginal) {
  const nouveauxNom = document.getElementById("mod-nom").value;
  const prix = parseFloat(document.getElementById("mod-prix").value);
  const parts = parseInt(document.getElementById("mod-parts").value);
  const desc = document.getElementById("mod-desc").value;

  let plats = JSON.parse(localStorage.getItem("plats")) || [];
  const index = plats.findIndex(p => p.date === date && p.nom === nomOriginal);
  if (index === -1) return alert("Erreur : plat introuvable.");

  plats[index].nom = nouveauxNom;
  plats[index].prix = prix;
  plats[index].parts = parts;
  plats[index].description = desc;

  localStorage.setItem("plats", JSON.stringify(plats));
  ouvrirModaleAdmin(plats[index]); // réaffiche la fiche avec les modifs
  afficherCalendrierAdmin(currentMonth, currentYear);
 // recharge le calendrier
}



function fermerModaleAdmin() {
  document.getElementById("modal-admin").style.display = "none";
}


function fermerModaleAdmin() {
  document.getElementById("modal-admin").style.display = "none";
}
function modifierPlatDepuisModale(date, nom) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const idx = plats.findIndex(p => p.date === date && p.nom === nom);
  if (idx === -1) return;

  const nouveauPrix = prompt("Nouveau prix (€) :", plats[idx].prix);
  const nouvellesParts = prompt("Nouveau nombre de parts :", plats[idx].parts);
  if (nouveauPrix && nouvellesParts) {
    plats[idx].prix = parseFloat(nouveauPrix);
    plats[idx].parts = parseInt(nouvellesParts);
    localStorage.setItem("plats", JSON.stringify(plats));
    alert("Plat modifié !");
    fermerModaleAdmin();
    afficherCalendrierAdmin(currentMonth, currentYear);
  }
}

function supprimerPlatDepuisModale(date, nom) {
  if (!confirm("Supprimer ce plat et toutes ses commandes ?")) return;

  let plats = JSON.parse(localStorage.getItem("plats") || "[]");
  plats = plats.filter(p => !(p.date === date && p.nom === nom));
  localStorage.setItem("plats", JSON.stringify(plats));

  let commandes = JSON.parse(localStorage.getItem("commandes") || "[]");
  commandes = commandes.filter(c => !(c.date === date && c.plat === nom));
  localStorage.setItem("commandes", JSON.stringify(commandes));

  alert("Plat et commandes supprimés.");
  fermerModaleAdmin();
  afficherCalendrierAdmin(currentMonth, currentYear);
}


function modifierCommande(index, date, nomPlat, nouvelleQuantite) {
  let commandes = JSON.parse(localStorage.getItem("commandes") || "[]");
  const filtered = commandes.filter(c => c.date === date && c.plat === nomPlat);

  if (filtered[index]) {
    filtered[index].quantite = parseInt(nouvelleQuantite);
    // Re-tri dans la liste complète
    let all = commandes.filter(c => !(c.date === date && c.plat === nomPlat));
    all = [...all, ...filtered];
    localStorage.setItem("commandes", JSON.stringify(all));
    ouvrirModaleAdmin({ date: date, nom: nomPlat, prix: getPlatPrix(date, nomPlat), parts: getPlatParts(date, nomPlat), image: getPlatImage(date, nomPlat) });
  }
}

function supprimerCommande(index, date, nomPlat) {
  let commandes = JSON.parse(localStorage.getItem("commandes") || "[]");
  const filtered = commandes.filter(c => c.date === date && c.plat === nomPlat);

  if (filtered[index]) {
    filtered.splice(index, 1);
    let all = commandes.filter(c => !(c.date === date && c.plat === nomPlat));
    all = [...all, ...filtered];
    localStorage.setItem("commandes", JSON.stringify(all));
    ouvrirModaleAdmin({ date: date, nom: nomPlat, prix: getPlatPrix(date, nomPlat), parts: getPlatParts(date, nomPlat), image: getPlatImage(date, nomPlat) });
  }
}

function getPlatPrix(date, nom) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const p = plats.find(p => p.date === date && p.nom === nom);
  return p ? p.prix : 0;
}
function getPlatParts(date, nom) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const p = plats.find(p => p.date === date && p.nom === nom);
  return p ? p.parts : 0;
}
function getPlatImage(date, nom) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");
  const p = plats.find(p => p.date === date && p.nom === nom);
  return p ? p.image : "";
}
function ouvrirModaleSelf(menu) {
  const html = `
    <h2>Menu Self du ${menu.date}</h2>
    <p><strong>Entrée :</strong> ${menu.entree}<br><img src="${menu.imageEntree}" style="width:80px;"></p>
    <p><strong>Plat :</strong> ${menu.plat}<br><img src="${menu.imagePlat}" style="width:80px;"></p>
    <p><strong>Dessert :</strong> ${menu.dessert}<br><img src="${menu.imageDessert}" style="width:80px;"></p>
    <p><strong>Chef :</strong> ${menu.chef}</p>
    <button onclick='modifierMenuSelf(${JSON.stringify(menu).replace(/'/g, "&apos;")})'>Modifier</button>
    <button onclick='supprimerMenuSelf("${menu.date}")'>Supprimer</button>
  `;
  document.getElementById("modal-self-contenu").innerHTML = html;
  document.getElementById("modal-self").style.display = "block";
}

function fermerModaleSelf() {
  document.getElementById("modal-self").style.display = "none";
}
function supprimerMenuSelf(date) {
  const menus = JSON.parse(localStorage.getItem("menusSelf") || "[]");
  const newMenus = menus.filter(m => m.date !== date);
  localStorage.setItem("menusSelf", JSON.stringify(newMenus));
  fermerModaleSelf();
  afficherCalendrierAdmin(moisActuel, anneeActuelle); // recharge le calendrier
}

function modifierMenuSelf(menu) {
  // Remplir les champs du formulaire avec les valeurs existantes
  document.getElementById("date-self").value = menu.date;
  document.getElementById("entree").value = menu.entree;
  document.getElementById("image-entree").value = menu.imageEntree;
  document.getElementById("plat").value = menu.plat;
  document.getElementById("image-plat").value = menu.imagePlat;
  document.getElementById("dessert").value = menu.dessert;
  document.getElementById("image-dessert").value = menu.imageDessert;
  document.getElementById("chef").value = menu.chef;

  // Supprimer l'ancien menu
  supprimerMenuSelf(menu.date);
  fermerModaleSelf();

  // Scroll vers le haut pour le formulaire
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

if (document.getElementById("calendar")) {
  document.addEventListener("DOMContentLoaded", () => {
    const aujourdHui = new Date();
    let moisActuel = aujourdHui.getMonth();
    let anneeActuelle = aujourdHui.getFullYear();

    afficherCalendrierAdmin(moisActuel, anneeActuelle);

    document.getElementById("mois-prec").addEventListener("click", () => {
      moisActuel--;
      if (moisActuel < 0) {
        moisActuel = 11;
        anneeActuelle--;
      }
      afficherCalendrierAdmin(moisActuel, anneeActuelle);
    });

    document.getElementById("mois-suiv").addEventListener("click", () => {
      moisActuel++;
      if (moisActuel > 11) {
        moisActuel = 0;
        anneeActuelle++;
      }
      afficherCalendrierAdmin(moisActuel, anneeActuelle);
    });
  });
}
function validerModificationPlat(ancienneDate, ancienNom) {
  const plats = JSON.parse(localStorage.getItem("plats") || "[]");

  // Supprimer l'ancien plat (date + nom)
  const platsModifiés = plats.filter(p => !(p.date === ancienneDate && p.nom === ancienNom));

  // Ajouter le plat modifié
  const nouveauPlat = {
    date: document.getElementById("edit-plat-date").value,
    nom: document.getElementById("edit-plat-nom").value,
    description: document.getElementById("edit-plat-desc").value,
    prix: parseFloat(document.getElementById("edit-plat-prix").value),
    parts: parseInt(document.getElementById("edit-plat-parts").value),
    image: document.getElementById("edit-plat-image").value,
    prof: document.getElementById("edit-plat-prof").value,
    type: "self" // ou "vae", selon ta logique si tu as un mode sélectionné
  };

  platsModifiés.push(nouveauPlat);
  localStorage.setItem("plats", JSON.stringify(platsModifiés));

  alert("Plat modifié !");
  fermerModalAdmin();
  afficherCalendrier(currentMonth, currentYear); // recharge le calendrier avec les nouvelles données
}

window.onload = () => {
  afficherCalendrierAdmin();
};
window.modifierPlatDepuisModale   = modifierPlatDepuisModale;
window.supprimerPlatDepuisModale  = supprimerPlatDepuisModale;
window.enregistrerModifications   = enregistrerModifications;

