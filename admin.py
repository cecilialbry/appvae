<!DOCTYPE html>
<html lang="fr">
<head>
  

  
  <meta charset="UTF-8">
  <title>Admin - Ajouter un plat</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f5f5f5;
      margin: 20px;
    }

    h1, h2 {
      text-align: center;
      color: #333;
    }

    form {
      background-color: #ffffff;
      padding: 15px;
      border-radius: 10px;
      max-width: 600px;
      margin: auto;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    label {
      display: block;
      margin-top: 10px;
      font-weight: bold;
    }

    input, select {
      width: 100%;
      padding: 8px;
      margin-top: 4px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    #mode-actuel {
      text-align: center;
      margin-top: 15px;
      font-size: 1.1em;
      color: #555;
    }

    #liste-plats > div {
      border: 1px solid #ddd;
      padding: 10px 15px;
      margin: 12px auto;
      max-width: 600px;
      border-radius: 8px;
      background-color: #ffffff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    button {
      padding: 6px 12px;
      font-size: 14px;
      border-radius: 5px;
      border: 1px solid #aaa;
      background-color: #eaeaea;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background-color: #d8d8d8;
    }

    #resultat-commandes {
      max-width: 600px;
      margin: auto;
      background-color: #fff;
      padding: 10px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    hr {
      margin: 20px 0;
    }
    .calendar {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  max-width: 700px;
  margin: auto;
  text-align: center;
  margin-top: 20px;
}
.day {
  border: 1px solid #ccc;
  padding: 10px;
  min-height: 60px;
  font-size: 14px;
  background-color: white;
  border-radius: 6px;
  cursor: pointer;
}
.header {
  font-weight: bold;
  background-color: #eee;
  cursor: default;
}

  </style>
  <link rel="stylesheet" href="style.css">
<!-- Firebase SDK -->

</script>
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
  import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

  const firebaseConfig = {
    apiKey: "AIzaSyCHClKNancbvFb3peypZAG5q6qOny9rUEc",
    authDomain: "vae-self-site.firebaseapp.com",
    databaseURL: "https://vae-self-site-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "vae-self-site",
    storageBucket: "vae-self-site.appspot.com",
    messagingSenderId: "312344689130",
    appId: "1:312344689130:web:c8c98f2b7a820533419a93",
    measurementId: "G-YEVD3PMQ4V"
  };

  // 🔸 Tu colles CE BLOC juste ici :
  const app = initializeApp(firebaseConfig);
  const db = getDatabase(app);

  // 🔸 Puis tu ajoutes aussi CE CODE juste après :
  function afficherPlatsDansCalendrier() {
    const platsRef = ref(db, 'plats/');

    onValue(platsRef, (snapshot) => {
      const data = snapshot.val();
      if (!data) return;

      document.querySelectorAll('.day .plats').forEach(el => el.remove());

      Object.entries(data).forEach(([id, plat]) => {
        const date = new Date(plat.date);
        const jour = date.getDate();
        const caseJour = document.querySelector(`.day[data-day="${jour}"]`);
        if (caseJour) {
          const div = document.createElement("div");
          div.className = "plats";
          div.textContent = `${plat.nom} (${plat.parts} parts)`;
          caseJour.appendChild(div);
        }
      });
    });
  }

  afficherPlatsDansCalendrier();
</script>


</head>
<body>

  <h2>Ajouter une vente à emporter</h2>

  <form id="form-plat">
    <label>Date : <input type="date" id="date" required></label>
    <label>Nom du plat : <input type="text" id="nom" required></label>
    <label>Prix (€) : <input type="number" id="prix" step="0.01" required></label>
    <label>Nombre de parts disponibles : <input type="number" id="parts" required></label>
    <label>Image (URL) : <input type="text" id="image" required></label>
    <label>Description : <input type="text" id="description" required></label>
    <label>Professeur responsable (VAE) :</label>
    <input type="text" id="prof" placeholder="Nom du professeur"><br><br>
    <input type="hidden" id="type-plat" value="vae">


    
    <p id="mode-actuel" style="font-weight: bold;"></p>
    <button type="submit">Ajouter le plat</button>
  </form>

<div id="calendrier" class="calendrier"></div>
<h2>Ajouter un menu Self pédagogique</h2>
<form id="form-self">
  <form id="form-self">
  <label>Date : <input type="date" id="date-self" required></label><br>
  <label>Entrée : <input type="text" id="entree" required></label><br>
  <label>Image entrée : <input type="text" id="image-entree" placeholder="URL image"></label><br>
  <label>Plat : <input type="text" id="plat" required></label><br>
  <label>Ima
