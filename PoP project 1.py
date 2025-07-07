# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def ship_type(ship):
  if ship[0] == "D" or ship[0] == "destroyer":
    return ('destroyer')
  if ship[0] == "C" or ship[0] == "carrier":
    return ('carrier')

  #ship_type(ship) returns a string that is the type of the given ship ship, e.g., "destroyer", where ship is a tuple of the form (type, squares, hits) (see Data structures)
  #tuple should read D and output destroyer etc.

def ship_from_input(type_inp, rotation_inp, anchor_inp):

  sq_str = anchor_inp.split()
  (N,M) = (int(sq_str[0]), int(sq_str[1]))

  if type_inp == "D":  
    if rotation_inp == "0": 
      return ("destroyer", {(N,M), (N,M+1)}, set())
    elif rotation_inp == "90":
      return ("destroyer", {(N,M), (N+1,M)}, set())
    elif rotation_inp == "180":
      return ("destroyer", {(N,M), (N,M-1)}, set())  
    elif rotation_inp == "270":
      return ("destroyer", {(N,M), (N-1,M)}, set())
  elif type_inp == "C":
    if rotation_inp == "0": 
      return ("carrier", {(N,M), (N,M+1), (N+1,M), (N+2,M)}, set())
    elif rotation_inp == "90":
      return ("carrier", {(N,M), (N+1,M), (N,M-1), (N,M-2)}, set())
    elif rotation_inp == "180":
      return ("carrier", {(N,M), (N,M-1), (N-1,M), (N-2,M)}, set())
    elif rotation_inp == "270":
      return ("carrier", {(N,M), (N-1,M), (N,M+1), (N,M+2)}, set())
  return None

#ship_from_input(type_inp, rotation_inp, anchor_inp) returns a tuple ship of the form (type, squares, hits) (see Data structures) representing a ship with the parameters supplied by the user input as follows:
#type_inp is a string indicating the type of the ship equal to "D" for destroyer and "C" for carrier
#rotation_inp is a string equal to either of "0", "90", "180" or "270" indicating the rotation
#anchor_inp is a string of the form "N M" where N indicates the row and M indicates the column of the anchor square of the ship in the ocean

def ok_to_place_ship_at(ship, fleet):
  ship_type, ship_squares, ship_hits = ship
  adj_squares = set()

  for current_ship in fleet:
    current_type, current_squares, current_hits = current_ship
    for n, m in current_squares:
      adj_squares.add((n,m))
      adj_squares.add((n+1,m))
      adj_squares.add((n-1,m))
      adj_squares.add((n,m+1))
      adj_squares.add((n,m-1))
      
  for square in ship_squares:
    #current_type, current_squares, current_hits = current_ship #checks if square already occupied
    if square in adj_squares:
      return False

  for n, m in ship_squares: #checks if same square as another ship
    if n > 9 or n < 0 or m > 9 or m < 0:
      return False
  
  return True

#ok_to_place_ship_at(ship, fleet) returns a Boolean value that is True if the ship ship can be placed in the ocean within the given fleet fleet and it returns False otherwise

def is_sunk(ship):
    """Checks if the ship is sunk."""
    ship_type, ship_squares, ship_hits = ship

    if ship_type == "destroyer":
        # All squares of the destroyer must be hit
        return ship_squares == ship_hits

    elif ship_type == "carrier":
        # Initialize lists to collect rows and columns
        ship_rows = []
        ship_cols = []
        hit_rows = []
        hit_cols = []

        # Collect rows and columns of the ship's squares
        for n, m in ship_squares:
            ship_rows.append(n)
            ship_cols.append(m)

        # Collect rows and columns of the hit squares
        for n, m in ship_hits:
            hit_rows.append(n)
            hit_cols.append(m)

        # Check if all rows or all columns of one side have been hit
        if ship_rows == hit_rows or ship_cols == hit_cols:
            return True
        else:
            return False

    return False

  

  
  #  rows = {}
   # col = {}

    #for n, m in ship_squares: #group squares by row, then col
     # rows.setdefault(n, [].append((n,m)))
      #col.setdefault(n, [].append((n,m)))

    #for row_squares in rows.values():
     # if all(square in ship_hits for square in row_squares): #check if they all hit
      #  return True
    #for col_squares in col.values():
     # if all(square in ship_hits for square in col_squares): #check if they all hit
      #  return True
  


#is_sunk(ship) returns a Boolean value that is True if the ship ship is sunk according to its sinking condition, and False otherwise

