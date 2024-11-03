import math
import random
from copy import deepcopy


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.total_points = 0
        self.untried_actions = state.get_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, exploration_weight=1.41):
        # Use UCT (Upper Confidence Bound for Trees) with added considerations
        choices_weights = [
            (child.value / (child.visits + 1e-6)) +
            exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        action = self.untried_actions.pop(0)
        next_state = deepcopy(self.state)
        next_state.perform_move(action)
        child_node = Node(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_terminal()

# Enhanced MCTS class with dynamic exploration and advanced simulation strategies
class MCTS:
    def __init__(self, exploration_weight=1.41, max_depth=100):
        self.exploration_weight = exploration_weight
        self.max_depth = max_depth

    def select(self, node):
        # Select the most promising node using UCT
        while not node.is_terminal_node() and node.is_fully_expanded():
            node = node.best_child(self.adjust_exploration_rate(node))
        return node

    def adjust_exploration_rate(self, node):
        # Adjust exploration rate based on game phase (early vs. late)
        total_moves = sum(len(hand) for hand in node.state.cards_in_hand.values())
        if total_moves > 20:
            return self.exploration_weight * 1.2  # Increase exploration in early game
        elif 10 <= total_moves <= 20:
            return self.exploration_weight
        else:
            return self.exploration_weight * 0.8  # Decrease exploration in late game

    def simulate(self, node):
        # Simulate a game using an advanced strategic approach
        current_state = deepcopy(node.state)
        depth = 0
        while not current_state.is_terminal() and depth < self.max_depth:
            legal_moves = current_state.get_legal_moves()
            if legal_moves:
                move = self.weighted_move_selection(legal_moves, current_state)
                current_state.perform_move(move)
            depth += 1
        return current_state.get_reward()

    def weighted_move_selection(self, legal_moves, state):
        # Weight moves based on their strategic value, prioritize trumps, and high points
        move_weights = []
        for move in legal_moves:
            suit, rank = move.split('-')
            weight = 1  # Base weight for any move
            if suit == state.trump_suit or rank == 'jack':
                weight += 5  # Prioritize trump cards
            if rank in ['ace', '10']:
                weight += 3  # High point cards
            move_weights.append(weight)
        return random.choices(legal_moves, weights=move_weights, k=1)[0]

    def backpropagate(self, node, reward):
        # Propagate the simulation result up the tree, considering total points for better insight
        while node:
            node.visits += 1
            node.value += reward
            node.total_points += reward  # Track cumulative points for the node
            reward = -reward  # Alternate reward for opposing perspectives
            node = node.parent

    def run(self, initial_state, itermax=1000):
        root = Node(initial_state)
        for _ in range(itermax):
            node = self.select(root)
            if not node.is_fully_expanded() and not node.is_terminal_node():
                node = node.expand()
            reward = self.simulate(node)
            self.backpropagate(node, reward)
        return root.best_child(0)  # Return the best child with highest value for decision-making

# Enhanced SkatGameState class with improved evaluation methods and detailed game logic
class SkatGameState:
    def __init__(self, current_player, cards_in_hand, trick_cards, score, trump_suit=None):
        self.current_player = current_player
        self.cards_in_hand = cards_in_hand  # {player_id: [cards]}
        self.trick_cards = trick_cards  # Cards played in current trick
        self.score = score  # {player_id: score}
        self.trump_suit = trump_suit
        self.tricks_won = {player: 0 for player in cards_in_hand}

    def get_legal_moves(self):
        current_hand = self.cards_in_hand[self.current_player]
        if not self.trick_cards:
            return current_hand
        lead_suit = self.trick_cards[0].split('-')[0]
        playable_cards = [card for card in current_hand if card.split('-')[0] == lead_suit]
        return playable_cards if playable_cards else current_hand

    def perform_move(self, card):
        self.trick_cards.append(card)
        self.cards_in_hand[self.current_player].remove(card)
        if len(self.trick_cards) == 3:
            self.resolve_trick()

    def resolve_trick(self):
        winning_card = max(self.trick_cards, key=self.card_strength)
        winner = (self.current_player + self.trick_cards.index(winning_card)) % 3
        self.tricks_won[winner] += 1
        self.trick_cards = []
        self.current_player = winner

    def card_strength(self, card):
        suit, rank = card.split('-')
        is_trump = suit == self.trump_suit or rank == 'jack'
        rank_order = ['jack', 'ace', '10', 'king', 'queen', '9', '8', '7'] if is_trump else ['ace', '10', 'king', 'queen', 'jack', '9', '8', '7']
        rank_index = rank_order.index(rank)
        return (1 if is_trump else 0, rank_index)

    def is_terminal(self):
        return all(len(hand) == 0 for hand in self.cards_in_hand.values())

    def get_reward(self):
        declarer = 0  # Assuming player 0 is the declarer for demonstration
        declarer_points = sum(card_value(card) for card in self.get_tricks_cards(declarer))
        if declarer_points >= 61:
            return 1  # Declarer wins
        else:
            return -1  # Defenders win

    def get_tricks_cards(self, player):
        # Get cards won by a player in tricks
        return [card for trick in self.tricks_won[player] for card in trick] if self.tricks_won[player] > 0 else []

# Helper function to evaluate card value (e.g., Aces and 10s score high)
def card_value(card):
    rank = card.split('-')[1]
    if rank == 'jack':
        return 2
    elif rank == 'ace':
        return 11
    elif rank == '10':
        return 10
    elif rank == 'king':
        return 4
    elif rank == 'queen':
        return 3
    else:
        return 0
