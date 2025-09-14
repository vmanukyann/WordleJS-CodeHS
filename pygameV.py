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

const words = [
  "ABACK", "ABASE", "ABATE", "ABBEY", "ABIDE", "ABOUT", "ABOVE", "ABYSS", "ACORN", "ACRID", "ACTOR", "ACUTE",
  "ADAGE", "ADAPT", "ADMIT", "ADOBE", "ADOPT", "ADORE", "ADULT", "AFTER", "AGAIN", "AGAPE", "AGATE", "AGENT",
  "AGILE", "AGING", "AGLOW", "AGONY", "AGREE", "AHEAD", "AISLE", "ALBUM", "ALIEN", "ALIKE", "ALIVE", "ALLOW",
  "ALOFT", "ALONE", "ALOOF", "ALOUD", "ALPHA", "ALTAR", "ALTER", "AMASS", "AMBER", "AMISS", "AMPLE", "ANGEL",
  "ANGER", "ANGRY", "ANGST", "ANODE", "ANTIC", "ANVIL", "AORTA", "APART", "APHID", "APPLE", "APPLY", "APRON",
  "APTLY", "ARBOR", "ARDOR", "ARGUE", "AROMA", "ASCOT", "ASIDE", "ASKEW", "ASSET", "ATOLL", "ATONE", "AUDIO",
  "AUDIT", "AVAIL", "AVERT", "AWAIT", "AWAKE", "AWASH", "AWFUL", "AXIOM", "AZURE", "BACON", "BADGE", "BADLY",
  "BAGEL", "BAKER", "BALSA", "BANAL", "BARGE", "BASIC", "BASIN", "BATHE", "BATON", "BATTY", "BAYOU", "BEACH",
  "BEADY", "BEAST", "BEAUT", "BEEFY", "BEGET", "BEGIN", "BEING", "BELCH", "BELIE", "BELLY", "BELOW", "BENCH",
  "BERET", "BERTH", "BESET", "BEVEL", "BINGE", "BIOME", "BIRCH", "BIRTH", "BLACK", "BLAME", "BLAND", "BLARE",
  "BLEAK", "BLEED", "BLEEP", "BLIMP", "BLOCK", "BLOKE", "BLOND", "BLOWN", "BLUFF", "BLURB", "BLURT", "BLUSH",
  "BOOBY", "BOOST", "BOOZE", "BOOZY", "BORAX", "BOSSY", "BOUGH", "BRACE", "BRAID", "BRAIN", "BRAKE", "BRASH",
  "BRASS", "BRAVE", "BRAVO", "BREAD", "BREAK", "BREED", "BRIAR", "BRIBE", "BRIDE", "BRIEF", "BRINE", "BRING",
  "BRINK", "BRINY", "BRISK", "BROAD", "BROKE", "BROOK", "BROOM", "BROTH", "BRUSH", "BRUTE", "BUDDY", "BUGGY",
  "BUGLE", "BUILD", "BUILT", "BULKY", "BULLY", "BUNCH", "BURLY", "CABLE", "CACAO", "CACHE", "CADET", "CAMEL",
  "CAMEO", "CANDY", "CANNY", "CANOE", "CANON", "CAPER", "CARAT", "CARGO", "CAROL", "CARRY", "CARVE", "CATCH",
  "CATER", "CAULK", "CAUSE", "CEDAR", "CHAFE", "CHAIN", "CHALK", "CHAMP", "CHANT", "CHAOS", "CHARD", "CHARM",
  "CHART", "CHEAT", "CHEEK", "CHEER", "CHEST", "CHIEF", "CHILD", "CHILL", "CHIME", "CHOIR", "CHOKE", "CHORD",
  "CHUNK", "CHUTE", "CIDER", "CIGAR", "CINCH", "CIRCA", "CIVIC", "CLASS", "CLEAN", "CLEAR", "CLEFT", "CLERK",
  "CLICK", "CLIMB", "CLING", "CLOCK", "CLONE", "CLOSE", "CLOTH", "CLOUD", "CLOWN", "CLUCK", "COACH", "COAST",
  "COCOA", "COLON", "COMET", "COMMA", "CONDO", "CONIC", "CORER", "CORNY", "COULD", "COUNT", "COURT", "COVER",
  "COVET", "COWER", "COYLY", "CRAFT", "CRAMP", "CRANE", "CRANK", "CRASS", "CRATE", "CRAVE", "CRAZE", "CRAZY",
  "CREAK", "CREDO", "CREPT", "CRIME", "CRIMP", "CROAK", "CRONE", "CROSS", "CROWD", "CROWN", "CRUMB", "CRUSH",
  "CRUST", "CUMIN", "CURLY", "CYNIC", "DADDY", "DAISY", "DANCE", "DANDY", "DEATH", "DEBIT", "DEBUG", "DEBUT",
  "DECAL", "DECAY", "DECOY", "DELAY", "DELTA", "DELVE", "DENIM", "DEPOT", "DEPTH", "DETER", "DEVIL", "DIARY",
  "DICEY", "DIGIT", "DINER", "DINGO", "DISCO", "DITTO", "DODGE", "DOING", "DOLLY", "DONOR", "DONUT", "DOUBT",
  "DOWRY", "DOZEN", "DRAIN", "DRAWN", "DREAM", "DRINK", "DRIVE", "DROLL", "DROOP", "DROVE", "DUCHY", "DUTCH",
  "DUVET", "DWARF", "DWELL", "DWELT", "EARLY", "EARTH", "EBONY", "EDICT", "EGRET", "EJECT", "ELDER", "ELOPE",
  "ELUDE", "EMAIL", "EMBER", "EMPTY", "ENACT", "ENEMA", "ENJOY", "ENNUI", "ENSUE", "ENTER", "EPOCH", "EPOXY",
  "EQUAL", "EQUIP", "ERODE", "ERROR", "ERUPT", "ESSAY", "ETHER", "ETHIC", "ETHOS", "EVADE", "EVERY", "EVOKE",
  "EXACT", "EXALT", "EXCEL", "EXERT", "EXIST", "EXPEL", "EXTRA", "EXULT", "FACET", "FAINT", "FAITH", "FARCE",
  "FAULT", "FAVOR", "FEAST", "FEIGN", "FERAL", "FERRY", "FEWER", "FIBER", "FIELD", "FIEND", "FIFTY", "FILET",
  "FINAL", "FINCH", "FINER", "FIRST", "FISHY", "FIXER", "FJORD", "FLAIL", "FLAIR", "FLAKE", "FLAME", "FLANK",
  "FLARE", "FLASK", "FLESH", "FLICK", "FLING", "FLIRT", "FLOAT", "FLOCK", "FLOOD", "FLOOR", "FLORA", "FLOSS",
  "FLOUR", "FLOUT", "FLUFF", "FLUME", "FLUNK", "FLYER", "FOCAL", "FOCUS", "FOGGY", "FOLLY", "FORAY", "FORCE",
  "FORGE", "FORGO", "FORTE", "FORTH", "FORTY", "FOUND", "FOYER", "FRAME", "FRANK", "FRESH", "FRIED", "FROCK",
  "FROND", "FRONT", "FROST", "FROTH", "FROWN", "FROZE", "FULLY", "FUNGI", "FUNNY", "GAMER", "GAMMA", "GAMUT",
  "GAUDY", "GAUNT", "GAUZE", "GAWKY", "GECKO", "GENRE", "GHOUL", "GIANT", "GIDDY", "GIRTH", "GIVEN", "GLASS",
  "GLAZE", "GLEAM", "GLEAN", "GLIDE", "GLOAT", "GLOBE", "GLOOM", "GLORY", "GLOVE", "GLYPH", "GNASH", "GOLEM",
  "GONER", "GOOFY", "GOOSE", "GORGE", "GOUGE", "GRACE", "GRADE", "GRAIL", "GRAND", "GRANT", "GRAPH", "GRASP",
  "GRATE", "GRAVE", "GRAVY", "GREAT", "GREED", "GREEN", "GRIEF", "GRILL", "GRIME", "GROAN", "GROVE", "GUARD",
  "GUAVA", "GUESS", "GUEST", "GUIDE", "GUILE", "GUILT", "GUSTO", "GYPSY", "HAPPY", "HEART", "HOARD", "HOBBY",
  "HOLLY", "HORDE", "HORSE", "HOTEL", "HUMAN", "HUMOR", "HUMUS", "HYDRA", "HYPER", "IDEAL", "IDIOM", "IMPLY",
  "INDEX", "INPUT", "IVORY", "JAUNT", "JOINT", "JUDGE", "JUICE", "JUICY", "KINKY", "KNOCK", "KNOLL", "KNOWS",
  "LANCE", "LAPSE", "LATCH", "LEAST", "LEAVE", "LIVER", "LOBBY", "LODGE", "LOGIC", "LOOSE", "LUCKY", "LUMEN",
  "LUCID", "LUCKY", "LUNAR", "LUNCH", "LUNGE", "LUSTY", "LYING", "MACAW", "MADAM", "MAGIC", "MAGMA", "MAIZE",
  "MAJOR", "MANIA", "MANGA", "MANLY", "MANOR", "MAPLE", "MARCH", "MARRY", "MARSH", "MASON", "MASSE", "MATCH",
  "MATEY", "MAXIM", "MAYBE", "MAYOR", "MEALY", "MEANT", "MEDAL", "MEDIA", "MEDIC", "MELON", "MERCY", "MERGE",
  "MERIT", "MERRY", "METAL", "METER", "METRO", "MICRO", "MIDGE", "MIDST", "MIMIC", "MINCE", "MINER", "MINUS",
  "MODEL", "MODEM", "MOIST", "MOLAR", "MOMMY", "MONEY", "MONTH", "MOOSE", "MOSSY", "MOTOR", "MOTTO", "MOULT",
  "MOUNT", "MOURN", "MOUSE", "MOVIE", "MUCKY", "MULCH", "MUMMY", "MURAL", "MUSHY", "MUSIC", "MUSTY", "NAIVE",
  "NANNY", "NASTY", "NATAL", "NAVAL", "NEEDY", "NEIGH", "NERDY", "NEVER", "NICER", "NIGHT", "NINJA", "NINTH",
  "NOBLE", "NOISE", "NORTH", "NYMPH", "OCCUR", "OCEAN", "OFFAL", "OFTEN", "OLDER", "OLIVE", "ONION", "ONSET",
  "OPERA", "ORDER", "ORGAN", "OTHER", "OUGHT", "OUNCE", "OUTDO", "OUTER", "OVERT", "OWNER", "OXIDE", "PAINT",
  "PANEL", "PANIC", "PAPAL", "PAPER", "PARER", "PARRY", "PARTY", "PASTA", "PATTY", "PAUSE", "PEACE", "PEACH",
  "PENNE", "PERCH", "PERKY", "PESKY", "PHASE", "PHONE", "PHONY", "PHOTO", "PIANO", "PICKY", "PIETY", "PILOT",
  "PINCH", "PINEY", "PINKY", "PINTO", "PIOUS", "PIPER", "PIQUE", "PITHY", "PIXEL", "PIXIE", "PLACE", "PLAIT",
  "PLANK", "PLANT", "PLATE", "PLAZA", "PLEAT", "PLUCK", "PLUNK", "POINT", "POISE", "POKER", "POLKA", "POLYP",
  "PORCH", "POUND", "POWER", "PRESS", "PRICE", "PRICK", "PRIDE", "PRIME", "PRIMO", "PRINT", "PRIOR", "PRIZE",
  "PROBE", "PRONE", "PRONG", "PROUD", "PROVE", "PROWL", "PROXY", "PRUNE", "PSALM", "PULPY", "PURGE", "QUALM",
  "QUART", "QUEEN", "QUERY", "QUEST", "QUEUE", "QUICK", "QUIET", "QUIRK", "QUITE", "QUOTE", "RADIO", "RAINY",
  "RAISE", "RAMEN", "RANCH", "RANGE", "RATIO", "RAYON", "REACT", "REALM", "REBEL", "REBUS", "REBUT", "RECAP",
  "RECUR", "REFER", "REGAL", "RELIC", "RENEW", "REPAY", "REPEL", "RERUN", "RESIN", "RETCH", "RETRO", "RETRY",
  "REVEL", "RHINO", "RHYME", "RIDGE", "RIDER", "RIGHT", "RIPER", "RISEN", "RIVAL", "ROBIN", "ROBOT", "ROCKY",
  "RODEO", "ROGUE", "ROOMY", "ROUGE", "ROUND", "ROUSE", "ROUTE", "ROVER", "ROYAL", "RUDDY", "RUDER", "RUPEE",
  "RUSTY", "SAINT", "SALAD", "SALLY", "SALSA", "SALTY", "SANDY", "SASSY", "SAUCY", "SAUTE", "SAVOR", "SCALD",
  "SCALE", "SCANT", "SCARE", "SCARF", "SCENT", "SCOFF", "SCOLD", "SCONE", "SCOPE", "SCORN", "SCOUR", "SCOUT",
  "SCRAM", "SCRAP", "SCRUB", "SEDAN", "SEEDY", "SENSE", "SERUM", "SERVE", "SEVEN", "SEVER", "SHADE", "SHAFT",
  "SHAKE", "SHALL", "SHAME", "SHANK", "SHAPE", "SHARD", "SHARP", "SHAVE", "SHAWL", "SHELL", "SHIFT", "SHINE",
  "SHIRE", "SHIRK", "SHORE", "SHORN", "SHOUT", "SHOWN", "SHOWY", "SHRUB", "SHRUG", "SHYLY", "SIEGE", "SIGHT",
  "SINCE", "SISSY", "SKATE", "SKIER", "SKIFF", "SKILL", "SKIMP", "SKIRT", "SKUNK", "SLATE", "SLEEK", "SLEEP",
  "SLICE", "SLOPE", "SLOSH", "SLOTH", "SLUMP", "SLUNG", "SMALL", "SMART", "SMASH", "SMEAR", "SMELT", "SMILE",
  "SMIRK", "SMITE", "SMITH", "SMOCK", "SMOKE", "SNACK", "SNAFU", "SNAIL", "SNAKE", "SNAKY", "SNARE", "SNARL",
  "SNEAK", "SNORT", "SNOUT", "SOGGY", "SOLAR", "SOLID", "SOLVE", "SONIC", "SOUND", "SOWER", "SPACE", "SPADE",
  "SPEAK", "SPECK", "SPELL", "SPELT", "SPEND", "SPENT", "SPICE", "SPICY", "SPIEL", "SPIKE", "SPILL", "SPIRE",
  "SPLAT", "SPOKE", "SPOON", "SPOUT", "SPRAY", "SPURT", "SQUAD", "SQUAT", "STAFF", "STAGE", "STAID", "STAIN",
  "STAIR", "STAKE", "STALE", "STALL", "STAND", "STARK", "START", "STASH", "STATE", "STEAD", "STEAM", "STEED",
  "STEEL", "STEIN", "STERN", "STICK", "STIFF", "STILL", "STING", "STINK", "STINT", "STOCK", "STOLE", "STOMP",
  "STONE", "STONY", "STOOL", "STORE", "STORM", "STORY", "STOUT", "STOVE", "STRAP", "STRAW", "STUDY", "STUNG",
  "STYLE", "SUGAR", "SULKY", "SUPER", "SURER", "SURLY", "SUSHI", "SWEAT", "SWEEP", "SWEET", "SWILL", "SWINE",
  "SWIRL", "SWISH", "SWOON", "SWUNG", "SYRUP", "TABLE", "TABOO", "TACIT", "TAKEN", "TALON", "TANGY", "TAPER",
  "TAPIR", "TARDY", "TASTE", "TASTY", "TAUNT", "TAWNY", "TEACH", "TEARY", "TEASE", "TEMPO", "TENTH", "TEPID",
  "TERSE", "THANK", "THEIR", "THEME", "THERE", "THESE", "THIEF", "THIGH", "THING", "THINK", "THIRD", "THORN",
  "THOSE", "THREE", "THREW", "THROW", "THUMB", "THUMP", "THYME", "TIARA", "TIBIA", "TIDAL", "TIGER", "TILDE",
  "TIPSY", "TITAN", "TITHE", "TITLE", "TODAY", "TONIC", "TOPAZ", "TOPIC", "TORCH", "TORSO", "TOTEM", "TOUCH",
  "TOUGH", "TOWEL", "TOXIC", "TOXIN", "TRACE", "TRACT", "TRADE", "TRAIN", "TRAIT", "TRASH", "TRAWL", "TREAT",
  "TREND", "TRIAD", "TRICE", "TRITE", "TROLL", "TROPE", "TROVE", "TRUSS", "TRUST", "TRUTH", "TRYST", "TUTOR",
  "TWANG", "TWEAK", "TWEED", "TWICE", "TWINE", "TWIRL", "ULCER", "ULTRA", "UNCLE", "UNDER", "UNDUE", "UNFED",
  "UNFIT", "UNIFY", "UNITE", "UNLIT", "UNMET", "UNTIE", "UNTIL", "UNZIP", "UPSET", "URBAN", "USAGE", "USHER",
  "USING", "USUAL", "USURP", "UTTER", "VAGUE", "VALET", "VALID", "VALUE", "VAPID", "VAULT", "VENOM", "VERGE",
  "VERVE", "VIDEO", "VIGOR", "VIOLA", "VIRAL", "VITAL", "VIVID", "VODKA", "VOICE", "VOILA", "VOTER", "VOUCH",
  "WACKY", "WAGON", "WALTZ", "WASTE", "WATCH", "WEARY", "WEDGE", "WHACK", "WHALE", "WHEEL", "WHELP", "WHERE",
  "WHICH", "WHIFF", "WHILE", "WHINE", "WHINY", "WHIRL", "WHISK", "WHOOP", "WIDEN", "WINCE", "WINDY", "WOKEN",
  "WOMAN", "WOOER", "WORDY", "WORLD", "WORRY", "WORSE", "WORST", "WOULD", "WOVEN", "WRATH", "WREAK", "WRIST",
  "WRITE", "WRONG", "WROTE", "WRUNG", "YACHT", "YEARN", "YIELD", "YOUNG", "YOUTH", "ZEBRA", "ZEALY", "ZESTY"];
  

if __name__ == "__main__":
    main()
