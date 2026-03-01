# import numpy as np
# from numpy.typing import NDArray

suits:list[str] = ['S', 'D', 'C', 'H']
ranks:list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_order:dict = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}

start_deck:list[str] = [i + j for i in suits for j in ranks]

# rank_order_A_high:dict = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}
# rank_order_A_low = {str(rank): idx + 1 for idx, rank in enumerate(ranks_A_low)}