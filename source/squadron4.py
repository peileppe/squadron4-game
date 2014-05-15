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
www.peileppe.com          
"""

import curses
from random import randint

def printbox(x, y, x1, y1, ws):
    # to draw platforms 
    for py in range(y, y1):
        for px in range(x, x1):
            ws.addch(py, px, "-")
    return

def setDecor(w, xx, yy):
    # generating platforms / obstacles 
    for y in range(3, yy, 3):
        printbox(10,y,20,y+2,w)
        printbox(40,y,50,y+2,w)
    return
    
def screenUpdate(w, maxTurn):
    msg="__["+str(maxTurn)+"]__"
    w.addstr(0,0,msg)
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
        if sane==4:
            self.alive=False
            new_x, new_y=self.x, self.y 
            w.addch(self.y,self.x,'=') # a block is kept
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
            w.addch(self.y,self.x,'B') # boom
        return new_x, new_y
#==> end class magnetBlock

class mePlayer(movingObject):
    def __init__(self, x, y, symbol):
        movingObject.__init__(self, x, y, symbol)
        self.dir_x, self.dir_y = 0, 0 # no movement
        self.magnetBlocks=[]
        return

    def interpretKey(self, w, xx, yy, action, ax, ay):
        if action == curses.KEY_UP and ay > 1 \
        and w.inch(ay-1,ax) == ord(' '):
            self.dir_y=-1 ; self.dir_x=0 ; ay -=1
        elif action == curses.KEY_DOWN and ay < yy-2 \
        and w.inch(ay+1,ax) == ord(' '):
            self.dir_y=+1 ; self.dir_x=0; ay +=1
        elif action == curses.KEY_RIGHT and ax < xx-2 \
        and w.inch(ay,ax+1) == ord(' '):
            self.dir_x=+1 ; self.dir_y=0; ax  +=1
        elif action == curses.KEY_LEFT and ax > 1 \
        and w.inch(ay,ax-1) == ord(' '):
            self.dir_x=-1 ; self.dir_y=0; ax -=1
        elif action == ord('f') or action == ord(' '): # press fire
            self.magnetBlocks.append(magnetBlock(ax,ay,"~", self.dir_x, self.dir_y ))

        for m in self.magnetBlocks:
            new_x, new_y = m.interpretAim(w)
            m.x, m.y = m.showandClean(w, new_x, new_y)
            
        return  ax, ay
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
    w.keypad(1)
    w.nodelay(1)
    w.clear()
    w.border()
    yy, xx = w.getmaxyx()  
    setDecor(w,xx,yy)
    balls=[]
    for i in range(4):
        balls.append(ball(randint(26,34),randint(3,10),'o'))
    chasers=[]
    chasers.append(chaser(randint(60,78), randint(20,22), 'c'))
    chasers.append(chaser(randint(70,75), randint(19,22), 'd'))
    chasers.append(chaser(randint(2,4),randint(18,22), 'e'))
    chasers.append(chaser(randint(60,78), randint(2,20), 'f'))
    me  = mePlayer(xx/2-1,yy/2-1,'@')  
    # the one controlled by player - using key
    maxTurn = 0 
    action= None
    while action!=ord('q'):
        action=w.getch()
        me_x, me_y=me.interpretKey(w, xx, yy, action, me.x, me.y)
        me.x, me.y=me.showandClean(w, me_x, me_y)        
        for b in balls:
            new_x, new_y = b.interpretBounce(w)
            b.x, b.y = b.showandClean(w, new_x, new_y)
        for c in chasers:
            ch_x, ch_y = c.interpretChase(w, me)
            c.x, c.y= c.showandClean(w, ch_x, ch_y)
        screenUpdate(w, maxTurn)
        maxTurn += 1
    w.getch()
    curses.endwin()

if __name__ == '__main__':                                                       
    curses.wrapper(main)
