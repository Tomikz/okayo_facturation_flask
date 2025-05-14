from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import *
from datetime import datetime
import random, string
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def generer_ref_facture():
    """on crée la référence en commançant par FA-"""
    while True:
        ref = "FA-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Facture.query.filter_by(refFacture=ref).first():
            return ref

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            #  on crée la facture
            ref = generer_ref_facture()
            facture = Facture(
                refFacture=ref,
                idClient=int(request.form['idClient']),
                dateFacturation=datetime.strptime(request.form['dateFacturation'], '%Y-%m-%d'),
                dateEcheance=datetime.strptime(request.form['dateEcheance'], '%Y-%m-%d'),
                conditionReglement=request.form['conditionReglement'],
                totalHTFacture=0,
                totalTTC=0
            )
            db.session.add(facture)
            db.session.commit()

            # Lignes de facture
            total_ht = 0
            total_ttc = 0
            produits_ids = request.form.getlist('produits[]')

            for pid in produits_ids:
                produit = Produit.query.get(int(pid))
                quantite = int(request.form.get(f'quantite_{pid}', 1))
                total_ligne_ht = produit.prixUHT * quantite
                tva_obj = TVA.query.get(produit.idTVA)
                taux_tva = tva_obj.taux / 100
                total_ligne_ttc = total_ligne_ht * (1 + taux_tva)

                ligne = ProduitFacture(
                    idFacture=facture.idFacture,
                    idProduit=produit.idProduit,
                    designation=produit.designation,
                    prixUHT=produit.prixUHT,
                    tva=tva_obj.taux,
                    quantite=quantite,
                    totalHT=round(total_ligne_ht, 2)
                )
                db.session.add(ligne)

                total_ht += total_ligne_ht
                total_ttc += total_ligne_ttc

            facture.totalHTFacture = round(total_ht, 2)
            facture.totalTTC = round(total_ttc, 2)

            compte = CompteOkayo.query.first()
            if compte:
                compte.solde += facture.totalHTFacture

            db.session.commit()

            return redirect(url_for('facture_detail', id=facture.idFacture))

        except IntegrityError:
            db.session.rollback()
            return "la facture n'a pas pu être créée", 400
        except Exception as e:
            db.session.rollback()
            print("ERREUR :", e)
            return "Erreur serveur", 500

    clients = Client.query.all()
    produits = Produit.query.filter_by(toujoursActif=True).all()
    return render_template('index.html', clients=clients, produits=produits)


@app.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'produit':
            produit = Produit(
                designation=request.form['designation'],
                prixUHT=float(request.form['prixUHT']),
                toujoursActif=True,  # le produit est forcément activé à la création
                idTVA=int(request.form['idTVA'])
            )
            db.session.add(produit)
            db.session.commit()

        elif form_type == 'tva':
            tva = TVA(
                taux=float(request.form['taux']),
                dateDebut=datetime.strptime(request.form['dateDebut'], '%Y-%m-%d'),
                dateFin=request.form['dateFin'] or None
            )
            db.session.add(tva)
            db.session.commit()

        return redirect(url_for('catalogue'))

    show_all = request.args.get('show') == 'all'
    if show_all:
        produits = Produit.query.all()
    else:
        produits = Produit.query.filter_by(toujoursActif=True).all()

    tva_list = TVA.query.all()
    tvas = {tva.idTVA: tva.taux for tva in tva_list}
    return render_template('catalogue.html', produits=produits, tvas=tvas, tva_list=tva_list, show_all=show_all)

@app.route('/supprimer_produit/<int:id>', methods=['POST'])
def supprimer_produit(id):
    produit = Produit.query.get_or_404(id)
    produit.toujoursActif = False
    db.session.commit()
    return redirect(url_for('catalogue'))


@app.route('/supprimer_tva/<int:id>', methods=['POST'])
def supprimer_tva(id):
    tva = TVA.query.get_or_404(id)
    db.session.delete(tva)
    db.session.commit()
    return redirect(url_for('catalogue'))

@app.route('/modifier_produit/<int:id>', methods=['POST'])
def modifier_produit(id):
    produit = Produit.query.get_or_404(id)

    produit.designation = request.form['designation']
    produit.prixUHT = float(request.form['prixUHT'])
    produit.idTVA = int(request.form['idTVA'])

    db.session.commit()
    return redirect(url_for('catalogue', show='all'))  # on retourne au catalogue complet

@app.route('/modifier_tva/<int:id>', methods=['POST'])
def modifier_tva(id):
    tva = TVA.query.get_or_404(id)
    tva.taux = float(request.form['taux'])
    tva.dateDebut = datetime.strptime(request.form['dateDebut'], '%Y-%m-%d')
    tva.dateFin = request.form['dateFin'] or None
    db.session.commit()
    return redirect(url_for('catalogue', show='all'))

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        client = Client(
            codeClient=request.form['codeClient'],
            nomClient=request.form['nomClient'],
            adresse=request.form['adresse']
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/facture/<int:id>')
def facture_detail(id):
    facture = Facture.query.get_or_404(id)
    client = Client.query.get(facture.idClient)
    lignes = ProduitFacture.query.filter_by(idFacture=id).all()
    compte = CompteOkayo.query.first()

    #on regroupe les montants de TVA par taux
    tva_totaux = {} 
    for ligne in lignes:
        taux = ligne.tva
        montant_tva = round((ligne.totalHT * taux / 100), 2)
        if taux in tva_totaux:
            tva_totaux[taux] += montant_tva
        else:
            tva_totaux[taux] = montant_tva

    return render_template(
        'facture_detail.html',
        facture=facture,
        client=client,
        lignes=lignes,
        compte=compte,
        tva_totaux=tva_totaux
    )


@app.route('/factures')
def factures():
    client_id = request.args.get('client_id', type=int)
    if client_id:
        factures_filtrees = Facture.query.filter_by(idClient=client_id).order_by(Facture.dateFacturation.desc()).all()
    else:
        factures_filtrees = Facture.query.order_by(Facture.dateFacturation.desc()).all()

    clients = Client.query.all()
    client_dict = {client.idClient: client.nomClient for client in clients}

    return render_template('factures.html',
                           factures=factures_filtrees,
                           clients=clients,
                           client_dict=client_dict,
                           client_id=client_id)

@app.route('/supprimer_facture/<int:id>', methods=['POST'])
def supprimer_facture(id):
    facture = Facture.query.get_or_404(id)

    # on supprime les lignes associées
    ProduitFacture.query.filter_by(idFacture=id).delete()

    # on suupprime la facture 
    db.session.delete(facture)
    db.session.commit()
    return redirect(url_for('factures'))

@app.context_processor
def inject_solde():
    from models import CompteOkayo
    compte = CompteOkayo.query.first()
    return {'solde': compte.solde if compte else 0.0}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
