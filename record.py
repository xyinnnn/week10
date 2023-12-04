from lib import *
from pprint import pprint

import pandas as pd
    

"""
record game play data
data = {
    "game_id": "", # 0
    "move_count": "", # 8
    "first_move": "", # 2 
    "first_move_position:: "" # center/middle/corner
    "winner: "", # X/O/draw
    "result": "", # win/loss/draw
}
"""

game_data = []
position_category = {0 : 'corner', 
                     1 : 'middle', 
                     2 : 'corner', 
                     3 : 'middle', 
                     4 : 'center', 
                     5 : 'middle', 
                     6 : 'corner', 
                     7 : 'middle', 
                     8 : 'corner'}
# 30 games
for x in range(30):
    game_id = x
    move_count = 0
    data = {}
    # To play the game
    num_human_players = input("How many human players? (0/1/2): ")
    player1 = HumanPlayer("X")
    player2 = BotPlayer("O")
    if num_human_players == "0":
        player1 = BotPlayer("X")
    elif num_human_players == "1":
        player2 = BotPlayer("O")
    elif num_human_players == "2":
        player2 = HumanPlayer("O")
    else:
        print("Invalid input, defaulting to 0 human player.")
    game = Game(player1, player2)
    data['game_id'] = game_id
    while True:
        move_count += 1
        game.board.print_board()
        if not game.current_player.make_move(game.board):
            print("Invalid move, try again.")
            continue
        
        if move_count == 1:
            data['first_move'] = game.current_player.position
            data['first_move_position'] = position_category[game.current_player.position]
        
        if game.board.check_winner(game.current_player.symbol):
            game.board.print_board()
            print(f"Player {game.current_player.symbol} wins!")
            data['winner'] = game.current_player.symbol
            data['result'] = 'win' if game.current_player.symbol == 'X' else 'loss'
            data['move_count'] = move_count
            break

        if game.board.is_full():
            game.board.print_board()
            print("It's a tie!")
            data['winner'] = "draw"
            data['result'] = "draw"
            data['move_count'] = move_count
            break

        game.switch_player()

    game_data.append(data)

pprint(game_data)
pd.DataFrame(game_data).to_csv("./logs/database.csv")
