# Projet Data-Driven Decision Making (DDDM) - Optimisation Logistique

## Description du Projet
L'objectif principal est de fournir un outil d'aide à la décision basé sur les données historiques, la distance spatiale (formule de Haversine) et les conditions météorologiques, afin d'optimiser l'attribution des coursiers et de minimiser les coûts liés aux pénalités de retard.

## Structure du Dépôt
* `Livraison.ipynb` : Jupyter Notebook contenant l'audit des données, le feature engineering, l'entraînement du modèle prédictif et l'analyse d'explicabilité (SHAP).
* `app.py` : Code source du dashboard interactif Streamlit contenant les 5 vues d'analyse métier.
* `decisionTestImpact.md` : Document détaillant les recommandations stratégiques et le plan d'A/B Testing.
* `dataStory.md` : Pitch narratif détaillant le contexte métier, l'approche analytique et le retour sur investissement (ROI) attendu.
* `requirements.txt` : Liste des dépendances et bibliothèques Python nécessaires à l'exécution du projet.
* `df_livraisons.csv` : Jeu de données nettoyé et enrichi utilisé par le dashboard (généré par le notebook).
* `modele_livraison.pkl` : Fichier binaire du modèle de Machine Learning sérialisé (généré par le notebook).

## Prérequis
* Python 3.8 ou supérieur
* Git
* Compte Kaggle (pour le téléchargement des données brutes)

## Instructions d'Installation et d'Exécution

### 1. Cloner le dépôt
Ouvrez un terminal et clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/hafsaa22/DDDM_project
cd DDDM_project
```

### 2. Créer un environnement virtuel
Sous Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Sous Linux / WSL:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
Installez les bibliothèques requises :
```bash
pip install -r requirements.txt
```

### 4. Télécharger les données Kaggle
Téléchargez les jeux de données bruts depuis Kaggle via ces lien : [Food Delivery Time](https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time), [Weather Data](https://www.kaggle.com/datasets/muthuj7/weather-dataset)
Placez les fichiers CSV téléchargés directement à la racine du projet.

### 5. Exécuter le Notebook (Étape Préalable Obligatoire)
Il est impératif de commencer par l'exécution du notebook avant de tenter de lancer le dashboard. 
Ouvrez et exécutez l'intégralité des cellules du fichier `Livraison.ipynb`. Cette étape va :
* Croiser et nettoyer les données brutes.
* Calculer les distances géographiques.
* Entraîner le modèle de Machine Learning.
* Générer automatiquement les fichiers `df_livraisons.csv` et `modele_livraison.pkl`

### 6. Lancer le Dashboard interactif
Une fois le notebook exécuté et les fichiers nécessaires générés, vous pouvez démarrer l'application Streamlit :
```bash
streamlit run app.py
```
Le dashboard s'ouvrira automatiquement à l'adresse locale `http://localhost:8501`.

## Restitution et Prise de Décision
* Pour comprendre le cheminement métier et la narration des données, consultez le fichier `dataStory.md`.
* Pour consulter les recommandations stratégiques d'optimisation et le protocole expérimental complet (A/B Testing), référez-vous au fichier `decisionTestImpact.md`.