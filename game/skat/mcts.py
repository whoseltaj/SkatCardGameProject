import math
import random
from copy import deepcopy
from collections import defaultdict

# Node class for MCTS with enhanced capabilities and state management
class Node:
    def __init__(self, state, parent=None):
        """Initialize a new node for MCTS."""
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.total_points = 0
        self.untried_actions = state.get_legal_moves()
        self.expanded_actions = set()
        self.state_cache = defaultdict(float)

    def is_fully_expanded(self):
        
        return len(self.untried_actions) == 0

    def best_child(self, exploration_weight=1.41):
        #Select the best child node using UCB1
        choices_weights = [
            (child.value / (child.visits + 1e-6)) +
            exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        #Expand the node by selecting an untried action and adding the resulting node as a child."""
        action = self.untried_actions.pop(0)
        self.expanded_actions.add(action)
        next_state = deepcopy(self.state)
        next_state.perform_move(action)
        child_node = Node(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        #Check if the current node represents a terminal state in the game.
        return self.state.is_terminal()

    def get_path(self):
        """Return the sequence of moves leading to this node."""
        path = []
        current = self
        while current.parent is not None:
            path.append(current.state.last_move)
            current = current.parent
        path.reverse()
        return path

# Enhanced MCTS class for running simulations and choosing optimal moves
class MCTS:
    def __init__(self, exploration_weight=1.41, max_depth=100):
        """Initialize the MCTS algorithm with exploration parameters."""
        self.exploration_weight = exploration_weight
        self.max_depth = max_depth
        self.state_cache = {}

    def select(self, node):
        #Select the most promising node using UCT until a non-terminal, non-fully expanded node is found."
        while not node.is_terminal_node() and node.is_fully_expanded():
            node = node.best_child(self.adjust_exploration_rate(node))
        return node

    def adjust_exploration_rate(self, node):
        """Dynamically adjust the exploration rate based on the game phase."""
        total_moves = sum(len(hand) for hand in node.state.cards_in_hand.values())
        if total_moves > 20:
            return self.exploration_weight * 1.2  # Early game: increase exploration
        elif 10 <= total_moves <= 20:
            return self.exploration_weight  # Mid game: standard exploration
        else:
            return self.exploration_weight * 0.8  # Late game: decrease exploration

    def simulate(self, node):
        #Simulate a game from the current node's state until a terminal state is reached or max depth.
        current_state = deepcopy(node.state)
        depth = 0
        while not current_state.is_terminal() and depth < self.max_depth:
            legal_moves = current_state.get_legal_moves()
            if legal_moves:
                move = self.rollout_policy(legal_moves, current_state)
                current_state.perform_move(move)
            depth += 1
        return current_state.get_reward()

    def rollout_policy(self, legal_moves, state):
        """Choose a move during rollout using a weighted random strategy."""
        if state in self.state_cache:
            return random.choice(legal_moves)
        move_weights = [self.evaluate_move(move, state) for move in legal_moves]
        self.state_cache[state] = True
        return random.choices(legal_moves, weights=move_weights, k=1)[0]

    def evaluate_move(self, move, state):
        #Evaluate a move's strategic importance during rollouts.
        suit, rank = move.split('-')
        weight = 1  # Base weight for any move
        if suit == state.trump_suit or rank == 'jack':
            weight += 5  # Higher weight for trump cards
        if rank in ['ace', '10']:
            weight += 3  # High value cards are prioritized
        if state.is_lead_move(move):
            weight += 2  # Leading with a strong card can be advantageous
        return weight

    def backpropagate(self, node, reward):
        #Backpropagate the result of a simulation up the tree, updating visits and value.
        while node:
            node.visits += 1
            node.value += reward
            node.total_points += reward
            reward = -reward  # Alternate perspective for the opponent
            node = node.parent

    def run(self, initial_state, itermax=1000):
        #Run the MCTS algorithm for a given number of iterations and return the best child.
        root = Node(initial_state)
        for _ in range(itermax):
            node = self.select(root)
            if not node.is_fully_expanded() and not node.is_terminal_node():
                node = node.expand()
            reward = self.simulate(node)
            self.backpropagate(node, reward)
        return root.best_child(0)

# SkatGameState class with comprehensive game logic and strategic enhancements
class SkatGameState:
    def __init__(self, current_player, cards_in_hand, trick_cards, score, trump_suit=None):
        """Initialize a Skat game state."""
        self.current_player = current_player
        self.cards_in_hand = cards_in_hand
        self.trick_cards = trick_cards
        self.score = score
        self.trump_suit = trump_suit
        self.tricks_won = {player: [] for player in cards_in_hand}
        self.last_move = None

    def get_legal_moves(self):
        #Return the list of legal moves for the current player.
        current_hand = self.cards_in_hand[self.current_player]
        if not self.trick_cards:
            return current_hand  # Any card can be played if the trick is empty
        lead_suit = self.trick_cards[0].split('-')[0]
        playable_cards = [card for card in current_hand if card.split('-')[0] == lead_suit]
        return playable_cards if playable_cards else current_hand  # Must follow suit if possible

    def perform_move(self, card):
        #Execute a move by the current player, updating the game state.
        self.trick_cards.append(card)
        self.cards_in_hand[self.current_player].remove(card)
        self.last_move = card
        if len(self.trick_cards) == 3:
            self.resolve_trick()

    def resolve_trick(self):
        #Determine the winner of the current trick and update the state accordingly.
        winning_card = max(self.trick_cards, key=self.card_strength)
        winner = (self.current_player + self.trick_cards.index(winning_card)) % 3
        self.tricks_won[winner].append(list(self.trick_cards))
        self.trick_cards = []
        self.current_player = winner

    def card_strength(self, card):
        #Evaluate the strength of a card, considering trump suit and rank.
        suit, rank = card.split('-')
        is_trump = suit == self.trump_suit or rank == 'jack'
        rank_order = ['jack', 'ace', '10', 'king', 'queen', '9', '8', '7'] if is_trump else ['ace', '10', 'king', 'queen', 'jack', '9', '8', '7']
        rank_index = rank_order.index(rank)
        return (1 if is_trump else 0, rank_index)

    def is_terminal(self):
        #Check if the game is in a terminal state (all cards have been played).
        return all(len(hand) == 0 for hand in self.cards_in_hand.values())

    def is_lead_move(self, card):
        #Check if a card is a lead move in a trick."""
        return len(self.trick_cards) == 0

    def get_reward(self):
        #Calculate the reward for the current game state, focusing on declarer's score."""
        declarer = 0  # For simplicity, assuming player 0 is the declarer
        declarer_points = sum(card_value(card) for trick in self.tricks_won[declarer] for card in trick)
        return 1 if declarer_points >= 61 else -1  # Declarer wins if points >= 61

    def get_tricks_cards(self, player):
        #Return all cards won by a specific player."""
        return [card for trick in self.tricks_won[player] for card in trick] if self.tricks_won[player] else []

# Helper function to evaluate card value
def card_value(card):
    """Return the value of a card for scoring purposes."""
    rank = card.split('-')[1]
    return {
        'jack': 2,
        'ace': 11,
        '10': 10,
        'king': 4,
        'queen': 3
    }.get(rank, 0)
