import random


class Board:
    """
    Represents a Tic Tac Toe board.
    Attributes:
        board (list): A list representing the 3x3 Tic Tac Toe board.
    """

    def __init__(self):
        """Initializes the board with empty spaces."""
        self.board = [" " for _ in range(9)]  # 3x3 Tic Tac Toe board

    def print_board(self):
        """Prints the current state of the board."""
        for i in range(3):
            print("|".join(self.board[i * 3 : (i + 1) * 3]))
            if i < 2:
                print("-----")

    def make_move(self, position, symbol):
        """
        Attempts to place a symbol at the given position on the board.
        Args:
            position (int): The position to place the symbol (0-8).
            symbol (str): The symbol to place ('X' or 'O').
        Returns:
            bool: True if the move is valid and made; False otherwise.
        >>> board = Board()
        >>> board.make_move(0, 'X')
        True
        >>> board.make_move(0, 'O')
        False
        """
        if self.is_valid_move(position):
            self.board[position] = symbol
            return True
        return False

    def is_valid_move(self, position):
        """
        Checks if the move is valid (i.e., within the board and on an empty space).
        Args:
            position (int): The position to check.
        Returns:
            bool: True if the move is valid; False otherwise.
        >>> board = Board()
        >>> board.is_valid_move(0)
        True
        >>> board.is_valid_move(9)
        False
        """
        if 0 <= position <= 8:
            return self.board[position] == " "
        return False

    def check_winner(self, symbol):
        """
        Checks if the given symbol has won the game.
        Args:
            symbol (str): The symbol to check ('X' or 'O').
        Returns:
            bool: True if the symbol has won; False otherwise.
        """
        # Check all winning conditions
        for i in range(3):
            # Check rows and columns
            if (
                self.board[i * 3]
                == self.board[i * 3 + 1]
                == self.board[i * 3 + 2]
                == symbol
            ) or (self.board[i] == self.board[i + 3] == self.board[i + 6] == symbol):
                return True
        # Check diagonals
        if (self.board[0] == self.board[4] == self.board[8] == symbol) or (
            self.board[2] == self.board[4] == self.board[6] == symbol
        ):
            return True
        return False

    def is_full(self):
        """
        Checks if the board is full (no empty spaces left).
        Returns:
            bool: True if the board is full; False otherwise.
        >>> board = Board()
        >>> board.is_full()
        False
        """
        return " " not in self.board


class BasePlayer:
    """
    Represents a generic player in the Tic Tac Toe game.
    Attributes:
        symbol (str): The symbol assigned to the player ('X' or 'O').
    """

    def __init__(self, symbol):
        """Initializes the player with a symbol."""
        self.symbol = symbol

    def make_move(self, board):
        """
        Makes a move on the board. This method should be overridden in subclasses.
        Args:
            board (Board): The game board.
        """
        pass


class HumanPlayer(BasePlayer):
    """
    Represents a human player in the Tic Tac Toe game.
    """

    def make_move(self, board):
        """
        Prompts the human player to make a move.
        Args:
            board (Board): The game board.
        Returns:
            bool: True if the move is successful; False otherwise.
        """
        try:
            self.position = int(input(f"Player {self.symbol}, enter your move (0-8): "))
        except ValueError:
            return False
        return board.make_move(self.position, self.symbol)


class BotPlayer(BasePlayer):
    """
    Represents a bot player in the Tic Tac Toe game.
    """

    def make_move(self, board):
        """
        The bot makes a move on the board.
        Args:
            board (Board): The game board.
        Returns:
            bool: True if the move is successful; False otherwise.
        """
        valid_moves = [i for i in range(9) if board.is_valid_move(i)]
        print(f"Valid moves: {valid_moves}")
        self.position = random.choice(valid_moves)
        print(f"BotPlayer {self.symbol} chooses position {self.position}")
        return board.make_move(self.position, self.symbol)


class Game:
    """
    Represents the Tic Tac Toe game.
    Attributes:
        board (Board): The game board.
        player1 (Player): The first player.
        player2 (Player): The second player.
        current_player (Player): The player who has the current turn.
    """

    def __init__(self, player1, player2):
        """Initializes the game with two players."""
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def play(self):
        """
        Starts and manages the Tic Tac Toe game play.
        """
        while True:
            self.board.print_board()
            if not self.current_player.make_move(self.board):
                print("Invalid move, try again.")
                continue

            if self.board.check_winner(self.current_player.symbol):
                self.board.print_board()
                print(f"Player {self.current_player.symbol} wins!")
                break

            if self.board.is_full():
                self.board.print_board()
                print("It's a tie!")
                break

            self.switch_player()


if __name__ == "__main__":
    # To play the game
    num_human_players = input("How many human players? (1/2): ")
    player1 = HumanPlayer("X")
    player2 = BotPlayer("O")
    if num_human_players == "1":
        player2 = BotPlayer("O")
    elif num_human_players == "2":
        player2 = HumanPlayer("O")
    else:
        print("Invalid input, defaulting to 1 human player.")
    game = Game(player1, player2)
    game.play()
