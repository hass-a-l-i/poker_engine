import inspect

game_rules = """
             Welcome to Texas Hold-Em' Poker!
             -------------------------------------
             Rules:
             Type '1' to Check.
             Type '2' to Call.
             Type '3' to Bet.
             Type '4' to Fold.
             """

game_rules = inspect.cleandoc(game_rules)

suits:list[str] = ['S', 'D', 'C', 'H']
ranks:list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order:dict = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}

start_deck:list[str] = [i + j for i in suits for j in ranks]

actions_dict = {1: "Check", 2: "Call", 3: "Bet", 4: "Fold"}

# rank_order_A_high:dict = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}
# rank_order_A_low = {str(rank): idx + 1 for idx, rank in enumerate(ranks_A_low)}