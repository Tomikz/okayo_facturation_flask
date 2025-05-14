Ceci est le fichier README pour la simulation d'un système de gestion de factures

Voici les fonctionnalités

- Création de factures avec une sélection des produits voulus et leur quantités 
- Visualisation des factures avec un visuel proche de la consigne
- Gestion des clients, produits, TVA et catalogue
- Historique des factures avec un système de filtrage par client
- Calcul automatique du total HT, TTC et du montant des TVA par taux
- Mise à jour automatique du solde du compte OKAYO après l'émission d’une facture

Pour installer et tester le projet voici les étapes à suivre :

1) Cloner le dépôt :

git clone https://github.com/Tomikz/okayo_facturation_flask.git

cd okayo_facturation_flask

2) On crée un environnement virtuel:

python -m venv venv
source venv/bin/activate  # pour linux/macOS
venv\Scripts\activate     # pour windows

3. On Installe les dépendances:

pip install -r requirements.txt

4. Enfin on initialise la base de données avec les données exemple de l'exercice:

python init_db.py


Voici les données initialisées : 

- Le compte OKAYO pour le solde
- Le client Mon client SAS avec adresse
- Les taux de TVA : 20.0%, 5.5%, 7.0%
- Produits d’exemple avec différents taux de TVA


Pour lancer l'application il faut utiliser la commande:

python app.py

Après ça il faut ouvrir l'url "http://127.0.0.1:5000" dans un navigateur


Possibilités d'évolutions :

Ce projet peut être grandement amélioré, que ce soit au niveau du design ou bien d'ajout de fonctionnalités. 
Voici certains points d'améliorations qui peuvent être intéressants à explorer :

- Essayer de centraliser sur une page ou deux au lieu de faire un onglet par "item" dans la navbar
- Ajout d'un système permettant de transformer les factures en PDF et de pouvoir les télécharger
- Essayer de mettre en place une réelle fonction pour les conditions de règlement
- Coder une fonction qui supprime ou désactive une tva pour laquelle la date dépasse la date limite/période donnée
- Ajouter un système de majoration si le paiement du client dépasse l'échéancier 