def is_water(p2_row, p2_col, fleet):
  shot = (p2_row, p2_col)
  
  for ship in fleet:  
    ship_type, ship_squares, ship_hits = ship
    if shot in ship_squares:
      if is_sunk(ship):
        return True
      elif shot in ship_hits:
        return True
      else:
        return False
  return True

#is_water(row, column, fleet) return a Boolean value that is True if firing at the square with the row row and column column results in water, and False otherwise

def what_hit(p2_row, p2_col, fleet):
  shot = (p2_row, p2_col)

  for ship in fleet:  
    ship_type, ship_squares, ship_hits = ship
    if shot in ship_squares:
      if is_sunk(ship):
        return None
      elif shot in ship_hits:
        return None
      else:
        ship_hits.add(shot)
        return ship
  return True

#what_hit(row, column, fleet) returns a tuple ship of the form (type, squares, hits) (see Data structures) representing a ship in the given fleet fleet that was hit by fire at the square with the row row and column column;
# it returns None if there is no hit to any ship in the fleet fleet as a result of the fire above

def what_sunk(p2_row, p2_col, fleet):
  shot = (p2_row, p2_col)

  for current_ship in fleet:  
    current_type, current_squares, current_hits = current_ship
    if shot in current_squares and is_sunk(current_ship) == True: #This isn't perfect. Would evaluate to true even if not last hit
      return current_ship
  return None

#what_sunk(row, column, fleet) returns a tuple ship of the form (type, squares, hits) (see Data structures) representing a ship in the given fleet fleet that will be sunk by fire at the square with the row row and column column;
#it returns None if there is no ship in the fleet fleet that will sink as a result of the fire above
def are_unsunk_left(fleet):

  for current_ship in fleet:
    if is_sunk(current_ship) == False:
      return True
  return False

#are_unsunk_left(fleet) returns a Boolean value that is True if the fleet fleet contains any unsunk ships, and False otherwise
def update_fleet(p2_row, p2_col, fleet):
  shot = (p2_row, p2_col)

  for current_ship in fleet:  
    current_type, current_squares, current_hits = current_ship
    if shot in current_squares: 
      current_hits.add(shot)
  return fleet


#update_fleet(row, column, fleet) returns a list of ships that represents the fleet fleet after a fire at the square with the row row and column column

def main():
  fleet = []

  print('Your turn Player 1. When entering a type of a ship, type "D" for destroyer and "C" for carrier (followed by Enter key).\nWhen entering rotation of a ship, type "0", "90", "180" or "270".\nWhen entering a square, first type row and then column, e.g. "6 3". Both numbers must be between 0 and 9.\n')
  
  while True:
    type_inp = input('Player 1, enter the type of the next ship or enter "Q" if you are done specifying the fleet: ') 
    if type_inp == "Q":
      break
    rotation_inp = input("Player 1, enter the rotation of this ship: ")
    anchor_inp = input("Player 1, enter the square that the anchor of this ship occupies in the ocean: ")

    ship = ship_from_input(type_inp, rotation_inp, anchor_inp)
    while ok_to_place_ship_at(ship, fleet) == False:
      anchor_inp = input("This is not a valid placement. Player 1, enter the square that the anchor of this ship occupies in the ocean: ")
      ship = ship_from_input(type_inp, rotation_inp, anchor_inp)
    fleet.append(ship)

  print('\nYour turn Player 2. When entering a square, first type row and then column, e.g. "6 3". Both numbers must be between 0 and 9.\n')
  
  shots = set()

  while are_unsunk_left(fleet) == True:
    p2_square = input('Player 2, enter the square in the ocean you fire at: ')
    p2_str = p2_square.split()
    (p2_row, p2_col) = (int(p2_str[0]), int(p2_str[1]))
    shot = (p2_row, p2_col)

    if shot in shots: #checks for the same places
      print("Water!")
      continue
    else:
      shots.add(shot)

    if is_water(p2_row, p2_col, fleet): #water
      print("Water!")
    else:
      hit_ship = what_hit(p2_row, p2_col, fleet) 
      if hit_ship is None:
        print("Water!")
      else:
        fleet = update_fleet(p2_row, p2_col, fleet)
        for ship in fleet:
          if ship[1] == hit_ship[1]:
            hit_ship = ship
            break
        if is_sunk(hit_ship):
          print("You hit a", ship_type(hit_ship), "!") 
          print('You sunk a', ship_type(hit_ship),"!")
          fleet.remove(hit_ship)
        else:
          print("You hit a", ship_type(hit_ship), "!") 

  print("Game over!")  
    
#main()

if __name__ == "__main__":  main() #DO NOT MODIFY THIS LINE OR MOVE IT FROM THE END OF FILE