import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 6, 5
BOX_SIZE = 60
MARGIN = 10
TOP_OFFSET = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 124, 126)
YELLOW = (201, 180, 88)
GREEN = (106, 170, 100)

# Fonts
FONT = pygame.font.SysFont("Arial", 40, bold=True)
TITLE_FONT = pygame.font.SysFont("Impact", 60)
SUB_FONT = pygame.font.SysFont("Arial", 24)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle by Vazgen Manukyan")

# Pick random target
target_word = random.choice(WORDS).upper()

# Game state
guesses = []
colors = []
current_guess = ""
game_over = False
message = ""

def draw_board():
    screen.fill(WHITE)

    # Title
    title = TITLE_FONT.render("WORDLE", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    subtitle = SUB_FONT.render("by Vazgen Manukyan", True, BLACK)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 80))

    # Draw grid
    for r in range(ROWS):
        for c in range(COLS):
            x = c * (BOX_SIZE + MARGIN) + (WIDTH - (COLS * (BOX_SIZE + MARGIN))) // 2
            y = r * (BOX_SIZE + MARGIN) + TOP_OFFSET
            rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
            color = GRAY

            if r < len(colors):  # Already guessed rows
                color = colors[r][c]
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)

            # Draw letters
            if r < len(guesses):
                letter = guesses[r][c]
                letter_surface = FONT.render(letter, True, WHITE)
                screen.blit(letter_surface, (
                    x + BOX_SIZE // 2 - letter_surface.get_width() // 2,
                    y + BOX_SIZE // 2 - letter_surface.get_height() // 2
                ))

    # Draw current guess
    if not game_over:
        r = len(guesses)
        for c, ch in enumerate(current_guess):
            x = c * (BOX_SIZE + MARGIN) + (WIDTH - (COLS * (BOX_SIZE + MARGIN))) // 2
            y = r * (BOX_SIZE + MARGIN) + TOP_OFFSET
            letter_surface = FONT.render(ch, True, BLACK)
            screen.blit(letter_surface, (
                x + BOX_SIZE // 2 - letter_surface.get_width() // 2,
                y + BOX_SIZE // 2 - letter_surface.get_height() // 2
            ))

    # Show message
    if message:
        msg_surface = SUB_FONT.render(message, True, BLACK)
        screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

def check_guess(guess):
    row_colors = [GRAY] * COLS
    target_letters = list(target_word)

    # Green pass
    for i in range(COLS):
        if guess[i] == target_letters[i]:
            row_colors[i] = GREEN
            target_letters[i] = None  # Consume letter

    # Yellow pass
    for i in range(COLS):
        if row_colors[i] == GRAY and guess[i] in target_letters:
            row_colors[i] = YELLOW
            target_letters[target_letters.index(guess[i])] = None

    return row_colors

def main():
    global current_guess, game_over, message, target_word, guesses, colors

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    if len(current_guess) == 5:
                        guess = current_guess.upper()
                        if guess not in WORDS:
                            message = "Not in word list"
                        else:
                            guesses.append(guess)
                            colors.append(check_guess(guess))
                            if guess == target_word:
                                message = "You Win!"
                                game_over = True
                            elif len(guesses) >= ROWS:
                                message = f"You Lose! Word was {target_word}"
                                game_over = True
                            current_guess = ""
                    else:
                        message = "Must be 5 letters"
                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif pygame.K_a <= event.key <= pygame.K_z:
                    if len(current_guess) < 5:
                        current_guess += chr(event.key).upper()

        draw_board()

WORDS = ["ABOUT", "OTHER", "WHICH", "THEIR", "APPLE", "MOUSE", "HAPPY", "SMART", "CRANE", "SMILE"]

if __name__ == "__main__":
    main()
