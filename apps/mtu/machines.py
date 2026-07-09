"""Opérations comme VRAIES machines de Turing.  COMPLÉTER : tables ADD, SUB.
-> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine
ADD = TuringMachine(
    transitions={
        #avancer jusqu'au +, le remplacer par 1
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "+"): ("q1", "1", "R"),
        #avancer jusqu'à la fin
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q2", "_", "L"),
        #effacer le dernier 1
        ("q2", "1"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)
SUB = TuringMachine(
    transitions={
        # Marquer un 1 de m avec X, aller chercher un 1 de n
        ("q0", "1"): ("q1", "X", "R"),
        ("q0", "X"): ("q0", "X", "R"),
        ("q0", "-"): ("q_clean", "-", "L"),   # m épuisé

        # Traverser jusqu'à n
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "X"): ("q1", "X", "R"),
        ("q1", "-"): ("q2", "-", "R"),

        # Marquer un 1 de n avec X
        ("q2", "X"): ("q2", "X", "R"),
        ("q2", "1"): ("q3", "X", "L"),
        ("q2", "_"): ("q_back", "_", "L"),    # n épuisé avant m

        # Revenir au début
        ("q3", "X"): ("q3", "X", "L"),
        ("q3", "1"): ("q3", "1", "L"),
        ("q3", "-"): ("q3", "-", "L"),
        ("q3", "_"): ("q0", "_", "R"),

        # n épuisé : traverser X de n et - pour trouver le dernier X de m
        ("q_back", "X"): ("q_back", "X", "L"),
        ("q_back", "-"): ("q_back2", "-", "L"),

        # Remettre le dernier X de m en 1
        ("q_back2", "1"): ("q_back2", "1", "L"),
        ("q_back2", "X"): ("q_undo", "1", "L"),

        # Effacer les X de m restants (consommés)
        ("q_undo", "X"): ("q_undo", "_", "L"),
        ("q_undo", "1"): ("q_undo", "1", "L"),
        ("q_undo", "_"): ("q_fwd", "_", "R"),

        # Avancer : garder 1, effacer X de m et -
        ("q_fwd", "1"): ("q_fwd", "1", "R"),
        ("q_fwd", "X"): ("q_fwd", "_", "R"),
        ("q_fwd", "_"): ("q_fwd", "_", "R"),
        ("q_fwd", "-"): ("q_fwd2", "_", "R"),

        # Effacer X de n
        ("q_fwd2", "X"): ("q_fwd2", "_", "R"),
        ("q_fwd2", "1"): ("q_fwd2", "_", "R"),
        ("q_fwd2", "_"): ("qf", "_", "S"),

        # m épuisé : tout effacer
        ("q_clean", "X"): ("q_clean", "X", "L"),
        ("q_clean", "_"): ("q_clean2", "_", "R"),
        ("q_clean2", "X"): ("q_clean2", "_", "R"),
        ("q_clean2", "-"): ("q_clean2", "_", "R"),
        ("q_clean2", "1"): ("q_clean2", "_", "R"),
        ("q_clean2", "_"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)

# Bonus (E3.6 / Jour 4) : table MONOLITHIQUE de multiplication 1^m * 1^n = -> 1^(m*n)
# Format ruban : 1^m * 1^n =
#
# Principe (une seule table, pas de composition d'ADD) :
#   - q0/q1  : chercher, dans le bloc m, un 1 non marqué -> le marquer X.
#   - q2..q5 : pour ce X, parcourir le bloc n et, pour chaque 1 non marqué (marqué
#              Y le temps du tour), écrire un 1 tout à la fin du ruban (le résultat
#              R s'accumule après le "=") ; une fois le bloc n épuisé (tous Y),
#              on démarque les Y (retour à 1) et on reprend un nouveau X dans m.
#   - qclean : quand m est épuisé (plus de 1 non marqué, on lit "*"), on efface le
#              bloc n et le "=", on convertit les marqueurs de résultat R en 1,
#              puis on efface les marqueurs X et "*" restants avant de s'arrêter en qf.
MUL = TuringMachine(
    transitions={
        # q0 : trouver 1 non marqué de m, le marquer X
        ("q0", "1"): ("q1", "X", "R"),
        ("q0", "X"): ("q0", "X", "R"),
        ("q0", "*"): ("qclean", "*", "R"),   # m épuisé : nettoyer

        # q1 : aller après * pour trouver n
        ("q1", "X"): ("q1", "X", "R"),
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "*"): ("q2", "*", "R"),

        # q2 : marquer un 1 de n avec Y, l'écrire dans résultat
        ("q2", "Y"): ("q2", "Y", "R"),
        ("q2", "1"): ("q3", "Y", "R"),
        ("q2", "="): ("q5", "=", "L"),       # n épuisé ce tour

        # q3 : aller à la fin du résultat (après =) et écrire R
        ("q3", "Y"): ("q3", "Y", "R"),
        ("q3", "1"): ("q3", "1", "R"),
        ("q3", "="): ("q3", "=", "R"),
        ("q3", "R"): ("q3", "R", "R"),
        ("q3", "_"): ("q4", "R", "L"),

        # q4 : revenir au Y pour continuer la copie de n
        ("q4", "R"): ("q4", "R", "L"),
        ("q4", "="): ("q4", "=", "L"),
        ("q4", "1"): ("q4", "1", "L"),
        ("q4", "Y"): ("q2", "Y", "R"),

        # q5 : remettre Y en 1, revenir à q0
        ("q5", "Y"): ("q5", "1", "L"),
        ("q5", "*"): ("q5", "*", "L"),
        ("q5", "1"): ("q5", "1", "L"),
        ("q5", "X"): ("q0", "X", "R"),

        # qclean : effacer n, =, convertir R en 1
        ("qclean", "1"): ("qclean", "_", "R"),
        ("qclean", "Y"): ("qclean", "_", "R"),
        ("qclean", "="): ("qclean", "_", "R"),
        ("qclean", "R"): ("qclean", "1", "R"),
        ("qclean", "_"): ("qclean2", "_", "L"),

        # qclean2 : revenir à gauche, effacer X et *
        ("qclean2", "1"): ("qclean2", "1", "L"),
        ("qclean2", "_"): ("qclean2", "_", "L"),
        ("qclean2", "*"): ("qclean3", "_", "L"),   # on passe le "*" : bloc X (ou rien si m=0)
        ("qclean2", "R"): ("qclean2", "1", "L"),
        ("qclean2", "="): ("qclean2", "_", "L"),

        # qclean3 : on est juste après le "*" ; s'il reste des X (m>0), on les
        # efface un à un ; dès qu'on retombe sur un blanc "vierge" (jamais écrit,
        # y compris tout de suite si m=0), le bloc m est entièrement effacé -> halte.
        ("qclean3", "X"): ("qclean3", "_", "L"),
        ("qclean3", "_"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)