# Squadron4 #

A very basic platform game written in **Python 2.7** using the standard **curses** library - with only one level.

**Work best with a terminal window of 80x24**

The goal of this game is for the player ('@') to collect the four flags '1','2','3' and '4' ; and to avoid or trap the chasers (symbols : 'c', 'd', 'e', 'f') ; to render the flag collection a little bit more challenging in the middle area 4 balls are bouncing endlessly and can't be destroyed (but they can be trapped)

- the task has to be done before the countdown (which start at 1000) reach 0.

When the player decides to use a "magnet block" (by pressing 'f' or space bar) the countdown is reduced by 20, so part of the tactic is to use them wisely.

When the four flags are collected - are seen in the lower status bar - the game ends, and the high score is presented.

A tactic to win, is to use the obstacle blocks, or to launch some magnet blocks to trap the chasers, if the chasers are getting too close, they will prevent the player's movements, or may actually completely prevents all movements ; then the only option is to quit the game, or to wait for the countdown to reach 0.

![https://squadron4-game.googlecode.com/hg/screenshot/squadron4-win.png](https://squadron4-game.googlecode.com/hg/screenshot/squadron4-win.png)

The idea of the game is to see the interaction between 4 different moving objects :
  * one controlled by the player (symbol : '@')
  * 4 bouncing balls (symbol : 'o')
  * 4 chasers that will track the player (symbols : 'c', 'd', 'e', 'f')
  * and magnet blocks fired by the player to trap the chasers (symbol : 'B')

Keys for the player '@' :
  * Arrow keys to move
  * 'f' or space bar to launch a magnet Block
  * 'q' to Quit the program

NB : A port of this text-based game into a graphical based version is available at :
  * https://code.google.com/p/squadron4g/