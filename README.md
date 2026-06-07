# Projet Data-Driven Decision Making (DDDM) - Optimisation Logistique

## Structure du Dépôt
* `Livraison.ipynb` : Jupyter Notebook contenant l'audit des données, le feature engineering, l'entraînement du modèle prédictif et l'analyse d'explicabilité (SHAP).
* `app.py` : Code source du dashboard interactif Streamlit contenant les 5 vues d'analyse métier (Direction, Opérations, Marketing, RH, et Simulateur IA).
* `requirements.txt` : Liste des dépendances et bibliothèques Python nécessaires à l'exécution du projet.
* `df_livraisons.csv` : Jeu de données nettoyé et enrichi utilisé par le dashboard à générer via le notebook.

## Prérequis
* Python 3.8 ou supérieur
* Git

## Instructions d'Installation et d'Exécution

### 1. Cloner le dépôt
Ouvrez un terminal et clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/hafsaa22/DDDM_project
cd DDDM_project
```

### 2. Créer un environnement virtuel
Sous Windows :
```bash
python -m venv .venv
.venv\Scripts\activate
```

Sous Linux / WSL :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
Installez les bibliothèques requises :
```bash
pip install -r requirements.txt
```

### 4. Lancer le Dashboard interactif
Assurez-vous que les fichiers de données (`.csv`) sont présents à la racine du projet. Lancez l'application Streamlit :
```bash
streamlit run app.py
```
Le dashboard s'ouvrira automatiquement à l'adresse locale `http://localhost:8501`.

## Prise de Décision et Mesure d'Impact
Le rapport complet détaillant les 3 recommandations stratégiques d'optimisation (routage dynamique prédictif, communication proactive, réduction de la zone de couverture) et le plan de test expérimental (A/B Testing) est disponible dans la [documentation du projet](decisionTestImpact.md).