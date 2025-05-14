from app import app, db
from models import CompteOkayo, Client, TVA, Produit
from datetime import date

with app.app_context():
    db.create_all()

    # on initialise le compte OKAYO pour pouvoir augmenter le solde
    if not CompteOkayo.query.first():
        compte = CompteOkayo(
            domiciliation="BRED",
            nomCompte="OKAYO",
            codeIBAN=" FR76 0000 0000 0000 0000 0000 097",
            codeBIC="BREDFRPPXXX",
            solde=0
        )
        db.session.add(compte)
        print("Compte OKAYO créé.")
    else:
        print("Le Compte OKAYO existe déjà")

    # on crée le client "Mon client SAS" qui était indiqué dans l'exercice en exemple
    if not Client.query.filter_by(codeClient="2022-0025").first():
        client = Client(
            codeClient="2022-0025",
            nomClient="Mon client SAS",
            adresse="45, rue du test 75016 PARIS"
        )
        db.session.add(client)
        print("client ajouté")
    else:
        print("client déjà existant")

    # 3. on crée les TVAs en exemple
    tva_data = [
        {"taux": 20.0, "dateDebut": date(2020, 1, 1), "dateFin": "Septembre 2026"},
        {"taux": 5.5, "dateDebut": date(2020, 1, 1), "dateFin": "18/04/2025"},
        {"taux": 7.0, "dateDebut": date(2020, 1, 1), "dateFin": "18/04/2025"}
    ]
    for entry in tva_data:
        if not TVA.query.filter_by(taux=entry["taux"]).first():
            db.session.add(TVA(**entry))
            print(f" TVA ajoutée")
        else:
            print(f"TVA déjà existante.")

    db.session.commit()

    # 4. on ajoute des produits dans le catalogue
    tva_20 = TVA.query.filter_by(taux=20.0).first()
    tva_5 = TVA.query.filter_by(taux=5.5).first()
    tva_7 = TVA.query.filter_by(taux=7.0).first()

    catalogue = [
        {"designation": "Mon Produit C", "prixUHT": 70000.00, "idTVA": tva_20.idTVA},
        {"designation": "Mon produit A", "prixUHT": 1500.00, "idTVA": tva_5.idTVA},
        {"designation": "Mon produit D", "prixUHT": 3000.00, "idTVA": tva_20.idTVA},
        {"designation": "Mon produit B ", "prixUHT": 4000.00, "idTVA": tva_7.idTVA}
    ]

    for prod in catalogue:
        if not Produit.query.filter_by(designation=prod["designation"]).first():
            db.session.add(Produit(**prod))
            print(f"Produit ajouté : {prod['designation']}")
        else:
            print(f"le produit existe déjà : {prod['designation']}")

    db.session.commit()
    print("la database est initialisée")
