import random
import time
import os
import sys

#Basic Grid Setup and System
start = time.time()
grid = [[]]
grid_size = 10
starting_ships = 8
num_of_ships = 8
bullets_left = 60
starting_bullets = 60
game_over = False
ships_sunk = 0
ship_positions = [[]]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
''
#checks if it is safe to place the ship there - returns true or false
def validate_and_place_ship(start_row, end_row, start_col, end_col):
  global grid
  global ship_positions

  #Checks if it is empty space: if not, returns false
  all_valid = True
  for r in range(start_row, end_row):
    for c in range(start_col, end_col):
      if grid[r][c] != ".":
        all_valid = False
        break
  
  #Will only activate once all valid is true
  if all_valid == True:
    ship_positions.append([start_row, end_row, start_col, end_col])
    for r in range(start_row, end_row):
      for c in range(start_col, end_col):
        grid[r][c] = "O"
  
  return all_valid

#based on direction calls helper method to try and place ship on grid
def try_to_place_ship_on_grid(row, col, direction, length):
  global grid_size
  
  start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
  
  if direction == "left":
    if col - length < 0:
      return False
    start_col = col - length + 1
  
  elif direction == "right":
    if col + length >= grid_size:
      return False
    end_col = col + length
  
  elif direction == "up":
    if row - length < 0:
      return False
    start_row = row - length + 1
  
  elif direction == "down":
    if row + length >= grid_size:
      return False
    end_row = row + length
  
  return validate_and_place_ship(start_row, end_row, start_col, end_col)

#creates a 15 x 15 grid and places ships of different sizes in random directions
def create_grid():
  global grid
  global grid_size
  global num_of_ships
  global ship_positions
  
  random.seed(time.time())

  rows, cols = (grid_size, grid_size)

  grid = []
  
  for r in range(rows):
    row = []
    for c in range(cols):
      row.append(".")
    grid.append(row)
  
  num_of_ships_placed = 0

  ship_positions = []

  while num_of_ships_placed != num_of_ships:
    random_row = random.randint(0, rows - 1)
    random_col = random.randint(0, cols - 1)
    direction = random.choice(["left", "right", "up", "down"])
    ship_size = random.randint(3, 5)
    if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
      num_of_ships_placed += 1

#prints the grid with rows A-N and columns 0-14
def print_grid():

    global grid
    global alphabet

    debug_mode = False

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len(grid)):
      print(alphabet[row], end=") ")
      for col in range(len(grid[row])):
        if grid[row][col] == "O":
          if debug_mode:
            print("O", end=" ")
          else:
            print(".", end=" ")
        else:
          print(grid[row][col], end=" ")
      print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")
  
#gets valid row and column to place bullet shot
def accept_valid_bullet_placement():
  global grid
  global alphabet
  
  is_valid = False
  row = -1
  col = -1
  while is_valid == False:
    print("\nPlease enter a row (A-J) and column(0-9) to choose where to fire your bullet.")
    print("(Ex: A3)")
    placement = input("-> ")
    placement = placement.upper()
    if len(placement) <= 0 or len(placement) > 2:
      print("\nInvalid Placement. Please try again...")
      continue
    row = placement[0]
    col = placement[1]
    if not row.isalpha() or not col.isnumeric():
      print("\nInvalid Placement. Please try again...")
      continue
    row = alphabet.find(row)
    if not (-1 < row < grid_size):
      print("\nInvalid Placement. Please try again...")
      continue
    col = int(col)
    if not (-1 < col < grid_size):
      print("\nInvalid Placement. Please try again...")
      continue
    if grid[row][col] == "#" or grid[row][col] == "X":
      print("\nYou have already shot a bullet here.\nPlease pick somewhere else...")
      continue
    if grid[row][col] == "." or grid[row][col] == "O":
      is_valid = True

  return row, col

#if all parts of a ship have been shot it is sunk and we later increment the sinking sequence
def check_for_ship_sunk(row, col):
  global ship_positions
  global grid
  
  for position in ship_positions:
    start_row = position[0]
    end_row = position[1]
    start_col = position[2]
    end_col = position[3]

    if start_row <= row <= end_row and start_col <= col <= end_col:
      #ship has been found, now checks if it has sunk
      for r in range(start_row, end_row):
        for c in range(start_col, end_col):
          if grid[r][c] != "X":
            return False
  
  return True

#Updates grid and ships based on where bullet was shot
def shoot_bullet():
  global grid
  global ships_sunk
  global bullets_left
  global num_of_ships
  
  row, col = accept_valid_bullet_placement()

  os.system('clear')
  print("Updating Grid...")
  time.sleep(0.5)
  print("Checking for errors...")
  time.sleep(0.5)
  print("Updating number of bullets...")
  time.sleep(0.5)
  os.system('clear')
  print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
  print("BATTLESHIPS")
  print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
  if grid[row][col] == ".":
    print("You've only hit empty water, no ship was shot!")
    grid[row][col] = "#"
  elif grid[row][col] == "O":
    print("You've hit a ship...", end = "\n")
    grid[row][col] = "X"
    if check_for_ship_sunk(row, col):
      print("And have completely sunk it in the process!")
      ships_sunk += 1
      num_of_ships -= 1
    else:
      print("And have dealt some damage to it in the process!")
  
  bullets_left -= 1
  

#Checks if game is over
def check_for_game_over():
  global ships_sunk
  global num_of_ships
  global bullets_left
  global game_over
  global start
  
  if num_of_ships < 1:
    end = time.time()
    diff = round(end, 2) - round(start, 2)
    os.system('clear')
    print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
    print("BATTLESHIPS")
    print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
    print("Congratulations, you've won the game!")
    print("You have successfully sunk all eight ships.")
    print("Thanks for playing!")
    print("\nFinal Score: " + str(diff) + " seconds")
    print("\n⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
    print("Would you like to play again?")
    print("1) Yes")
    print("2) No")
    play_again = input("-> ")
    if play_again == "1":
      main_menu()
    else:
      os.system('clear')
      exit()
    game_over = True
  elif bullets_left <= 0:
    print("You have lost and run out of bullets!")
    game_over = True

def main():
  global game_over

  create_grid()

  while game_over == False:
    print_grid()
    print("")
    print("Ships Remaining: " + str(num_of_ships) + "/" + str(starting_ships))
    print("Bullets Left: " + str(bullets_left) + "/" + str(starting_bullets))
    shoot_bullet()
    print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
    print("")
    check_for_game_over()

def main_menu():
  os.system('clear')
  print("                           BATTLESHIPS         ")
  print("                   ⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
  print("Attempt to sink all 8 ships.")
  print("You will start out with 60 bullets. Choose wisely.")
  print("When the program prompts you, type in a row and a column in orderto fire a bullet.")
  print("If you do not manage to sink all 8 ships when your bullets run out, you will lose the game.")
  print("")
  input("Enter anything to continue... ")
  os.system('clear')
  print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
  print("BATTLESHIPS")
  print("⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆")
  main()

if __name__ == "__main__":
  main_menu()