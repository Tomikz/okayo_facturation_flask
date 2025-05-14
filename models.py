from extensions import db

class Client(db.Model):
    __tablename__ = 'client'
    idClient = db.Column(db.Integer, primary_key=True)
    codeClient = db.Column(db.String(50), nullable=False, unique=True)
    nomClient = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)

class Produit(db.Model):
    __tablename__ = 'produit'
    idProduit = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100), nullable=False)
    prixUHT = db.Column(db.Float, nullable=False)
    toujoursActif = db.Column(db.Boolean, default=True)
    idTVA = db.Column(db.Integer, db.ForeignKey('tva.idTVA'), nullable=False)

class ProduitFacture(db.Model):
    __tablename__ = 'produitfacture'
    idProduitFacture = db.Column(db.Integer, primary_key=True)
    idFacture = db.Column(db.Integer, db.ForeignKey('facture.idFacture'), nullable=False)
    idProduit = db.Column(db.Integer, db.ForeignKey('produit.idProduit'), nullable=True)
    designation = db.Column(db.String(100), nullable=False)
    prixUHT = db.Column(db.Float, nullable=False)
    tva = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    totalHT = db.Column(db.Float, nullable=False)

class Facture(db.Model):
    __tablename__ = 'facture'
    idFacture = db.Column(db.Integer, primary_key=True)
    refFacture = db.Column(db.String(50), nullable=False, unique=True)
    idClient = db.Column(db.Integer, db.ForeignKey('client.idClient'), nullable=False)
    dateFacturation = db.Column(db.Date, nullable=False)
    dateEcheance = db.Column(db.Date, nullable=False)
    conditionReglement = db.Column(db.String(100), nullable=False)
    totalHTFacture = db.Column(db.Float, default=0)
    totalTTC = db.Column(db.Float, default=0)

class TVA(db.Model):
    __tablename__ = 'tva'
    idTVA = db.Column(db.Integer, primary_key=True)
    taux = db.Column(db.Float, nullable=False)
    dateDebut = db.Column(db.Date, nullable=False)
    dateFin = db.Column(db.String(50), nullable=True)

class CompteOkayo(db.Model):
    __tablename__ = 'compteokayo'
    idCompte = db.Column(db.Integer, primary_key=True)
    domiciliation = db.Column(db.String(100))
    nomCompte = db.Column(db.String(100), nullable=False)
    codeIBAN = db.Column(db.String(100))
    codeBIC = db.Column(db.String(100))
    solde = db.Column(db.Float, default=0)
