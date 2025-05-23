import pygame
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.display.set_caption('2048')
pygame.font.init()
running = True
# Text rendering function:
text_font = pygame.font.SysFont("Arial",30)
def draw_text(text, font, text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
squares = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(2):
    random_square = 2 + 2 * (random.randint(1,10) == 10)
    random_index = random.randint(0,15) 
    squares[(random_index)//4][(random_index)%4] = random_square

def left(squares):
  for r in range(4):
    # convert to int for easy processing and getting rid of 0s
    row = [int(x) for x in squares[r] if x != "0"]
    # using while loop since we change the length of the loop
    i = 0
    while i < len(row)-1:
      # check if the adjacent number is equal
      if row[i] == row[i + 1]:
        # Multiply the number by 2 and delete the adjacent number (it is ahead and this is the left function)
        row[i] *= 2
        del row[i + 1]
        # Iterating through while loop
        i += 1
      else:
        i += 1
    # Padding the right with zeros after moving left
    while len(row) < 4:
      row.append("0")
    # sending the updated row back to squares
    squares[r] = [str(x) for x in row]

def right(squares):
    for r in range(4):
        row = [int(x) for x in squares[r] if x != "0"]
        # going backwards
        i = len(row) - 1
        while i > 0:
            if row[i] == row[i - 1]:
                row[i] *= 2
                del row[i - 1]
                # don't decrement i again
            i -= 1
        row = [0] * (4 - len(row)) + row
        squares[r] = [str(x) for x in row]
def down(squares):
    for c in range(4):
        # Get all non-zero values in the column (top to bottom)
        col = [int(squares[r][c]) for r in range(4) if squares[r][c] != "0"]
        # Reverse to simulate bottom-up merging
        col.reverse()
        
        # Merge identical numbers
        i = 0
        while i < len(col) - 1:
            if col[i] == col[i + 1]:
                col[i] *= 2
                del col[i + 1]
                i += 1
            else:
                i += 1
        
        # Pad with 0s at the end and reverse back
        while len(col) < 4:
            col.append(0)
        col.reverse()
        
        # Write the merged column back into the grid (top to bottom)
        for r in range(4):
            squares[r][c] = col[r]

def up(squares):
  for c in range(4):
    # convert to int for easy processing and getting rid of 0s
    # similar to before except col major, goes through each row r with a set column c
    col = []
    for r in range(4):
      if squares[r][c] != "0":
        col += [int(squares[r][c])]
    # using while loop since we change the length of the loop
    
    i = 0
    while i < len(col)-1:
      if col[i] == col[i + 1]:
        col[i] *= 2
        del col[i + 1]
        i += 1
      else:
        i += 1
    while len(col) < 4:
      col.append("0")
    
    for r in range(4):
      squares[r][c] = col[r]
while running:
    color = pygame.Color(125,125,125)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Filling a random number every time a key is pressed
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):

            if event.key == pygame.K_LEFT:
                left(squares)
            elif event.key == pygame.K_RIGHT:
                right(squares)
            elif event.key == pygame.K_UP:
                up(squares)
            elif event.key == pygame.K_DOWN:
                down(squares)
            flat = []
            for i in squares:
                flat += i
            empty_indices = [i for i, v in enumerate(flat) if v == "0"]
            if empty_indices:
                new_index = random.choice(empty_indices)
                squares[new_index // 4][new_index % 4] = 2 + 2 * (random.randint(1, 10) == 10)

    screen.fill(color)
    
    for i in range(0,4):
        pygame.draw.line(screen,(0,0,0), (125*i,0), (125*i,500))
        pygame.draw.line(screen,(0,0,0), (0,125*i), (500,125*i))
        for j in range(0,4):
            draw_text(str(squares[i][j]),text_font, (0,0,0),125*j + 50, 125*i+50)
    """
    draw_text(str(squares), text_font, (0,0,0),0, 125)
    """
    pygame.display.flip()
    clock.tick(4)  # limits FPS to 60
pygame.quit()
