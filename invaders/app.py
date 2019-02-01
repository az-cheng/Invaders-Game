"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Annie Cheng zc375; Ruitong rl699
# November 29, 2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    OTHER ATTRIBUTES:
        _lastkeys: the number of keys pressed last frame [int >= 0]
        _win: True if the player wins, False otherwise [bool]
        _winsound: the win sound when the player won [Sound]
        _losesound: the lose sound when the player lost [Sound]
        _volume: the volume of the sounds being played [0 or 1]
        _livesbox: the display of the number of lives left at the top right corner
                   [GLabel, or None if there is no message to display]
        _levelbox: the display of the current level in the center of the top
                   [GLabel, or None if there is no message to display]
        _level: current level, increase 1 everytime a player wins [int >= 1]
        _scorebox: the display of the current score at the top left corner
                   [GLabel, or None if there is no message to display]
        _text0: added message 0 when diplaying instruction
                   [GLabel, or None if there is no message to display]
        _text2: added message 2 when diplaying instruction
                   [GLabel, or None if there is no message to display]
        _text3: added message 3 when diplaying instruction
                   [GLabel, or None if there is no message to display]
        _text4: added message 4 when diplaying instruction
                   [GLabel, or None if there is no message to display]
    """
    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._lastkeys = 0
        self._win = None
        message = "Space Invaders"
        self._text0 = None
        self._text = self._primeText(message)
        self._text2 = None
        self._text3 = None
        self._text4 = None
        self._winsound = Sound('win.wav')
        self._losesound = Sound('lose.wav')
        self._volume = 1
        self._livesbox = None
        self._levelbox = None
        self._level = 1
        self._scorebox = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        STATE_NEWGAME: This state displays a message depending on if the player
        has won or lost. The application switches to this state if the state was
        STATE_COMPLETE in the previous frame, and the player pressed a key. This
        state only lasts one animation frame before switching to STATE_ACTIVE.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._determineState(STATE_INSTRUCTION-STATE_INACTIVE)
        if self._state == STATE_INSTRUCTION:
            self._stateInstrcution()
        if self._state == STATE_NEWWAVE:
            self._stateNewWave()
        if self._state == STATE_ACTIVE:
            self._stateActive(dt,input)
        if self._state == STATE_PAUSED:
            message = "Press 'S' to Continue"
            self._text = self._primeText(message)
            self._livesbox = self._livesboxText()
            self._determineState(1)
        if self._state == STATE_CONTINUE:
            self._wave.setShip()
            self._text = None
            self._state = STATE_ACTIVE
        if self._state == STATE_COMPLETE:
            message = "You Lose :(" if self._win == False else "You Win!"
            self._text = self._primeText(message)
            self._livesbox = self._livesboxText()
            self._determineState(1)
        if self._state == STATE_NEWGAME:
            message = "Press 'S' for Another Try" if self._win == False else \
            "Press 'S' for a New Wave"
            self._text = self._primeText(message)
            self._determineState(STATE_NEWWAVE-STATE_NEWGAME)

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._primeDraw(self._text)
        self._primeDraw(self._wave)
        self._primeDraw(self._text0)
        self._primeDraw(self._text2)
        self._primeDraw(self._text3)
        self._primeDraw(self._text4)
        self._primeDraw(self._livesbox)
        self._primeDraw(self._levelbox)
        self._primeDraw(self._scorebox)

    # HELPER METHODS FOR THE STATES GO HERE
    def _primeText(self,message):
        """
        Return the text label with given message.

        Parameter message: message needs to be displayed
        Precondition: message is a GLabel object
        """
        return GLabel(text = message, x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                      font_size = FONT_SIZE, font_name = FONT_NAME)

    def _primeDraw(self, a):
        """
        Draw the given GObject a.

        Parameter a: object needs to be drawn
        Precondition: a is a GObject and an attribute of the class Invader
        """
        if a != None:
            a.draw(self.view)

    def _determineState(self,n):
        """
        Determines the current state and assigns it to self.state

        This method checks for a key press, and if there is one, changes the state
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.

        Parameter n: number of the state needs to be changed
        Precondition: n is an int

        Adopted from state.py by Walker M. White
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self._lastkeys == 0
        if change:
            self._state += n
        self._lastkeys = curr_keys

    def _stateActive(self,dt,input):
        """
        Check to see if there's any change in state. If not, then update wave.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        # pause the game
        if self._wave.getShip() == None and self._wave.getLives() > 0:
            self._state = STATE_PAUSED

        # end the game when there's no lives
        elif self._wave.getShip() == None and self._wave.getLives() == 0:
            self._win = False
            self._losesound.play()
            self._state = STATE_COMPLETE

        # end the game when there's no aliens
        elif self._wave.getAliensLeft() == 0 and self._wave.getLives() > 0:
            self._win = True
            self._winsound.play()
            self._level += 1
            self._state = STATE_COMPLETE

        # end the game when alien crossed the defense line
        elif self._wave.getCrossLine() == True and self._wave.getLives() > 0:
            self._win = False
            self._losesound.play()
            self._state = STATE_COMPLETE

        # otherwise keep updating
        self._wave.update(self.input,dt)
        self._scorebox = self._scoreboxText()

        # check if there's any key down to mute or unmute the sounds
        if self.input.is_key_down('u'):
            self._turnVolume(1)
        if self.input.is_key_down('m'):
            self._turnVolume(0)

    def _stateNewWave(self):
        """
        Create a new wave and make change to alien speed accordingly.
        """
        self._text0 = None
        self._text = None
        self._text2 = None
        self._text3 = None
        self._text4 = None
        if self._win != None:
            speed = self._wave.getAlienSpeed()
            score = self._wave.getScore()
        n = self._volume
        self._wave = Wave()

        # set the alien speed for the new wave by win or lose
        if self._win == True:
            self._wave.setAlienSpeed(speed*SPEED_FACTOR2)
            self._wave.setScore(score)
        elif self._win == False:
            self._wave.setAlienSpeed(speed)
            self._wave.setScore(score)

        self._win == None
        if self._wave.getSounds()[0].volume > n:
            self._turnVolume(0)
        self._livesbox = self._livesboxText()
        self._levelbox = self._levelboxText()
        self._scorebox = self._scoreboxText()
        self._state = STATE_ACTIVE

    def _turnVolume(self,n):
        """
        Either mute or unmute all sounds in the application.

        Parameter n: volume to turn to
        Precondition: n is either 0 or 1
        """
        for i in [self._winsound,self._losesound]:
            i.volume = n
            self._volume = i.volume
        self._wave.setSounds(n)

    def _livesboxText(self):
        """
        Return the text label showing the number of lives left.
        """
        lives = str(self._wave.getLives()) if self._wave != None else '3'
        return GLabel(text = 'Lives: '+lives, x=LIVESBOX_X,y=LIVESBOX_Y,
                      font_size = FONT_SIZE/2, font_name = FONT_NAME)

    def _levelboxText(self):
        """
        Return the text label showing the current level.
        """
        return GLabel(text = 'Level '+str(self._level), x=GAME_WIDTH/2,
                      y=LIVESBOX_Y, font_size = FONT_SIZE/2,
                      font_name = FONT_NAME)

    def _scoreboxText(self):
        """
        Return the text label showing the current score.
        """
        return GLabel(text = 'Score: '+str(self._wave.getScore()),
                      x=GAME_WIDTH-LIVESBOX_X, y=LIVESBOX_Y,
                      font_size = FONT_SIZE/2, font_name = FONT_NAME)

    def _stateInstrcution(self):
        """
        Display messages during state instruction.
        """
        message0 = "Instruction"
        self._text0 = GLabel(text = message0, x=GAME_WIDTH/2, y=TEXT_Y0,
                             font_size = FONT_SIZE, font_name = FONT_NAME)
        message1 = "1. Press 'S' to Play"
        self._text = GLabel(text = message1, x=TEXT_X, y=TEXT_Y,
                             font_size = FONT_SIZE/2, font_name = FONT_NAME)
        message2 = "2. Press Spacebar to Fire Bolt"
        self._text2 = GLabel(text = message2, x=TEXT_X2, y=TEXT_Y2,
                             font_size = FONT_SIZE/2, font_name = FONT_NAME)
        message3 = "3. Press Left/Right to Move the Ship"
        self._text3 = GLabel(text = message3, x=TEXT_X3, y=TEXT_Y3,
                             font_size = FONT_SIZE/2, font_name = FONT_NAME)
        message4 = "4. Press 'M' to Mute Sound, Press 'U' to Unmute Sound"
        self._text4 = GLabel(text = message4, x=GAME_WIDTH/2, y=TEXT_Y4,
                             font_size = FONT_SIZE/2, font_name = FONT_NAME)
        self._determineState(STATE_NEWWAVE-STATE_INSTRUCTION)
