/*
Welcome to Wordle in JavaScript!
The Goal of this game is to find the unkown word with color changes of each letter
Green = A specific letter is in the correct space
Yellow = A specific letter is in the word but not in the correct space
Grey = A letter is not in the word at all
Each Guess must be 5 letters long and there are 6 attempts to find the word
Good Luck!
 */
 
// Variables
let boxs;
let boxes = [];
let resultColors = [];
let width = getWidth();
let boxWidth = 45;
let height = getHeight();
let gray = "#CECECE"
let boxBuffer = 5
let topBuffer = (width-(boxWidth+boxBuffer)*5)
let row;
let column;
let layer;
let randomWord;
let attempt = 0;
let attemptArray = 0;
let response;
let notFiveLettersCount = 0;
let end;
let guessCount = 0;
let letter = [];
let geussLetter = [];
let guess;
let button1;
let button2;

let name = readLine("Enter Name: ")
console.log("Hello " + name + ", press any key to start!")


// FUNCTIONS:
function main(){
    characterPlace();
    wordShuffle(words);
    //console.log(words[randomWord])
    keyDownMethod(input);
    buttons();
    mouseClickMethod(click);
}

function retry() {
    attempt = 0;
    boxes = []; // Clear boxes array
    console.log(name + ", press any key to retry!");
    characterPlace(); // Redraw the grid
    wordShuffle(words); // Generate a new word
    keyDownMethod(input);
    buttons(); // Redraw buttons
    mouseClickMethod(click);
}

// Game State
function winLose() {
    if (attempt >= 6) {
        console.log("You Lose, the word was: " + words[randomWord])
    }
    
    if (guess == words[randomWord]) {
        console.log("You Win")
    }
}

// Adds inputed Word onto screen
function displayWord (guess, row) {
    for(column = 0; column < guess.length; column ++){
        let letter1 = guess[column];
        let box = boxes[row][column];

        let xpos = box.getX(); 
        let ypos = box.getY();

        let displayText = new Text(letter1, "20pt Arial")
        displayText.setPosition(xpos, ypos);
        displayText.setColor("White")
        add(displayText);
    }
}

// Any Inputs for the User
function input(e) {
    guess  = readLine("Enter word:").toUpperCase();
    if (guess  != null) {
        determineColors();
            attempt++;
        }
    //Length/No Response Checker
    if (guess.length > 5 || guess.length < 5 || guess == null) {
        console.log("Must be 5 letters");
        guess = readLine("Enter word: ").toUpperCase();
        if (guess.length > 5 || guess.length < 5 || guess == null) {
            console.log("Must be 5 letters");
            guess = readLine("Enter word: ").toUpperCase();
            if (guess.length > 5 || guess.length < 5 || guess == null) {
            console.log("Bro just put the fries in the bag and enter a 5 letter word in.");
            }
        }
    }
    
    //displayWord(guess, row)
    winLose();
}

// COLORS!
function determineColors() { 
    resultColors = []; // Reset resultColors for this attempt
    checkGreen();
    checkYellow();
    checkGray();
    updateBoxColors(resultColors, attempt);
}

// Child Function of determinColors
function checkGreen() {
    letter = []; // Store target word's letters for reference
    for (let column = 0; column < 5; column++) {
        const targetChar = words[randomWord].charAt(column);
        letter.push(targetChar);

        if (guess[column] == targetChar) {
            resultColors[column] = "#6AAA64"; 
        } else {
            resultColors[column] = null; 
        }
    }
}

// Child Function of determinColors
function checkYellow() {
    let unmatchedLetters = letter.slice(); // Clone of the target word's letters
    // Remove greens from unmatched letters to prevent double counting
    for (let column = 0; column < 5; column++) {
        if (resultColors[column] == "#00FF00") {
            const index = unmatchedLetters.indexOf(guess[column]);
            if (index !== -1) {
                unmatchedLetters[index] = null; // Mark as used
            }
        }
    }
    for (let column = 0; column < 5; column++) {
        if (resultColors[column] == null) {
            const index = unmatchedLetters.indexOf(guess[column]);
            if (index !== -1) {
                resultColors[column] = "#FFFF00"; // Yellow for correct letter, wrong position
                unmatchedLetters[index] = null; // Mark as used
            }
        }
    }
}

// Child Function of determinColors
function checkGray() {
    for (let column = 0; column < 5; column++) {
        if (resultColors[column] == null) {
            resultColors[column] = "#787C7E"; // Gray for incorrect letters
        }
    }
}

// Child Function of determinColors/Takes the result and adds the needed color
function updateBoxColors(colors, row) {
    for (let column = 0; column < colors.length; column++) {
        if (boxes[row] && boxes[row][column]) {
            boxes[row][column].setColor(colors[column]);
        } 
    }
}

function buttons() {
    button1 = new Rectangle(width / 4, height / 10);
    button1.setPosition(width / 4.6, height / 1.19);
    button1.setColor("Orange");
    add(button1);

    button2 = new Rectangle(width / 3.5, height / 10);
    button2.setPosition(width / 1.81, height / 1.19);
    button2.setColor("Blue");
    add(button2);
    
    let rules = new Text("Restart","25pt Trattatello " );
    rules.setPosition(width/4.5, height/1.1);
    add(rules);
    
    let rules2 = new Text("Give up", "25pt Trattatello ");
    rules2.setPosition(width/1.8, height/1.1);
    add(rules2);
}

function click(e) {
    let x = e.getX();
    let y = e.getY();

    if (
        x >= button1.getX() &&
        x <= button1.getX() + button1.getWidth() &&
        y >= button1.getY() &&
        y <= button1.getY() + button1.getHeight()
    ) {
        console.log("processing...");
        console.log("New Game Started")
        retry();

    }
    if (
        x >= button2.getX() &&
        x <= button2.getX() + button2.getWidth() &&
        y >= button2.getY() &&
        y <= button2.getY() + button2.getHeight()
    ) {
        console.log("The Word was: " + words[randomWord] );
    }
}


// Adds Constant Boxs/Text
function characterPlace(e) {
    let back = new Rectangle(width, height);
        back.setPosition(0, 0);
        back.setColor("white");
        add(back); 
    for (row = 0; row < 6; row++){
        let rowA = [];
        for(column = 0; column < 5; column++) {
            // Background box DOES NOT CHANGE
            layer = new Rectangle(boxWidth, boxWidth);
            layer.setPosition(column*(boxWidth + boxBuffer)+topBuffer/1.8, topBuffer/1.8+(boxWidth + boxBuffer)* row);
            layer.setColor(gray);
            add(layer); 
            
            // White box, subject to change throughout the game
            boxs = new Rectangle(boxWidth-4, boxWidth-4);
            boxs.setPosition(column*(boxWidth + boxBuffer)+ topBuffer/1.8+2, 2+topBuffer/1.8+(boxWidth+ boxBuffer)* row);
            boxs.setColor("white");
            add(boxs); 
            
            rowA.push(boxs);
        }
        boxes.push(rowA)
    }
    
    // TEXTS
    let txt = new Text("WORDLE", "50pt Impact ");
    txt.setPosition(width/4, height/8);
    add(txt);
    let txt1 = new Text("by Vazgen Manukyan", "10pt Impact ");
    txt1.setPosition(width/3+20, height/6);
    add(txt1);

}
// Answer to the game
function wordShuffle(words) {
        // Randomizes by taking a random number from the length of the array (30)
        randomWord = Math.floor(Math.random() * words.length)
        // returns that random number's corresponding word
        return(words[randomWord])
}


// 1128 words from past wordles 
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
  
main();
