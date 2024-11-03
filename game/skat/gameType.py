class GameType:
    CLUBS = "Clubs"
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    GRAND = "Grand"
    NULL = "Null"

    @staticmethod
    def is_suit_game(game_type):
        return game_type in [GameType.CLUBS, GameType.SPADES, GameType.HEARTS, GameType.DIAMONDS]

    @staticmethod
    def is_trump_game(game_type):
        return game_type in [GameType.GRAND] or GameType.is_suit_game(game_type)

    @staticmethod
    def is_null_game(game_type):
        return game_type == GameType.NULL
