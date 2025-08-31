

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_plat', methods=['POST'])
def add_plat():
    data = request.form
    plat_data = {
        'date': data['date'],
        'nom': data['nom'],
        'prix': float(data['prix']),
        'parts': int(data['parts']),
        'image': data['image'],
        'description': data['description'],
        'prof': data['prof'],
        'type': 'vae'
    }

    ref = db.reference('plats')
    new_plat_ref = ref.push()
    new_plat_ref.set(plat_data)

    return jsonify({'status': 'success'})

@app.route('/add_self', methods=['POST'])
def add_self():
    data = request.form
    self_data = {
        'date': data['date-self'],
        'entree': data['entree'],
        'image_entree': data['image-entree'],
        'plat': data['plat'],
        'image_plat': data['image-plat'],
        'dessert': data['dessert'],
        'image_dessert': data['image-dessert'],
        'prof': data['prof-self'],
        'type': 'self'
    }

    ref = db.reference('selfs')
    new_self_ref = ref.push()
    new_self_ref.set(self_data)

    return jsonify({'status': 'success'})

@app.route('/get_plats')
def get_plats():
    ref = db.reference('plats')
    plats = ref.get()
    return jsonify(plats or {})

if __name__ == '__main__':
    app.run(debug=True)
```



```html
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
</head>
<body>
    <h2>Ajouter une vente à emporter</h2>

    <form id="form-plat" action="/add_plat" method="post">
        <label>Date : <input type="date" name="date" required></label>
        <label>Nom du plat : <input type="text" name="nom" required></label>
        <label>Prix (€) : <input type="number" name="prix" step="0.01" required></label>
        <label>Nombre de parts disponibles : <input type="number" name="parts" required></label>
        <label>Image (URL) : <input type="text" name="image" required></label>
        <label>Description : <input type="text" name="description" required></label>
        <label>Professeur responsable (VAE) :</label>
        <input type="text" name="prof" placeholder="Nom du professeur"><br><br>
        <input type="hidden" name="type-plat" value="vae">

        <p id="mode-actuel" style="font-weight: bold;"></p>
        <button type="submit">Ajouter le plat</button>
    </form>

    <div id="calendrier" class="calendrier"></div>

    <h2>Ajouter un menu Self pédagogique</h2>
    <form id="form-self" action="/add_self" method="post">
        <label>Date : <input type="date" name="date-self" required></label><br>
        <label>Entrée : <input type="text" name="entree" required></label><br>
        <label>Image entrée : <input type="text" name="image-entree" placeholder="URL image"></label><br>
        <label>Plat : <input type="text" name="plat" required></label><br>
        <label>Image plat : <input type="text" name="image-plat" placeholder="URL image"></label><br>
        <label>Dessert : <input type="text" name="dessert" required></label><br>
        <label>Image dessert : <input type="text" name="image-dessert" placeholder="URL image"></label><br>
        <label>Professeur responsable (Self) :</label>
        <input type="text" name="prof-self" placeholder="Nom du professeur"><br><br>
        <input type="hidden" name="type-self" value="self">

        <button type="submit">Ajouter le menu Self</button>
    </form>

    <script>
        // Function to display dishes in the calendar
        function afficherPlatsDansCalendrier() {
            fetch('/get_plats')
                .then(response => response.json())
                .then(data => {
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

        // Call the function when the page loads
        window.onload = function() {
            afficherPlatsDansCalendrier();
        };
    </script>
</body>
</html>
```
