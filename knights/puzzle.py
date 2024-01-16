from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
 
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
        # Information about the problem structure:

    # Every persona can be a knave or a knight but not both
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),

    # If one is not a knave, then it's a knight
    Implication(Not(AKnave), AKnight), 

        # Information about the testcase (what the characters said)

    # A being a knight implies he tells the truth,
    # A being a knave implies he lies
    Implication(AKnave, Not(And(AKnave, AKnight))),
    Implication(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
        # Information about the problem structure:

    # Every persona can be a knave or a knight but not both
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),

    # If one is not a knave, then it's a knight    
    Implication(Not(AKnave), AKnight), 
    Implication(Not(BKnave), BKnight), 

       # Information about the testcase (what the characters said)

    # A says A and B are knaves    
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
        # Information about the problem structure:

    # Every persona can be a knave or a knight but not both
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),

    # If one is not a knave, then it's a knight     
    Implication(Not(AKnave), AKnight), 
    Implication(Not(BKnave), BKnight), 

       # Information about the testcase (what the characters said)

    # A says A and B are knaves  or A and B are knights
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # B says A is a knight and B, a knave; or A is a knave and B a knight
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
        # Information about the problem structure:

    # Every persona can be a knave or a knight but not both
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),
    And(Or(CKnave, CKnight), Not(And(CKnave, CKnight))),

    # If one is not a knave, then it's a knight   
    Implication(Not(AKnave), AKnight), 
    Implication(Not(BKnave), BKnight), 
    Implication(Not(CKnave), CKnight), 

       # Information about the testcase (what the characters said)

    # A says either "A ia a knight." or "A is a knave."
    Implication(AKnight, And(Or(AKnave, AKnight), Not(And(AKnave, AKnight)))),
    Implication(AKnave, Not(And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))))),

    # B says A said A is a knave
    # If B tells the truth then it could be a lie or truth that A is a knave depending on A 
    # but BOTH implications must hold
    Implication(BKnight, Implication(AKnight, AKnave)),
    Implication(BKnight, Implication(AKnave, AKnight)),
    #If B lies, then we negate the CONJUNCTION of the previous implications (with Demorgan: ~(P ^ Q) <-> ~P ∨ ~Q)
    Implication(BKnave, Or(Not(Implication(AKnight, AKnave)), Not(Implication(AKnave, Not(AKnave))))),

    # B says C is a knave
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),

    # C says A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
