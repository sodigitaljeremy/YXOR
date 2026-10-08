# Capacités de YXOR : tâches et niveaux à balayer

**Engendré** par `.venv/bin/python scripts/capacites.py --ecrire` depuis `params/capacites.yaml`. Ne pas éditer à la main. Données seulement, **aucune décision**, rien de chiffré (phase 2 de la stratégie de la fiche 0069).

**Principe de Jeremy** (2026-10-05, ses mots) : « Je ne veux plus "fixer" de budget, je veux calculer le budget en fonction des contraintes et de ce qu'il est réellement possible de faire » ; « je veux arbitrer avec des vrais chiffres et non des estimations ». Budget et masse sont des SORTIES de l'explorateur, jamais des filtres.

Les capacités sont celles de la fiche 0069. **Capacités et niveaux CONFIRMÉS par Jeremy le 2026-10-05**, ses mots : « Je confirme la stratégie telle que reformulée par Claude, les capacités que j'ai cochées, et les niveaux proposés dans params/capacites.yaml ». Les articulations sollicitées et les méthodes restent **PROPOSÉES par Claude** ; † = niveaux ajoutés par Claude le 2026-10-05 pour une capacité cochée qui n'en avait pas (confirmés avec les autres). *En italique* : un axe qui n'existe pas encore dans `params/joints.yaml` (nom à créer).

| Tâche | Grandeur | Niveaux à balayer | Articulations sollicitées | Méthode (phase 3) |
| --- | --- | --- | --- | --- |
| marche sur sol plat | vitesse de marche | 0.3 / 0.6 / 1 m/s | hip_yaw, hip_roll, hip_pitch, knee, ankle_pitch, *ankle_roll* | simulation |
| marche sur sol irrégulier | hauteur de marche franchie | 2 / 4 cm | hip_roll, hip_pitch, knee, ankle_pitch, *ankle_roll* | simulation |
| marche en pente | pente | 5 / 10 ° | hip_pitch, knee, ankle_pitch, *ankle_roll* | simulation |
| relevé après une chute | position de départ | depuis le dos / depuis le ventre | hip_pitch, knee, ankle_pitch, shoulder_pitch, elbow_roll, waist_yaw, *waist_pitch* | simulation |
| course | vitesse de course | 1.5 / 2.5 m/s | hip_roll, hip_pitch, knee, ankle_pitch, *ankle_roll* | simulation |
| saut | hauteur du saut (centre de gravité) | 5 / 10 / 20 / 30 cm | hip_pitch, knee, ankle_pitch | energie |
| gestes et pointage † | vitesse du bout du bras (geste rapide) | 0.5 / 1 / 2 m/s | shoulder_pitch, shoulder_roll, shoulder_yaw, elbow_roll, wrist_pitch | energie |
| saisie et port de petits objets | masse de l'objet tenu bras tendu | 0.2 / 0.5 / 1 kg | shoulder_pitch, elbow_roll, wrist_pitch, wrist_roll, *pince* | statique |
| port de charges lourdes | masse portée, bras à 30 cm du torse | 2 / 5 / 10 kg | shoulder_pitch, elbow_roll, *waist_pitch*, hip_pitch, knee, ankle_pitch | statique |
| poussée de charges lourdes † | force horizontale de poussée | 20 / 50 / 100 N | shoulder_pitch, elbow_roll, *waist_pitch*, hip_pitch, knee, ankle_pitch | statique |
| manipulation fine (mains à doigts) | nombre d'axes par main | 6 / 12 / 17 axes | *doigts*, wrist_pitch, wrist_roll | statique |
| rotation et inclinaison du buste | axes du buste | lacet seul / lacet + roulis + tangage | waist_yaw, waist_roll, *waist_pitch* | statique |
| orientation de la tête | axes du cou | 2 / 3 axes | neck_yaw, neck_pitch, *neck_roll* | statique |
| expressions du visage | moyen d'expression | écran / 4 micro-servos / 10 micro-servos | *visage* | statique |
| autonomie sur batterie ‡ | durée d'un enchaînement de cycles « marche + pauses », batterie pleine jusqu'au seuil d'arrêt | 10 / 20 / 30 / 60 min | — | energie |
| IA embarquée ‡ | ce que le calculateur fait tourner à bord | commande seule / + vision / + vision et voix / + modèle de langage local | — | composants |

