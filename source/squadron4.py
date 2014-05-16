#!/usr/bin/env python

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
For a copy of the license see .
=====================================================================

squadron 4
www.peileppe.com

"""

import curses
from curses import panel
from random import randint

def highscore(w, score, action ):
    if action==ord('q'):
        return
    w=curses.newwin(3,20,11,33)
    wpanel=panel.new_panel(w)
    w.box()
    if score>0:
        msg=" >High Score : "+str(score)
        logo="[4]"
    else:
        msg=" > Failed!"
        logo="[F]"        
    w.addstr(1,1,msg)
    w.addstr(0,0,logo) # adding some kind of gratuitous decoration
    w.move(0,1)    
    w.refresh()
    w.getch()
    del wpanel
    return

def printbox(x, y, x1, y1, ws):
# to draw platforms 
    for py in range(y, y1):
        for px in range(x, x1):
            ws.addch(py, px, "-")
    return

def setDecor(w, xx, yy):
    # generating platforms / obstacles 
    if xx !=80 or yy !=24:
        w.move(0,0) ; w.hline("_",79)
        w.move(23,0) ; w.hline("_",79)
        w.move(0,0) ; w.vline("!",23)
        w.move(0,79) ; w.vline("!",23)
        w.addch(0,0,"+")
        w.addch(0,79,"+")
        w.addch(23,0,"+")        
        w.addch(23,79,"+")        
        xx, yy = 80, 24
    else:
        w.box()
    for y in range(3, yy-3, 3):
        printbox(randint(7,10),y,randint(16,20),y+2,w)
        printbox(randint(37,40),y,randint(46,50),y+2,w)
        printbox(randint(57,60),y,randint(66,70),y+2,w)        
    return xx, yy
    
def screenUpdate(w, score):
    msg="_["+str(score)+"]_"
    w.addstr(0,1,msg)
    w.move(0,0) # get the cursor out of the way        
    w.refresh()
    w.timeout(100)
    return
    
class movingObject(object):    
    def __init__(self, x, y, symbol):
        self.x, self.y, self.symbol=x, y, symbol
        self.alive=True         
        return
        
    def showandClean(self, w, newposx, newposy):
        if self.alive==False:        
            return 0, 0
        w.addch(self.y,self.x,' ')
        w.addch(newposy,newposx,self.symbol)
        return newposx, newposy
#==> end class movingObject

class ball(movingObject):
    def __init__(self, x, y, symbol):
        movingObject.__init__(self, x, y, symbol)
        self.dir_x, self.dir_y=1, 1
        return
        
    def interpretBounce(self, w):
        if self.alive==False:
            return 0,0
        new_x, new_y = self.x+self.dir_x, self.y+self.dir_y
        sane = 0 
        while (w.inch(new_y,new_x) != ord(' ') or \
        new_y not in range(2,23) or \
        new_x not in range(1,78)) and sane < 4 :
            if sane % 2 != 0:
                self.dir_x = -self.dir_x
            else:
                self.dir_y = -self.dir_y
            new_x = self.x+self.dir_x
            new_y = self.y+self.dir_y
            sane += 1
        if sane==4: # move is not possible
            self.alive=False
            new_x, new_y=self.x, self.y 
            w.addch(self.y,self.x,'=') # a dead cell is kept
        return new_x, new_y
#==> end class ball

class magnetBlock(movingObject):
    def __init__(self, x, y, symbol, dir_x, dir_y):
        movingObject.__init__(self, x, y, symbol)
        self.dir_x, self.dir_y= dir_x, dir_y
        return

    def interpretAim(self, w):
        if self.alive==False:
            return 0,0
        new_x, new_y = self.x+self.dir_x, self.y+self.dir_y
        if self.dir_y==0:
            self.symbol='~'
        else:
            self.symbol=':'
        if w.inch(new_y,new_x) != ord(' '):
            self.alive=False
            new_x, new_y=self.x, self.y 
            w.addch(self.y,self.x,'B') # blockMagnet is shown
        return new_x, new_y
#==> end class magnetBlock

class mePlayer(movingObject):
    def __init__(self, x, y, symbol):
        movingObject.__init__(self, x, y, symbol)
        self.dir_x, self.dir_y = 0, 0 # no movement
        self.magnetBlocks=[]
        self.win=0
        return

    def interpretKey(self, w, xx, yy, action, ax, ay, score):
        validspot=(ord(' '), ord('1'), ord('2'), ord('3'), ord('4'))
        if action == curses.KEY_UP and ay > 1 \
        and w.inch(ay-1,ax) in validspot:
            self.dir_y=-1 ; self.dir_x=0 ; ay -=1
        elif action == curses.KEY_DOWN and ay < yy-2 \
        and w.inch(ay+1,ax) in validspot:
            self.dir_y=+1 ; self.dir_x=0; ay +=1
        elif action == curses.KEY_RIGHT and ax < xx-2 \
        and w.inch(ay,ax+1) in validspot:
            self.dir_x=+1 ; self.dir_y=0; ax  +=1
        elif action == curses.KEY_LEFT and ax > 1 \
        and w.inch(ay,ax-1) in validspot:
            self.dir_x=-1 ; self.dir_y=0; ax -=1
        elif action == ord('f') or action == ord(' ') and score > 20: # press fire
            self.magnetBlocks.append(magnetBlock(ax,ay,"~", self.dir_x, self.dir_y ))
            score-=20

        final_spot=w.inch(ay, ax) # check if flag are captured
        if  final_spot == ord('1'): 
            w.addch(23,64, '1')
            self.win+=1
        elif final_spot == ord('2'):
            w.addch(23,68, '2')
            self.win+=1
        elif final_spot == ord('3'):
            w.addch(23,72, '3')
            self.win+=1
        elif final_spot == ord('4'):
            w.addch(23,76, '4')   
            self.win+=1

        if self.win==4: # if all 4 flags are captured
            output=open("squadron4-highscore.txt","a")
            output.write("High Score = ["+str(score)+"]\n")
            output.close()
            return ax, ay, score
            
        for m in self.magnetBlocks: # managing all magnetBlocks in transit
            new_x, new_y = m.interpretAim(w)
            m.x, m.y = m.showandClean(w, new_x, new_y)
            
        return  ax, ay, score
#==> end class mePlayer
    
class chaser(movingObject):
    def interpretChase(self, w, me):
        dx=me.x-self.x
        dy=me.y-self.y
        ch_x, ch_y =self.x, self.y
        if abs(dx) > abs(dy):
            if dx>0 and w.inch(ch_y,ch_x+1) == ord(' ') :
                ch_x +=1
            elif dx<0 and w.inch(ch_y,ch_x-1) == ord(' ') :
                ch_x -=1        
        else:
            if dy>0 and w.inch(ch_y+1,ch_x) == ord(' ') :
                ch_y +=1
            elif dy<0 and w.inch(ch_y-1,ch_x) == ord(' ') :
                ch_y -=1
        return ch_x, ch_y
#==> end class chaser
    
def main(w):
    w=curses.initscr()
    yy, xx = w.getmaxyx() 
    w.keypad(1)
    w.nodelay(1)
    w.clear()
    xx,yy = setDecor(w,xx,yy) # forcing area to be 80x24
    balls=[]
    for i in range(4):
        balls.append(ball(randint(26,34),randint(3,10),'o'))
    chasers=[]
    chasers.append(chaser(randint(64,78), randint(20,22), 'c'))
    chasers.append(chaser(randint(70,75), randint(19,22), 'd'))
    chasers.append(chaser(randint(2,4),randint(18,22), 'e'))
    chasers.append(chaser(randint(64,78), randint(2,20), 'f'))
    # declaring the cursor controlled by player
    me  = mePlayer(xx/2-1,yy/2-1,'@')  
    # preparing the 4 flags in the area and receptacles on status line
    w.addstr(2, 7, '[1]')
    w.addstr(2, 60,'[2]')
    w.addstr(20, 7, '[3]')
    w.addstr(20,60, '[4]')
    w.addstr(23,63, '[ ]_[ ]_[ ]_[ ]') 
    scoreMagnet = 1000 # countdown initialized
    action= None
    while action!=ord('q') and me.win<4 and scoreMagnet>0:
        action=w.getch()
        me_x, me_y, scoreMagnet=me.interpretKey(w, xx, yy, action, me.x, me.y, scoreMagnet)
        me.x, me.y=me.showandClean(w, me_x, me_y)        
        for b in balls:
            new_x, new_y = b.interpretBounce(w)
            b.x, b.y = b.showandClean(w, new_x, new_y)
        for c in chasers:
            ch_x, ch_y = c.interpretChase(w, me)
            c.x, c.y= c.showandClean(w, ch_x, ch_y)
        screenUpdate(w, scoreMagnet)
        scoreMagnet -= 1
    highscore(w,scoreMagnet, action)
    curses.endwin()

if __name__ == '__main__':                                                       
    curses.wrapper(main)
