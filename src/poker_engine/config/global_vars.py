import numpy as np
from numpy.typing import NDArray

suits:NDArray[np.str_] = np.array(['S', 'D', 'C', 'H'])
ranks:NDArray[np.str_] = np.array(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
rank_order:dict = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}

start_deck:NDArray[np.integer] = np.array([i + j for i in suits for j in ranks])

# ranks_A_low = np.array(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
# ranks_A_low_order = {str(rank): idx + 1 for idx, rank in enumerate(ranks_A_low)}