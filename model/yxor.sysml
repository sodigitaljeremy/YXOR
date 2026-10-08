// ENGENDRÉ par `.venv/bin/python scripts/sysml.py --ecrire` depuis params/ : NE PAS ÉDITER À LA MAIN.
// Pilote SysML v2 (2026-10-08). Le YAML reste la source de vérité ; ce fichier en est une vue.
package YXOR {

    doc /* Gamme YXOR (fiche 0073) : Kit, Lab, Home et Pro, variantes d'une même famille. */

    // ── Axes (params/joints.yaml, règle 3 : mêmes noms partout) ──
    package Axes {
        part def Articulation;
        part def hip_yaw :> Articulation;
        part def hip_roll :> Articulation;
        part def hip_pitch :> Articulation;
        part def knee :> Articulation;
        part def ankle_pitch :> Articulation;
        part def shoulder_pitch :> Articulation;
        part def shoulder_roll :> Articulation;
        part def shoulder_yaw :> Articulation;
        part def elbow_roll :> Articulation;
        part def elbow_yaw :> Articulation;
        part def wrist_pitch :> Articulation;
        part def wrist_roll :> Articulation;
        part def waist_yaw :> Articulation;
        part def waist_roll :> Articulation;
        part def neck_yaw :> Articulation;
        part def neck_pitch :> Articulation;
    }

    // ── Ensembles d'axes de l'explorateur (scripts/explorateur.py, ENSEMBLES) ──
    package Ensembles {
        private import Axes::*;
        part def Ensemble25 {
            doc /* 25 axes. JAMAIS calculé le 2026-10-04 (seulement cité par le prompt d'alors) : le 26 sans roulis de taille */
            part hip_yaw : Axes::hip_yaw[2];
            part hip_roll : Axes::hip_roll[2];
            part hip_pitch : Axes::hip_pitch[2];
            part knee : Axes::knee[2];
            part ankle_pitch : Axes::ankle_pitch[2];
            part shoulder_pitch : Axes::shoulder_pitch[2];
            part shoulder_roll : Axes::shoulder_roll[2];
            part elbow_roll : Axes::elbow_roll[2];
            part wrist_pitch : Axes::wrist_pitch[2];
            part wrist_roll : Axes::wrist_roll[2];
            part gripper : Articulation[2];   // nom provisoire, absent de joints.yaml
            part waist_yaw : Axes::waist_yaw[1];
            part neck_yaw : Axes::neck_yaw[1];
            part neck_pitch : Axes::neck_pitch[1];
        }
        part def Ensemble26 {
            doc /* 26 axes. squelette v3 (params/squelette.yaml, fiche 0068 : 5 axes par jambe) */
            part hip_yaw : Axes::hip_yaw[2];
            part hip_roll : Axes::hip_roll[2];
            part hip_pitch : Axes::hip_pitch[2];
            part knee : Axes::knee[2];
            part ankle_pitch : Axes::ankle_pitch[2];
            part shoulder_pitch : Axes::shoulder_pitch[2];
            part shoulder_roll : Axes::shoulder_roll[2];
            part elbow_roll : Axes::elbow_roll[2];
            part wrist_pitch : Axes::wrist_pitch[2];
            part wrist_roll : Axes::wrist_roll[2];
            part gripper : Articulation[2];   // nom provisoire, absent de joints.yaml
            part waist_yaw : Axes::waist_yaw[1];
            part waist_roll : Axes::waist_roll[1];
            part neck_yaw : Axes::neck_yaw[1];
            part neck_pitch : Axes::neck_pitch[1];
        }
        part def Ensemble27 {
            doc /* 27 axes. fiche 0069 (proposition de Claude) et étude du 2026-10-04 : jambes 6 × 2, taille 1, bras 5 × 2, pinces, cou 2 */
            part hip_yaw : Axes::hip_yaw[2];
            part hip_roll : Axes::hip_roll[2];
            part hip_pitch : Axes::hip_pitch[2];
            part knee : Axes::knee[2];
            part ankle_pitch : Axes::ankle_pitch[2];
            part ankle_roll : Articulation[2];   // dans joints.yaml, « amont_non_retenus » (fiche 0068)
            part shoulder_pitch : Axes::shoulder_pitch[2];
            part shoulder_roll : Axes::shoulder_roll[2];
            part elbow_roll : Axes::elbow_roll[2];
            part wrist_pitch : Axes::wrist_pitch[2];
            part wrist_roll : Axes::wrist_roll[2];
            part gripper : Articulation[2];   // nom provisoire, absent de joints.yaml
            part waist_yaw : Axes::waist_yaw[1];
            part neck_yaw : Axes::neck_yaw[1];
            part neck_pitch : Axes::neck_pitch[1];
        }
        part def Ensemble29 {
            doc /* 29 axes. étude du 2026-10-04 (« 29, bras 5 ») : le 27 avec la taille à 3 axes */
            part hip_yaw : Axes::hip_yaw[2];
            part hip_roll : Axes::hip_roll[2];
            part hip_pitch : Axes::hip_pitch[2];
            part knee : Axes::knee[2];
            part ankle_pitch : Axes::ankle_pitch[2];
            part ankle_roll : Articulation[2];   // dans joints.yaml, « amont_non_retenus » (fiche 0068)
            part shoulder_pitch : Axes::shoulder_pitch[2];
            part shoulder_roll : Axes::shoulder_roll[2];
            part elbow_roll : Axes::elbow_roll[2];
            part wrist_pitch : Axes::wrist_pitch[2];
            part wrist_roll : Axes::wrist_roll[2];
            part gripper : Articulation[2];   // nom provisoire, absent de joints.yaml
            part waist_yaw : Axes::waist_yaw[1];
            part waist_roll : Axes::waist_roll[1];
            part waist_pitch : Articulation[1];   // nom provisoire, absent de joints.yaml
            part neck_yaw : Axes::neck_yaw[1];
            part neck_pitch : Axes::neck_pitch[1];
        }
    }

    // ── Capacités et niveaux (params/capacites.yaml) ──
    package Capacites {
        enum def Niveau_marche_sol_plat {
            doc /* marche sur sol plat ; grandeur : vitesse de marche (m/s). */
            enum n0_3;
            enum n0_6;
            enum n1_0;
        }
        enum def Niveau_sol_irregulier {
            doc /* marche sur sol irrégulier ; grandeur : hauteur de marche franchie (cm). */
            enum n2;
            enum n4;
        }
        enum def Niveau_pente {
            doc /* marche en pente ; grandeur : pente (°). */
            enum n5;
            enum n10;
        }
        enum def Niveau_releve {
            doc /* relevé après une chute ; grandeur : position de départ (—). */
            enum depuis_le_dos;
            enum depuis_le_ventre;
        }
        enum def Niveau_course {
            doc /* course ; grandeur : vitesse de course (m/s). */
            enum n1_5;
            enum n2_5;
        }
        enum def Niveau_saut_vertical {
            doc /* saut ; grandeur : hauteur du saut (centre de gravité) (cm). */
            enum n5;
            enum n10;
            enum n20;
            enum n30;
        }
        enum def Niveau_gestes_pointage {
            doc /* gestes et pointage ; grandeur : vitesse du bout du bras (geste rapide) (m/s). */
            enum n0_5;
            enum n1_0;
            enum n2_0;
        }
        enum def Niveau_saisie {
            doc /* saisie et port de petits objets ; grandeur : masse de l'objet tenu bras tendu (kg). */
            enum n0_2;
            enum n0_5;
            enum n1_0;
        }
        enum def Niveau_charge_lourde {
            doc /* port de charges lourdes ; grandeur : masse portée, bras à 30 cm du torse (kg). */
            enum n2;
            enum n5;
            enum n10;
        }
        enum def Niveau_poussee {
            doc /* poussée de charges lourdes ; grandeur : force horizontale de poussée (N). */
            enum n20;
            enum n50;
            enum n100;
        }
        enum def Niveau_mains_a_doigts {
            doc /* manipulation fine (mains à doigts) ; grandeur : nombre d'axes par main (axes). */
            enum n6;
            enum n12;
            enum n17;
        }
        enum def Niveau_buste {
            doc /* rotation et inclinaison du buste ; grandeur : axes du buste (—). */
            enum lacet_seul;
            enum lacet_plus_roulis_plus_tangage;
        }
        enum def Niveau_tete {
            doc /* orientation de la tête ; grandeur : axes du cou (axes). */
            enum n2;
            enum n3;
        }
        enum def Niveau_visage {
            doc /* expressions du visage ; grandeur : moyen d'expression (—). */
            enum ecran;
            enum n4_micro_servos;
            enum n10_micro_servos;
        }
        enum def Niveau_autonomie {
            doc /* autonomie sur batterie ; grandeur : durée d'un enchaînement de cycles « marche + pauses », batterie pleine jusqu'au seuil d'arrêt (min). */
            enum n10;
            enum n20;
            enum n30;
            enum n60;
        }
        enum def Niveau_ia_embarquee {
            doc /* IA embarquée ; grandeur : ce que le calculateur fait tourner à bord (—). */
            enum commande_seule;
            enum plus_vision;
            enum plus_vision_et_voix;
            enum plus_modele_de_langage_local;
        }
    }

    // ── La gamme : quatre variantes d'une même famille (fiche 0073 ; profils de params/capacites.yaml) ──
    package Gamme {
        private import Capacites::*;
        part def ModeleYXOR {
            doc /* Ce que tout modèle de la gamme partage : la famille. */
            attribute marche_sol_plat : Niveau_marche_sol_plat[0..*];
            attribute sol_irregulier : Niveau_sol_irregulier[0..*];
            attribute pente : Niveau_pente[0..*];
            attribute releve : Niveau_releve[0..*];
            attribute course : Niveau_course[0..*];
            attribute saut_vertical : Niveau_saut_vertical[0..*];
            attribute gestes_pointage : Niveau_gestes_pointage[0..*];
            attribute saisie : Niveau_saisie[0..*];
            attribute charge_lourde : Niveau_charge_lourde[0..*];
            attribute poussee : Niveau_poussee[0..*];
            attribute mains_a_doigts : Niveau_mains_a_doigts[0..*];
            attribute buste : Niveau_buste[0..*];
            attribute tete : Niveau_tete[0..*];
            attribute visage : Niveau_visage[0..*];
            attribute autonomie : Niveau_autonomie[0..*];
            attribute ia_embarquee : Niveau_ia_embarquee[0..*];
        }
        part def YXOR_Kit :> ModeleYXOR {
            doc /* modèle décidé (fiche 0073, premier fabriqué) ; modules successifs, même taille, même squelette et mêmes composants que le Lab, en carton, aux outils du ménage (fiche 0074, Jeremy, 2026-10-08) ; capacités et niveaux des modules PROPOSÉS */
            // capacités À DÉFINIR avec Jeremy
        }
        part def YXOR_Lab :> ModeleYXOR {
            doc /* Jeremy, 2026-10-07, réponse à la question de Claude (phase 4a ter) */
            attribute :>> marche_sol_plat = Niveau_marche_sol_plat::n0_6;
            attribute :>> sol_irregulier = Niveau_sol_irregulier::n2;
            attribute :>> pente = Niveau_pente::n5;
            attribute :>> releve = (Niveau_releve::depuis_le_dos, Niveau_releve::depuis_le_ventre);
            attribute :>> saut_vertical = Niveau_saut_vertical::n5;
            attribute :>> gestes_pointage = Niveau_gestes_pointage::n2_0;
            attribute :>> saisie = Niveau_saisie::n0_2;
            attribute :>> poussee = Niveau_poussee::n20;
            attribute :>> buste = Niveau_buste::lacet_seul;
            attribute :>> tete = Niveau_tete::n2;
            attribute :>> visage = Niveau_visage::ecran;
            attribute :>> autonomie = Niveau_autonomie::n30;
            attribute :>> ia_embarquee = Niveau_ia_embarquee::plus_vision;
        }
        part def YXOR_Home :> ModeleYXOR {
            doc /* modèle décidé (fiche 0073) ; capacités et niveaux À DÉFINIR avec Jeremy */
            // capacités À DÉFINIR avec Jeremy
        }
        part def YXOR_Pro :> ModeleYXOR {
            doc /* fiche 0069 (capacités cochées par Jeremy le 2026-10-04) ; « YXOR Pro remplace ce que nous appelions YXOR final » (Jeremy, 2026-10-08, fiche 0073) ; niveaux à balayer en phase 4b */
            // marche_sol_plat : niveau à balayer (phase 4b)
            // sol_irregulier : niveau à balayer (phase 4b)
            // pente : niveau à balayer (phase 4b)
            // releve : niveau à balayer (phase 4b)
            // course : niveau à balayer (phase 4b)
            // saut_vertical : niveau à balayer (phase 4b)
            // gestes_pointage : niveau à balayer (phase 4b)
            // saisie : niveau à balayer (phase 4b)
            // charge_lourde : niveau à balayer (phase 4b)
            // poussee : niveau à balayer (phase 4b)
            // mains_a_doigts : niveau à balayer (phase 4b)
            attribute :>> buste = Niveau_buste::lacet_plus_roulis_plus_tangage;
            // tete : niveau à balayer (phase 4b)
            // visage : niveau à balayer (phase 4b)
            attribute :>> autonomie = Niveau_autonomie::n60;
            attribute :>> ia_embarquee = Niveau_ia_embarquee::plus_modele_de_langage_local;
        }
        variation part def Gamme {
            doc /* Les quatre modèles de la gamme (fiche 0073). */
            variant part kit : YXOR_Kit;
            variant part lab : YXOR_Lab;
            variant part home : YXOR_Home;
            variant part pro : YXOR_Pro;
        }
    }

    // ── Exigences chiffrées du profil lab, à H = 0.6 m (anthropometry.yaml, tailles.S) ──
    package ExigencesLab {
        private import ScalarValues::*;
        requirement def CoupleArticulation {
            doc /* Couple de POINTE requis : τ ≥ a·M + b pour chaque tâche (M, masse du robot, en kg ;
                   a en N·m/kg, b en N·m) ; la marge de la fiche 0051 s'applique en plus. */
            attribute a : Real;
            attribute b : Real;
        }
        requirement couple_ankle_pitch_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe ankle_pitch. */
            attribute :>> a = 0.222551;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_roll_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe ankle_roll. */
            attribute :>> a = 0.0774909;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_pitch_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe hip_pitch. */
            attribute :>> a = 0.788385;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_roll_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe hip_roll. */
            attribute :>> a = 0.499909;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_yaw_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe hip_yaw. */
            attribute :>> a = 0.541841;
            attribute :>> b = 0.0;
        }
        requirement couple_knee_marche_sol_plat_n0_6 : CoupleArticulation {
            doc /* capacité marche_sol_plat = 0.6 ; axe knee. */
            attribute :>> a = 0.840853;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_pitch_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe ankle_pitch. */
            attribute :>> a = 0.322334;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_roll_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe ankle_roll. */
            attribute :>> a = 0.128666;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_pitch_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe hip_pitch. */
            attribute :>> a = 0.354956;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_roll_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe hip_roll. */
            attribute :>> a = 0.239888;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_yaw_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe hip_yaw. */
            attribute :>> a = 0.0723489;
            attribute :>> b = 0.0;
        }
        requirement couple_knee_releve_depuis_le_dos : CoupleArticulation {
            doc /* capacité releve = depuis le dos ; axe knee. */
            attribute :>> a = 0.428707;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_pitch_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe ankle_pitch. */
            attribute :>> a = 0.322334;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_roll_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe ankle_roll. */
            attribute :>> a = 0.128666;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_pitch_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe hip_pitch. */
            attribute :>> a = 0.354956;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_roll_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe hip_roll. */
            attribute :>> a = 0.239888;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_yaw_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe hip_yaw. */
            attribute :>> a = 0.0723489;
            attribute :>> b = 0.0;
        }
        requirement couple_knee_releve_depuis_le_ventre : CoupleArticulation {
            doc /* capacité releve = depuis le ventre ; axe knee. */
            attribute :>> a = 0.428707;
            attribute :>> b = 0.0;
        }
        requirement couple_ankle_pitch_saut_vertical_n5 : CoupleArticulation {
            doc /* capacité saut_vertical = 5 ; axe ankle_pitch. */
            attribute :>> a = 0.412834;
            attribute :>> b = 0.0;
        }
        requirement couple_hip_pitch_saut_vertical_n5 : CoupleArticulation {
            doc /* capacité saut_vertical = 5 ; axe hip_pitch. */
            attribute :>> a = 0.548364;
            attribute :>> b = 0.0;
        }
        requirement couple_knee_saut_vertical_n5 : CoupleArticulation {
            doc /* capacité saut_vertical = 5 ; axe knee. */
            attribute :>> a = 0.784331;
            attribute :>> b = 0.0;
        }
        requirement couple_shoulder_pitch_gestes_pointage_n2_0 : CoupleArticulation {
            doc /* capacité gestes_pointage = 2.0 ; axe shoulder_pitch. */
            attribute :>> a = 0.111788;
            attribute :>> b = 0.0;
        }
        requirement def Autonomie {
            doc /* 1 cycle = 60 s : 40 s de marche sur sol plat au niveau du profil, puis 20 s debout immobile (posture tenue, couples de maintien) */
            attribute minutes : Real;
        }
        requirement autonomie_lab : Autonomie { attribute :>> minutes = 30; }
        requirement def IAEmbarquee {
            attribute niveau : String;
        }
        requirement ia_lab : IAEmbarquee { attribute :>> niveau = "+ vision"; }
    }

    // ── Traçabilité : chaque exigence de couple se rattache à son axe (dépendance exigence → axe) ──
    package Tracabilite {
        private import Axes::*;
        private import ExigencesLab::*;
        dependency ExigencesLab::couple_ankle_pitch_marche_sol_plat_n0_6 to Axes::ankle_pitch;
        dependency ExigencesLab::couple_hip_pitch_marche_sol_plat_n0_6 to Axes::hip_pitch;
        dependency ExigencesLab::couple_hip_roll_marche_sol_plat_n0_6 to Axes::hip_roll;
        dependency ExigencesLab::couple_hip_yaw_marche_sol_plat_n0_6 to Axes::hip_yaw;
        dependency ExigencesLab::couple_knee_marche_sol_plat_n0_6 to Axes::knee;
        dependency ExigencesLab::couple_ankle_pitch_releve_depuis_le_dos to Axes::ankle_pitch;
        dependency ExigencesLab::couple_hip_pitch_releve_depuis_le_dos to Axes::hip_pitch;
        dependency ExigencesLab::couple_hip_roll_releve_depuis_le_dos to Axes::hip_roll;
        dependency ExigencesLab::couple_hip_yaw_releve_depuis_le_dos to Axes::hip_yaw;
        dependency ExigencesLab::couple_knee_releve_depuis_le_dos to Axes::knee;
        dependency ExigencesLab::couple_ankle_pitch_releve_depuis_le_ventre to Axes::ankle_pitch;
        dependency ExigencesLab::couple_hip_pitch_releve_depuis_le_ventre to Axes::hip_pitch;
        dependency ExigencesLab::couple_hip_roll_releve_depuis_le_ventre to Axes::hip_roll;
        dependency ExigencesLab::couple_hip_yaw_releve_depuis_le_ventre to Axes::hip_yaw;
        dependency ExigencesLab::couple_knee_releve_depuis_le_ventre to Axes::knee;
        dependency ExigencesLab::couple_ankle_pitch_saut_vertical_n5 to Axes::ankle_pitch;
        dependency ExigencesLab::couple_hip_pitch_saut_vertical_n5 to Axes::hip_pitch;
        dependency ExigencesLab::couple_knee_saut_vertical_n5 to Axes::knee;
        dependency ExigencesLab::couple_shoulder_pitch_gestes_pointage_n2_0 to Axes::shoulder_pitch;
    }
}
