"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Annie Cheng zc375; Ruitong rl699
# November 29, 2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _direction: the direction in which the aliens are moving [0 or 1]
        _step: the number of steps until the aliens fire [random int bewteen 1 and BOLT_RATE]
        _time2: the amount of time since the last Alien firing bolt [number >= 0]
        _aliensleft: the number of aliens left [int >=0]
        _crossline: True if any alien has crossed the defense line, False otherwise
                    [bool]
        _alienscoords: coordinates of active aliens [list of tuples, possibly empty]
        _alienspeed: the speed in which the aliens are moving [number >= 0]
        _movesound: a list of the move Sound objects when aliens move [list]
        _move: the number of move aliens taken since the first move sound
               [int between 0 and 3]
        _sounds: a list of all Sound objects being used in class Wave [list]
        _score: current score [int >= 0]
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the number of lives left.
        """
        return self._ship

    def setShip(self):
        """
        Set the _ship attribute.
        """
        self._ship = Ship(source0='ship.png')

    def getLives(self):
        """
        Returns the number of lives left.
        """
        return self._lives

    def getAliensLeft(self):
        """
        Returns the number of aliens left.
        """
        return self._aliensleft

    def getCrossLine(self):
        """
        Returns the _crossline attribute.
        """
        return self._crossline

    def getAlienSpeed(self):
        """
        Returns the _alienspeed attribute.
        """
        return self._alienspeed

    def setAlienSpeed(self,s):
        """
        Set the alien speed to s.

        Parameter s: the desired speed
        Precondition: a number >= 0
        """
        self._alienspeed = s

    def getSounds(self):
        """
        Returns the _sounds attribute.
        """
        return self._sounds

    def setSounds(self,n):
        """
        Set the volume of sounds to n.

        Parameter n: the desired volume
        Precondition: n is either 0 or 1
        """
        for i in self._sounds:
            i.volume = n

    def getScore(self):
        """
        Returns the current score.
        """
        return self._score

    def setScore(self, n):
        """
        Set the score from the previous wave.

        Parameter n: the score needs to be carried over
        Precondition: n is an int >= 0
        """
        self._score = n

    # Three main wave methods
    def __init__(self):
        """
        Initializes the class Wave and its attributes.
        """
        self._aliens = self._aliensList()
        self._ship = Ship(source0='ship.png')
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth=1, linecolor='black')
        self._time = 0
        self._direction = 0
        self._bolts = []
        self._step = random.randrange(1,BOLT_RATE+1)
        self._time2 = 0
        self._lives = SHIP_LIVES
        self._aliensleft = ALIEN_ROWS*ALIENS_IN_ROW
        self._crossline = False
        self._alienscoords = []
        self._alienspeed = ALIEN_SPEED
        self._sounds = [Sound('pew1.wav'),Sound('pop2.wav'),Sound('blast1.wav')]
        self._movesound = [Sound('move1.wav'),Sound('move2.wav'),
                           Sound('move3.wav'),Sound('move4.wav')]
        self._move = 0
        for i in self._movesound:
            self._sounds.append(i)
        self._score = 0

    def update(self,input,dt):
        """
        Animates the ship, aliens, and laser bolts.

        Parameter input: the user input, used to change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        self._shipUpdate(input)
        self._aliensUpdate(dt)
        self._firePlayerBolt(input)
        self._fireAlienBolt(dt)
        self._collision()

    def draw(self,view):
        """
        Draw the ship, aliens, defensive line and bolts.

        Parameter: The view window
        Precondition: view is a GView.
        """
        # draw aliens
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)

        # draw ship
        if self._ship != None:
            self._ship.draw(view)

        # draw dline
        self._dline.draw(view)

        # draw bolts
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS
    def _aliensList(self):
        """
        Create a 2d list of aliens.
        """
        a = []
        y1 = GAME_HEIGHT-ALIEN_CEILING-(ALIEN_V_SEP+ALIEN_HEIGHT)* \
             (ALIEN_ROWS-1)-ALIEN_HEIGHT/2
        for r in range(ALIEN_ROWS):
            b = []
            for i in range(ALIENS_IN_ROW):
                b.append(Alien(x0=ALIEN_WIDTH*(1/2+i)+(i+1)*ALIEN_H_SEP, y0=y1+
                         (ALIEN_H_SEP+ALIEN_HEIGHT)*r, source0=ALIEN_IMAGES[int
                         (r/2)%len(ALIEN_IMAGES)]))
            a.append(b)
        return a

    def _shipUpdate(self,input):
        """
        Update the ship upon key presses.

        Parameter input: the user input, used to change state
        Precondition: instance of GInput; it is inherited from GameApp

        Key press method adopted from arrows.py by Walker M. White
        """
        # detect key press
        da = 0
        if input.is_key_down('right'):
            da += SHIP_MOVEMENT
        if input.is_key_down('left'):
            da -= SHIP_MOVEMENT

        # move the ship
        if self._ship != None:
            self._ship.x += da

            # prevent the ship from moving out of the screen
            if self._ship.x < 0:
                self._ship.x = SHIP_WIDTH/2
            if self._ship.x > GAME_WIDTH:
                self._ship.x = GAME_WIDTH-SHIP_WIDTH/2

    def _aliensMove(self,direction,dt):
        """
        Move the aliens to the left/right with specified speed.

        Parameter direction: specifies the direction the aliens are removing
        Precondition: 0 or 1; 0 for moving right and 1 for moving left

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        if self._time > self._alienspeed:
            self._alienscoords = []
            for r in range(ALIEN_ROWS):
                for c in range(ALIENS_IN_ROW):
                    if self._aliens[r][c] != None:
                        self._aliens[r][c].x += direction
                        self._alienscoords.append((r,c))

            # play the move sound
            self._movesound[self._move].play()
            if self._move <= len(self._movesound)-1:
                self._move += 1
            if self._move == len(self._movesound):
                self._move = 0

            self._time = 0
        else:
            self._time += dt

    def _aliensDown(self):
        """
        Move the aliens down when the end reaches the edge of the screen and
        check to see if it has crossed the defense line.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:

                    # move down
                    alien.y -= ALIEN_V_WALK

                    # counter the horizontal walk
                    if self._direction == 0:
                        alien.x -= ALIEN_H_WALK
                    if self._direction == 1:
                        alien.x += ALIEN_H_WALK

                    # check to see if any aliens crossed the defense line
                    if alien.y-ALIEN_HEIGHT/2 < DEFENSE_LINE:
                        self._crossline = True

    def _aliensUpdate(self,dt):
        """
        Update the aliens using _aliensMove, _aliensDown and _aliensExtreme
        helpers.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        # when aliens are moving right
        if self._direction == 0:
            self._aliensMove(ALIEN_H_WALK,dt)
            if self._alienscoords != []:
                m,n = max(self._alienscoords,key=lambda item:item[1])
                if self._aliens[m][n] != None and self._aliens[m][n].x > \
                GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH/2 and self._direction != 1:
                    self._aliensDown()
                    self._direction = 1

        #when aliens are moving left
        if self._direction == 1:
            self._aliensMove(-ALIEN_H_WALK,dt)
            if self._alienscoords != []:
                m,n = min(self._alienscoords,key=lambda item:item[1])
                if self._aliens[m][n] != None and self._aliens[m][n].x < \
                ALIEN_H_SEP+ALIEN_WIDTH/2 and self._direction != 0:
                    self._aliensDown()
                    self._direction = 0

    def _firePlayerBolt(self,input):
        """
        Fire a bolt upon player pressing the spacebar and delete any off
        offscreen bolt.

        Parameter input: the user input, used to change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        # fire player bolt
        if input.is_key_down('spacebar'):
            try:
                for bolt in self._bolts:
                    assert bolt.isPlayerBolt() == False
                a = Bolt(self._ship.x,SHIP_BOTTOM+SHIP_HEIGHT+BOLT_HEIGHT/2)
                a._playerbolt = True
                self._bolts.append(a)
                self._sounds[0].play()
            except:
                pass
        for bolt in self._bolts:
            if bolt._playerbolt:
                bolt.y += bolt.getVelocity()
            else:
                bolt.y -= bolt.getVelocity()

        # delete any offscreen bolt
        i = 0
        while i < len(self._bolts):
            a = self._bolts[i]
            if a.y-BOLT_HEIGHT/2 > GAME_HEIGHT or a.y+BOLT_HEIGHT/2 < 0:
                del self._bolts[i]
            else:
                i += 1

    def _fireAlienBolt(self,dt):
        """
        Fire a bolt upon from a random alien within self._step

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        if self._time2 > self._step*self._alienspeed:

            #find a nonempty column
            for i in range(ALIENS_IN_ROW):
                b = random.randrange(ALIENS_IN_ROW)
                if not all(v is None for v in [row[b] for row in self._aliens]):
                    break
                else:
                    continue

            #find the bottom alien that's not None
            for i in range(ALIEN_ROWS):
                r = i
                if self._aliens[i][b] != None:
                    break
                else:
                    continue

            #fire the alien bolt
            if self._aliens[r][b] != None:
                a=Bolt(self._aliens[r][b].x,self._aliens[r][b].y-ALIEN_HEIGHT/2)
                a._playerbolt = False
                self._bolts.append(a)
                self._step = random.randrange(1,BOLT_RATE+1)
                self._time2 = 0

        else:
            self._time2 += dt

    def _collision(self):
        """
        Check to see if there's any collision between bolt and alien or bolt and
        ship. Then make changes accordingly.
        """
        for i in self._bolts:

            # when player bolt collides with alien
            if i.isPlayerBolt():
                for r in range(ALIEN_ROWS):
                    for c in range(ALIENS_IN_ROW):
                        if self._aliens[r][c]!= None and \
                        self._aliens[r][c].collides(i):
                            self._aliens[r][c] = None
                            self._aliensleft -= 1
                            self._bolts.remove(i)
                            self._sounds[1].play()
                            self._alienspeed *= SPEED_FACTOR
                            self._score += BASIC_SCORE*(int(r/2)+1)

            # when alien bolt collides with ship
            else:
                if self._ship != None and self._ship.collides(i):
                    self._ship = None
                    self._bolts.remove(i)
                    self._lives -= 1
                    self._sounds[2].play()
