# Author: Charles Beise
# Date: 8/9/2021
# Description: This program is a playable version of the game Quoridor. This is a game for 2 players which is played
# on an 9x9 board. Both players have one pawn which is placed on the center space of opposite sides of the board. The
# players then take turns either moving their pawn one space or playing a fence, of which each player has 10. The game
# continues until one player's pawn has reached the opposite side of the board.

class QuoridorGame:
    """This class is a playable version of the game Quoridor. It contains the necessary methods to move a pawn and place
    a fence. It also contains several methods to assist with gameplay (e.g. checking to see if a player has won,
    checking to see if a move is valid, tracking the fences placed on the board, tracking the number of fences each
    player has remaining)"""

    def __init__(self):
        """This initializes the necessary data members of the QuoridorGame class"""
        self._game_over = False
        self._winner = None
        self._P1 = Player((4, 0))
        self._P2 = Player((4, 8))
        self._turn = self._P1
        # This list will always contain the two spaces occupied by the two players' pawns
        self._occupied_spaces = [(4, 0), (4, 8)]
        # This dictionary contains the list of fences currently in play. It is initialized by stating the top and left
        # sides of the board are lined with fences.
        self._fences = {'v': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)],
                        'h': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]}

    def move_pawn(self, player, destination):
        """This method is used when a player makes a move. It checks if the move is valid and makes the necessary
        updates if the move is valid. This method calls is_game_over, check_turn, check_tuple, check_boundaries,
        is_valid_move, check_obstacles, acutally_make_move, check_winner, and next_turn"""
        # Check to see if the game has already been won
        if self.is_game_over() is True:
            return False
        # Check to see if it is this player's turn
        elif self.check_turn(player) is False:
            return False
        # Check to make sure the coordinates entered are a tuple of 2 integers
        elif self.check_tuple(destination) is False:
            return False
        # Check to see if the entered coordinates are outside the playing area
        elif self.check_boundaries(destination) is True:
            return False
        # Check to see if the move is valid (i.e. one space orthogonally, or a valid jump, or a valid diagonal move)
        elif self.is_valid_move(player, destination) is False:
            return False
        # Check to see if a fence is blocking the move or the opponent's piece is in the desired destination
        elif self.check_obstacles(player, destination) is True:
            return False
        # If all the checks are passed, the move is actually made
        else:
            self.actually_move_pawn(player, destination)
            self.check_winner(player)
            self.next_turn()
            return True

    def actually_move_pawn(self, player, destination):
        """If the move passes all the 'move_pawn' checks, then the move is made and the necessary modifications
         are made. This method calls update_unoccupied_spaces and set_location"""
        self.update_occupied_spaces(player, destination)
        if player == 1:
            self._P1.set_location(destination)
        else:
            self._P2.set_location(destination)

    def is_valid_move(self, player, destination):
        """This method checks to see if a move is valid (i.e. one space orthogonally, or a valid jump, or a valid
        diagonal move). This method calls get_location, check_vertical_move, check_horizontal_move, and
        check_diagonal_move"""
        if player == 1:
            old_space = self._P1.get_location()
        else:
            old_space = self._P2.get_location()
        # Check if the movement is vertical
        if old_space[0] == destination[0]:
            return self.check_vertical_move(old_space, destination)
        # Check if the movement is horizontal
        elif old_space[1] == destination[1]:
            return self.check_horizontal_move(old_space, destination)
        # Check if the move is diagonal
        else:
            if self.check_diagonal_move(old_space, destination) is True:
                return False

    def check_vertical_move(self, old_space, destination):
        """This method is called if the player is moving a piece in a vertical direction. Returns True if the move is
        valid. This method calls check_if_valid_jump"""
        if old_space[1] == (destination[1] + 1):
            return True
        elif old_space[1] == (destination[1] - 1):
            return True
        elif old_space[1] == (destination[1] + 2):
            middle_space = (old_space[0], old_space[1] - 1)
            return self.check_if_valid_jump(middle_space, destination)
        elif old_space[1] == (destination[1] - 2):
            middle_space = (old_space[0], old_space[1] + 1)
            return self.check_if_valid_jump(middle_space, destination)
        else:
            return False

    def check_horizontal_move(self, old_space, destination):
        """This method is called if the player is moving a piece in a vertical direction. Returns True if the move is
        valid. This method calls check_if_valid_jump"""
        if old_space[0] == (destination[0] + 1):
            return True
        elif old_space[0] == (destination[0] - 1):
            return True
        elif old_space[0] == (destination[0] + 2):
            middle_space = (old_space[0] + 1, old_space[1])
            return self.check_if_valid_jump(middle_space, destination)
        elif old_space[0] == (destination[0] - 2):
            middle_space = (old_space[0] - 1, old_space[1])
            return self.check_if_valid_jump(middle_space, destination)
        else:
            return False

    def check_diagonal_move(self, old_space, destination):
        """This method only gets called when a piece is not moving orthogonally. Checks to see if the piece is making
        a valid diagonal move. If the move is ILLEGAL return True. This method calls check_diagonal_fence."""
        # Create locations for adjacent spaces
        right = (old_space[0] + 1, old_space[1])
        left = (old_space[0] - 1, old_space[1])
        up = (old_space[0], old_space[1] - 1)
        down = (old_space[0], old_space[1] + 1)
        # Move is down and right
        if destination == (old_space[0] + 1, old_space[1] + 1):
            return self.check_diagonal_fence(destination, down, right, "DR")
        # Move is down and left
        elif destination == (old_space[0] - 1, old_space[1] + 1):
            return self.check_diagonal_fence(destination, down, left, "DL")
        # Move is up and right
        elif destination == (old_space[0] + 1, old_space[1] - 1):
            return self.check_diagonal_fence(destination, up, right, "UR")
        # Move is up and left
        elif destination == (old_space[0] - 1, old_space[1] - 1):
            return self.check_diagonal_fence(destination, up, left, "UL")
        # Move is more than one space diagonally, or not straight diagonally, or opponent's piece is not adjacent
        else:
            return True

    def check_diagonal_fence(self, destination, adjacent_1, adjacent_2, direction):
        """This method is used to check if a diagonal move down and to the right is valid. If the move is illegal,
        returns True. This method calls check_for_fence"""
        if adjacent_1 in self._occupied_spaces:
            if direction[0] == 'D':
                target_space = (adjacent_1[0], adjacent_1[1] + 1)
            else:
                target_space = (adjacent_1[0], adjacent_1[1] - 1)
            # If the player is able to jump the opponent's piece, then there is no fence blocking the jump and therefore
            # a diagonal move is not allowed
            if self.check_if_valid_jump(adjacent_1, target_space) is True:
                return True
            return self.check_for_fence(adjacent_1, destination)
        elif adjacent_2 in self._occupied_spaces:
            if direction[1] == 'R':
                target_space = (adjacent_1[0] + 1, adjacent_1[1])
            else:
                target_space = (adjacent_1[0] - 1, adjacent_1[1])
            # If the player is able to jump the opponent's piece, then there is no fence blocking the jump and therefore
            # a diagonal move is not allowed
            if self.check_if_valid_jump(adjacent_2, target_space) is True:
                return True
            return self.check_for_fence(adjacent_2, destination)
        else:
            return True

    def check_if_valid_jump(self, middle_space, destination):
        """This method checks to see if the player is making a valid jump. If the jump is valid, returns True. This
        method calls check_for_fence"""
        if middle_space in self._occupied_spaces:
            # check_for_fence returns True if there is a fence blocking the move
            if self.check_for_fence(middle_space, destination) is False:
                return True
            else:
                return False
        else:
            return False

    def check_obstacles(self, player, destination):
        """Checks to see if a fence is blocking the move or the opponent's piece is in the desired destination. If the
        move is blocked by either, returns True. This method calls get_location and check_for_fence"""
        # Check to see if the opponent's piece is in the desired destination or the destination is the current
        # player's current space (i.e. staying in the same space)
        if destination in self._occupied_spaces:
            return True
        # If player 1 is making the move sets the originating location the their current position, otherwise sets it to
        # player 2's location
        elif player == 1:
            old_space = self._P1.get_location()
        else:
            old_space = self._P2.get_location()
        return self.check_for_fence(old_space, destination)

    def check_for_fence(self, old_space, destination):
        """Checks to see if a fence is blocking the move. If a fence is blocking the move, returns True"""
        # If the player is moving vertically
        if old_space[0] == destination[0]:
            # If the player is moving up
            if old_space[1] > destination[1]:
                return old_space in self._fences['h']
            # If the player is moving down
            else:
                return (old_space[0], old_space[1] + 1) in self._fences['h']
        # If the player is moving horizontally
        else:
            # If the player is moving left
            if old_space[0] > destination[0]:
                return old_space in self._fences['v']
            # If the player is moving right
            else:
                return (old_space[0] + 1, old_space[1]) in self._fences['v']

    def update_occupied_spaces(self, player, destination):
        """This method updates the two spaces occupied by the players' pawns. This method calls get_location"""
        if player == 1:
            old_space = self._P1.get_location()
        else:
            old_space = self._P2.get_location()
        self._occupied_spaces.remove(old_space)
        self._occupied_spaces.append(destination)

    def place_fence(self, player, direction, location):
        """This method is used when a player places a fence. It checks if the fence placement is valid and if so, places
        a new fence in that position and reduces that player's available fences by 1. This method calls is_game_over,
        check_turn, check_tuple, check_fence, check_boundaries, check_player_fences, and actually_place_fence"""
        # Check to see if the game has already been won
        if self.is_game_over() is True:
            return False
        # Check to see if it is this player's turn
        elif self.check_turn(player) is False:
            return False
        # Check to make sure the coordinates entered are a tuple of 2 integers
        elif self.check_tuple(location) is False:
            return False
        # Check to see if there is already a fence at this location
        elif self.check_fence(direction, location) is True:
            return False
        # Check to see if the entered coordinates are outside the playing area
        elif self.check_boundaries(location) is True:
            return False
        else:
            # Check to see if the player has any fences left
            fence_list = self.check_player_fences(player)
            if fence_list["available"] == 0:
                return False
            # If all the checks are passed, then the fence is placed and the player's fence count is adjusted
            else:
                self.actually_place_fence(player, direction, location)
                return True

    def actually_place_fence(self, player, direction, location):
        """If the fence placement passes all the 'place_fence' checks, then the fence is played and the necessary
        modifications are made. This method calls play_fence and next_turn"""
        # Add the new fence to the fence list associated with the directional key (key:value == direction:fence list)
        self._fences[direction].append(location)
        # Reduces the player's available fences by 1
        if player == 1:
            self._P1.play_fence()
        else:
            self._P2.play_fence()
        # Changes whose turn it is to play to the next player
        self.next_turn()
        return True

    def check_turn(self, player):
        """This method checks to see if it is the entered player's turn. If it is their turn, return True"""
        # If player 1 is trying to make a move
        if player == 1:
            if self._turn == self._P1:
                return True
            else:
                return False
        # If player 2 is trying to make a move
        elif self._turn == self._P2:
            return True
        else:
            return False

    def next_turn(self):
        """This method changes the current player's turn once a valid move is made"""
        if self._turn == self._P1:
            self._turn = self._P2
        else:
            self._turn = self._P1

    def check_boundaries(self, location):
        """This method checks to see if the entered coordinates are outside the playing area. If the coordinates are
        outside the playing area, return True"""
        if 0 > location[0] or location[0] > 8:
            return True
        elif 0 > location[1] or location[1] > 8:
            return True
        else:
            return False

    def check_tuple(self, coordinates):
        """This method checks to see if the coordinates entered are a tuple of 2 integers. If so, returns True.
        Returns False otherwise"""
        if type(coordinates[0]) != int:
            return False
        elif type(coordinates[1]) != int:
            return False
        else:
            return True

    def check_player_fences(self, player):
        """This method is used to check if the player has any available fences remaining. This method calls
        get_fences"""
        if player == 1:
            return self._P1.get_fences()
        else:
            return self._P2.get_fences()

    def check_winner(self, player):
        """This method checks to see if the entered player has won (i.e. reached the opponent's baseline). This
        method calls get_location and end_game"""
        if player == 1:
            location = self._P1.get_location()
            # If Player 1 has reached Player 2's baseline
            if location[1] == 8:
                self.end_game("P1")
                return True
            else:
                return False
        else:
            location = self._P2.get_location()
            # If Player 2 has reached Player 1's baseline
            if location[1] == 0:
                self.end_game("P2")
                return True
            else:
                return False

    def end_game(self, winner):
        """This method is called once a player makes a winning move. It ends the game and sets the winner"""
        self._game_over = True
        if winner == "P1":
            self._winner = self._P1
        else:
            self._winner = self._P2

    def is_game_over(self):
        """Checks to see if the game has been won"""
        return self._game_over

    def is_winner(self, player):
        """This method is used to determine if a player has won"""
        if player == 1:
            player_id = self._P1
        else:
            player_id = self._P2
        if self._winner == player_id:
            return True
        else:
            return False

    def check_fence(self, direction, location):
        """This method checks to see if there is already a fence at the given location. If there is already a fence
        there, return True"""
        return location in self._fences[direction]

    def get_location(self, player):
        """Takes a player as a parameter and returns the location of the pawn. This method calls get_location"""
        if player == 1:
            return self._P1.get_location()
        else:
            return self._P2.get_location()


class Player:
    """This class will be used to create a Player object"""

    def __init__(self, location):
        """This initializes the necessary data members of the Player object"""
        self._fences = {"available": 10, "played": 0}
        self._location = location

    def get_location(self):
        """Returns the current location of the Player's pawn"""
        return self._location

    def set_location(self, location):
        """This method takes a location on the board as a parameter and sets that location as this player's pawn's
        current position"""
        self._location = location

    def get_fences(self):
        """Returns the dictionary containint how many fences the Player has available and how many fences the player
        has already played"""
        return self._fences

    def play_fence(self):
        """This method is called when the Player plays a fence. The amount of available fences is reduced by 1 and the
        amount of fences played is increased by 1"""
        self._fences["available"] -= 1
        self._fences["played"] += 1