‡ Ajoutées le 2026-10-07 et **CONFIRMÉES par Jeremy** le même soir, ses mots : « Je confirme les tâches autonomie et IA embarquée, et le cycle de 40 s de marche suivies de 20 s debout. » Cycle : 1 cycle = 60 s : 40 s de marche sur sol plat au niveau du profil, puis 20 s debout immobile (posture tenue, couples de maintien).

## Profils cibles : la gamme YXOR

**Gamme DÉCIDÉE par Jeremy le 2026-10-08** (fiche 0073) : YXOR Kit, YXOR Lab, YXOR Home et YXOR Pro ; « YXOR Pro remplace ce que nous appelions YXOR final ». Kit et Home : capacités À DÉFINIR avec Jeremy.

**YXOR Lab : DÉCIDÉ par Jeremy le 2026-10-07**, ses mots : « Je retiens pour YXOR Lab : marche sur sol plat 0,6 m/s, sol irrégulier 2 cm, pente 5°, relevé sur le dos et sur le ventre, saut 10 cm, gestes 2 m/s, saisie 0,2 kg, poussée 20 N, buste en lacet seul, tête à 2 axes, visage sur écran. Réservé au final : inclinaison du buste, port de charges lourdes, course, mains à doigts. » Puis, le 2026-10-08 (fiche 0073) : « Pour YXOR Lab, le saut est ramené à 5 cm. » YXOR Pro : les capacités de la fiche 0069, niveaux à balayer (phase 4b).

| Tâche | YXOR Kit | YXOR Lab | YXOR Home | YXOR Pro |
| --- | --- | --- | --- | --- |
| marche sol plat | à définir | 0.6 | à définir | à balayer |
| sol irregulier | à définir | 2 | à définir | à balayer |
| pente | à définir | 5 | à définir | à balayer |
| releve | à définir | depuis le dos et depuis le ventre | à définir | à balayer |
| course | à définir | réservé au Pro | à définir | à balayer |
| saut vertical | à définir | 5 | à définir | à balayer |
| gestes pointage | à définir | 2.0 | à définir | à balayer |
| saisie | à définir | 0.2 | à définir | à balayer |
| charge lourde | à définir | réservé au Pro | à définir | à balayer |
| poussee | à définir | 20 | à définir | à balayer |
| mains a doigts | à définir | réservé au Pro | à définir | à balayer |
| buste | à définir | lacet seul | à définir | lacet + roulis + tangage |
| tete | à définir | 2 | à définir | à balayer |
| visage | à définir | écran | à définir | à balayer |
| autonomie | à définir | 30 | à définir | 60 |
| ia embarquee | à définir | + vision | à définir | + modèle de langage local |

## Méthodes

- **simulation** : simulation MuJoCo de la tâche (trajectoire ou politique), relevé des couples, vitesses et puissances par articulation.
- **statique** : équilibre statique dans la posture la plus défavorable : couple = force × bras de levier, par articulation.
- **energie** : bilan d'énergie : potentielle m·g·h, cinétique ½·m·v² ou ½·I·ω², puissance = énergie / durée.
- **composants** : inventaire : puissance, masse et volume des composants (calculateur, accélérateur, capteurs), relevés au marché (docs/marche-calculateurs-2026-10.md).

## Noms d'axes à créer (PROPOSÉS, hors de `joints.yaml`)

- *ankle_roll* (jambes) : existe dans le modèle amont ; déclaré `amont_non_retenus` par la fiche 0068 (à revoir, fiche 0069).
- *waist_pitch* (taille) : tangage du buste (buste à 3 axes).
- *neck_roll* (nuque) : roulis de la tête (tête à 3 axes).
- *doigts* (mains) : 6, 12 ou 17 axes par main selon le niveau ; noms un à un à créer.
- *pince* (mains) : « gripper » du squelette, nom provisoire (squelette.yaml).
- *visage* (tete) : 4 à 10 micro-servos selon le niveau ; noms à créer.

## Sorties de l'explorateur, pour chaque solution

| Sortie | Unité | Formule |
| --- | --- | --- |
| cout | CHF HT | Σ prix des actionneurs (catalogue, taux BCE de params/budget.yaml) + structure, quand son prix sera connu |
| masse | kg | Σ actionneurs + structure (plaques réelles, CAO) + charge utile |
| energie chute | J | m · g · h_cg : masse totale × 9,81 × hauteur du centre de gravité debout |
| energie cinetique membre | J | ½ · I · ω_max² par membre (I autour de l'articulation proximale, ω_max = vitesse à vide de son actionneur) |

Balayage complet : 16 tâches, produit des niveaux = 8 957 952 combinaisons de capacités (avant le choix des axes et des actionneurs).
