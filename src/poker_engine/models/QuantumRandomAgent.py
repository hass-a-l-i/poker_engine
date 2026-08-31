from poker_engine.objects.Card import Card
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.objects.Player import Player
from poker_engine.config.cfg import PokerSkeleton
import numpy as np
cfg = PokerSkeleton()


class QuantumRandomAgent(Player):
    def __init__(self, name: str, chips: int, hand: list[Card]) -> None:
        """create a random-action quantum-based poker player."""
        super().__init__(name, chips, hand)


    @staticmethod
    def quantum_randint(min_val, max_val):
        if min_val > max_val:
            raise ValueError("min_val must be <= max_val")
        if min_val == max_val:
            return min_val

        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        range_size = max_val - min_val + 1
        num_qubits = int(np.ceil(np.log2(range_size)))

        simulator = AerSimulator()

        while True:
            # superposition of possible choices with hadamards
            qc = QuantumCircuit(num_qubits, num_qubits)
            qc.h(range(num_qubits))  # Apply H gate to all qubits
            qc.measure(range(num_qubits), range(num_qubits))

            # run circuit
            result = simulator.run(qc, shots=1).result()
            counts = result.get_counts(qc)
            measured_str = list(counts.keys())[0]
            measured_int = int(measured_str, 2)

            if measured_int < range_size:
                return min_val + measured_int


    def decision(self,
                 legal_actions: list[int],
                 call:int,
                 min_raise: int = cfg.big_blind):
        if len(legal_actions) == 0:
            raise IllegalMoveError("No choices")
        idx = self.quantum_randint(0, len(legal_actions) - 1)
        choice = legal_actions[idx]
        action_name = cfg.actions_dict[choice]
        if action_name == "Bet":
            minimum = min(cfg.big_blind, self.chips)
            amount = self.quantum_randint(minimum, self.chips)
            return choice, amount
        if action_name == "Raise":
            minimum_raise = min_raise
            maximum_raise = self.chips - call
            if maximum_raise <= minimum_raise:
                amount = maximum_raise
            else:
                amount = self.quantum_randint(minimum_raise, maximum_raise)
            return choice, amount
        return choice, 0

