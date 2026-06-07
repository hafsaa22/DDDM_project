## 1. Recommandations Actionnables (Hiérarchisées)

L'analyse croisée des données de livraison et l'explicabilité du modèle (SHAP) ont mis en évidence l'impact majeur de la distance et des conditions météorologiques sur les retards critiques. Pour maximiser la rentabilité (Niveau 1 du KPI Tree), trois leviers opérationnels sont recommandés :

* **Recommandation 1 (Priorité Haute - Logistique) : Routage dynamique prédictif.**
  * *Action :* Intégrer l'algorithme d'Aide à la Décision directement dans le système d'attribution. Dès qu'une commande franchit un seuil de risque de retard de 60% (ex: distance > 8km couplée à de la pluie), le système force l'attribution à un coursier motorisé (scooter/moto) et bloque l'option vélo.
  * *Justification :* Les graphes SHAP prouvent que le vélo est une force de retard majeure sur les longues distances sous intempéries.

* **Recommandation 2 (Priorité Moyenne - Expérience Client) : Communication proactive et "Soft Compensation".**
  * *Action :* Si le modèle prédit un retard inévitable au moment de la commande, déclencher automatiquement un SMS préventif au client proposant une livraison différée contre un bon d'achat immédiat de 2€.
  * *Justification :* Prévenir le client coûte infiniment moins cher (2€) que le remboursement complet d'une commande hors délai (généralement estimé à 15-20€), tout en réduisant drastiquement le risque de churn.

* **Recommandation 3 (Priorité Basse - Stratégie) : Réduction dynamique du rayon de couverture.**
  * *Action :* Désactiver temporairement la visibilité des restaurants situés à plus de 10 km des zones résidentielles lors de fortes précipitations.
  * *Justification :* Limiter le volume global pour privilégier le respect des délais (SLA) sur les trajets courts, préservant ainsi la note de satisfaction moyenne globale.

---

## 2. Protocole Expérimental : Plan d'A/B Testing

Pour mesurer l'impact réel de la **Recommandation 1** (Routage dynamique prédictif) sans risquer de perturber l'ensemble du système, nous déploierons le modèle ML en conditions réelles selon le protocole suivant.

### 2.1 Hypothèses du Test
* **Hypothèse Nulle ($H_0$) :** L'affectation algorithmique prédictive (Groupe B) ne réduit pas de manière significative le taux de commandes hors délai (>45 min) par rapport à l'affectation standard (Groupe A).
* **Hypothèse Alternative ($H_1$) :** L'affectation algorithmique prédictive diminue le taux de commandes hors délai d'au moins 15% (baisse relative).

### 2.2 Échantillonnage et Déploiement
* **Population Cible :** Toutes les commandes passées durant les heures de pointe (12h-14h et 19h-22h) dans un corridor urbain représentatif et dense (zone pilote garantissant un volume statistique suffisant).
* **Répartition :** Test A/B classique (50% / 50%) avec assignation aléatoire par identifiant de commande (Hash Modulo 2) pour éviter les biais de sélection.
  * *Groupe A (Contrôle) :* Algorithme standard d'attribution au coursier le plus proche, sans considération météo/véhicule.
  * *Groupe B (Traitement) :* Passage par le modèle ML. Si Risque > 60%, filtrage strict des vélos au profit des motos.

### 2.3 Durée et Taille d'Échantillon (Power Analysis)
Pour obtenir des résultats statistiquement significatifs (Puissance statistique de 80% et niveau de confiance $\alpha = 0.05$) :
* **Taux de conversion de base (Retards actuels) :** estimé à environ 20%.
* **Effet minimum détectable souhaité :** baisse à 17% de retards (soit -15% relatifs).
* **Taille d'échantillon requise :** Environ 2 700 commandes par variante (5 400 commandes au total).
* **Durée du test :** Fixée à **14 jours (2 semaines pleines)** pour lisser les effets de saisonnalité intra-hebdomadaire (pics du week-end vs jours ouvrés).

### 2.4 Métriques de Suivi Post-Décision
Le succès de l'expérimentation sera validé via notre KPI Tree :
* **Métrique Primaire :** Taux de livraisons hors délai (objectif : < 17%).
* **Métriques Secondaires (Garde-fous) :**
  * *Temps moyen de disponibilité des livreurs motorisés :* Pour s'assurer que la réaffectation ne crée pas de goulots d'étranglement logistiques (pénurie de motos).
  * *Coût moyen d'acquisition par livraison :* Comparer les coûts opérationnels entre le Groupe A et B (une moto coûtant potentiellement plus cher au kilomètre qu'un vélo).