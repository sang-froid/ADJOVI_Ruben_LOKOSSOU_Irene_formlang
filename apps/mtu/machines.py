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