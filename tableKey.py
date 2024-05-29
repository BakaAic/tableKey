try:
    import pyglet,pystray,fontTools,keyboard
except:
    import pip
    pip.main(['install','pyglet','pystray','fontTools','keyboard'])
from tkinter import *
from tkinter.ttk import *
from tkinter import font
import pyglet
from fontTools.ttLib import TTFont
import keyboard
import random
from PIL import Image
from pystray import MenuItem as item,Menu as mu
import pystray
import threading
import traceback
import pickle
import base64
import os

KEYCOLOR='#FFFFFF'
fuchsia = '#0A0F0C'
key_trans={'up':'↑','down':'↓','left':'←','right':'→','backspace':'BackSpace',
           'alt':'Alt','right alt':'Alt','ctrl':'Ctrl','right ctrl':'Ctrl',
           'shift':'Shift','right shift':'Shift','left windows':'Win',
           'space':'Space','menu':'Menu','enter':'Enter','esc':'Esc',
           'f1':'F1','f2':'F2','f3':'F3','f4':'F4','f5':'F5','f6':'F6',
           'f7':'F7','f8':'F8','f9':'F9','f10':'F10','f11':'F11','f12':'F12',
           'print screen':'PrtSc','scroll lock':'ScrLk','pause':'Pause',
           'insert':'Insert','home':'Home','page up':'PgUp','page down':'PgDn',
           'delete':'Delete','end':'End','tab':'Tab','caps lock':'CapsLock',
           'num lock':'NumLock',
           }

save_key=['ctrl','alt','shift','right ctrl','right shift','right alt','Ctrl','Alt','Shift']

class Color:
    @property
    def randomColor(self):
        return self._randomColor()
    
    def _randomColor(self):
        R=random.randint(0,255)
        G=random.randint(0,255)
        B=random.randint(0,255)
        _rgb='#'+hex(R)[2:].zfill(2)+hex(G)[2:].zfill(2)+hex(B)[2:].zfill(2)
        if _rgb==fuchsia:
            return self._randomColor()
        return _rgb
    
    @property
    def randomColorSpecial(self):
        return random.choice(['#442335','#6D4E60','#8C6A86'])
    
colorObject=Color()

class KeyBoardListener():
    def __init__(self,max_count=2):
        self.queue = []
        self.max_count=max_count
    
    def putQueue(self,key):
        self.queue.append(key)
        if len(self.queue)>self.max_count:
            self.queue.pop(0)
    
    def getQueue(self):
        if len(self.queue) == 0:
            return None
        else:
            return self.queue.pop(0)
class KeyFont:
    path=None
    size=25
    defaultFont=None
    curFont=None
    fontList=[None,'system']
    
    @classmethod
    def setFont(cls,font):
        cls.curFont=font
    
    @classmethod
    def getFont(cls):
        if cls.curFont==None:
            return cls.defaultFont
        else:
            return cls.curFont
        
    @classmethod
    def getFontList(cls):
        return cls.fontList
    
    @classmethod
    def loadLocalFont(cls):
        pyglet.options['win32_gdi_font']=True
        cls.path=os.getcwd()+'\\fonts\\'
        if os.path.isdir(cls.path):
            dir=os.listdir(cls.path)
            if dir:
                for f in dir:
                    _font=TTFont(cls.path+f)
                    font_name=_font['name'].getDebugName(1)
                    pyglet.font.add_file(cls.path+f)
                    cls.fontList.append(font_name)
        else:
            os.mkdir(cls.path)

class KeyObj:
    def __init__(self,root,pos,key,color=KEYCOLOR,move=2,loss=8,rsize=8):
        self.root=root
        self.pos=pos
        self.key=self.keyTrans(key)
        self.transparency=255
        if color=='random':
            self.color=colorObject.randomColor
        elif color=='random2':
            self.color=colorObject.randomColorSpecial
        else:
            self.color=color
        self.disapear=False
        self.size=30
        self.rsize=rsize
        self.move=move
        self.loss=loss
        self.build()
        
    def keyTrans(self,key):
        if key in key_trans:
            return key_trans[key]
        else:
            return key
        
    def build(self):
        self.obj=Toplevel(self.root,background=fuchsia)
        self.obj.overrideredirect(1)
        self.obj.attributes('-topmost',True)
        self.obj.attributes('-transparentcolor',fuchsia)
        self.obj.geometry(f'{self.size*self.rsize}x{self.size*3}+{self.pos[0]}+{self.pos[1]}')
        self.font=font.Font(family=KeyFont.getFont(),size=self.size)
        _Label=Label(self.obj,text=self.key,foreground=self.color,background=fuchsia,font=self.font)
        _Label.place(anchor=CENTER,relx=0.5,rely=0.5)
        
    def draw(self):
        return self.obj
    
    def destroy(self):
        self.obj.destroy()
    
    def update(self,move=None,loss=None):
        if move==None:
            move=self.move
        if loss==None:
            loss=self.loss
        self.pos=(self.pos[0],self.pos[1]-move)
        self.obj.geometry(f'{self.size*self.rsize}x{self.size*3}+{self.pos[0]}+{self.pos[1]}')
        self.transparency-=loss
        if self.transparency<=0:
            self.transparency=0
            self.disapear=True
            
        self.obj.attributes('-alpha',self.transparency/255)
        self.obj.update()

class KeyboardPos:
    def __init__(self):
        self.key_pos={'esc':(69,516),
                      'f1':(239,516),
                      'f2':(326,516),
                      'f3':(404,516),
                      'f4':(489,516),
                      'f5':(614,516),
                      'f6':(696,516),
                      'f7':(781,516),
                      'f8':(866,516),
                      'f9':(988,516),
                      'f10':(1080,516),
                      'f11':(1158,516),
                      'f12':(1243,516),
                      'print screen':(1343,516),
                      'scroll lock':(1427,516),
                      'pause':(1512,516),
                      '`':(53,625),'~':(53,625),
                      '1':(139,625),'!':(139,625),
                      '2':(225,625),'@':(225,625),
                      '3':(310,625),'#':(310,625),
                      '4':(396,625),'$':(396,625),
                      '5':(481,625),'%':(481,625),
                      '6':(563,625),'^':(563,625),
                      '7':(651,625),'&':(651,625),
                      '8':(738,625),'*':(738,625),
                      '9':(812,625),'(':(812,625),
                      '0':(902,625),')':(902,625),
                      '-':(990,625),'_':(990,625),
                      '=':(1074,625),'+':(1074,625),
                      'backspace':(1204,625),
                      'insert':(1350,625),
                      'home':(1434,625),
                      'page up':(1520,625),
                      'num lock':(1626,625),
                      'tab':(67,713),
                      'q':(180,713),'Q':(180,713),
                      'w':(264,713),'W':(264,713),
                      'e':(359,713),'E':(359,713),
                      'r':(436,713),'R':(436,713),
                      't':(520,713),'T':(520,713),
                      'y':(603,713),'Y':(603,713),
                      'u':(690,713),'U':(690,713),
                      'i':(776,713),'I':(776,713),
                      'o':(862,713),'O':(862,713),
                      'p':(946,713),'P':(946,713),
                      '[':(1034,713),'{':(1034,713),
                      ']':(1120,713),'}':(1120,713),
                      '\\':(1123,713),'|':(1123,713),
                      'delete':(1352,713),
                      'end':(1439,713),
                      'page down':(1523,713),
                      'caps lock':(67,803),
                      'a':(189,803),'A':(189,803),
                      's':(277,803),'S':(277,803),
                      'd':(363,803),'D':(363,803),
                      'f':(451,803),'F':(451,803),
                      'g':(537,803),'G':(537,803),
                      'h':(629,803),'H':(629,803),
                      'j':(708,803),'J':(708,803),
                      'k':(791,803),'K':(791,803),
                      'l':(881,803),'L':(881,803),
                      ';':(971,803),':':(971,803),
                      '\'':(1053,803),'"':(1053,803),
                      'enter':(1203,803),
                      'shift':(65,890),
                      'z':(221,890),'Z':(221,890),
                      'x':(307,890),'X':(307,890),
                      'c':(394,890),'C':(394,890),
                      'v':(488,890),'V':(488,890),
                      'b':(574,890),'B':(574,890),
                      'n':(660,890),'N':(660,890),
                      'm':(751,890),'M':(751,890),
                      ',':(837,890),'<':(837,890),
                      '.':(925,890),'>':(925,890),
                      '/':(1014,890),'?':(1014,890),
                      'right shift':(1199,890),
                      'up':(1446,803),
                      'ctrl':(52,985),
                      'left windows':(140,985),
                      'alt':(249,985),
                      'space':(594,985),
                      'right alt':(917,985),
                      'menu':(1135,985),
                      'right ctrl':(1246,985),
                      'left':(1367,985),
                      'down':(1453,985),
                      'right':(1550,985),
                      }
        # self.key_pos={}
    def __getitem__(self,i):
        if i in self.key_pos:
            return self.key_pos[i],False
        else:
            return (random.randint(1,300),random.randint(40,160)),True

class TableMan:
    def __init__(self,listener):
        self.base_pos=None
        self.key_pos=KeyboardPos()
        self.keyBoardListener=listener
        self.configColorWindow=False
        self.screen_width = None
        self.screen_height = None
        self.x_offset=-500
        self.y_offset=-400
        self.objs=[]
        self.easterEgg=[]
        self.enabled_status=True
        
    def offset(self,pos,offset=True):
        if offset:
            return (self.base_pos[0]+pos[0],self.base_pos[1]+pos[1])
        else:
            return pos
        
    def quit_window(self,icon,item):
        icon.stop()
        self.root.destroy()
        
    def colorChange(self,color):
        global KEYCOLOR
        match color:
            case 'white':
                KEYCOLOR='#FFFFFF'
            case 'black':
                KEYCOLOR='#000000'
            case 'red':
                KEYCOLOR='#FF0000'
            case 'blue':
                KEYCOLOR='#0000FF'
            case 'yellow':
                KEYCOLOR='#FFFF00'
            case 'green':
                KEYCOLOR='#00FF00'
            case 'random':
                KEYCOLOR='random'
            case 'random2':
                KEYCOLOR='random2'
            case _:
                KEYCOLOR=color
               
    def iconPic(self):
        return 'gASVSkkAAAAAAACMElBJTC5QbmdJbWFnZVBsdWdpbpSMDFBuZ0ltYWdlRmlsZZSTlCmBlF2UKH2UKIwDZHBplEdAWADEm6XjVEdAWADEm6XjVIaUjBFYTUw6Y29tLmFkb2JlLnhtcJRoAIwEaVRYdJSTlFi0BgAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTAxLTI3VDIxOjE4OjE3KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNS0yM1QxMjoyMDowNCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNS0yM1QxMjoyMDowNCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo0ZjljYmJjZS1hOTU3LTM3NDQtYWNkYy01ZGY3OTkxYTBlM2MiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDowYmI4ZmRjNy00ZmFmLTc2NGUtOTRkMS0wZTI5NjIyNzhkNzciIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpiMTNhYjUyYi1iZjcyLTliNDQtOTNjYy0xMDhlNjFlMjBiNzMiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmIxM2FiNTJiLWJmNzItOWI0NC05M2NjLTEwOGU2MWUyMGI3MyIgc3RFdnQ6d2hlbj0iMjAyMi0wMS0yN1QyMToxODoxNyswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo3MGI3NjM4OC0yYjEyLTVkNDUtYThiOS01YTkyNjU4ZGU2OTIiIHN0RXZ0OndoZW49IjIwMjItMDEtMjdUMjE6MzY6NTMrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE5IChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NGY5Y2JiY2UtYTk1Ny0zNzQ0LWFjZGMtNWRmNzk5MWEwZTNjIiBzdEV2dDp3aGVuPSIyMDI0LTA1LTIzVDEyOjIwOjA0KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+lIWUgZR9lCiMBGxhbmeUjACUjAR0a2V5lGgQdWJ1jARSR0JBlEtDSz+GlE5C9EEAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8P/j6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8P/j6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/D/4+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AAAAAAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wAAAAAA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/D/////wD///8A////AI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/D/4+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vw/+Pr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8MAj6/DAI+vw/+Pr8P/j6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAAAAADY+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vw/+Pr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8P/j6/D/4+vw/+Pr8P/j6/D/4+vwwCPr8P/j6/DAI+vwwCPr8P/j6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/D/4+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/D/4+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MA////AP///wD///8Aj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/D/4+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vw/+Pr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAP///wD///8A////AI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8P/j6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwCPr8MAj6/DAI+vwwD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AJRlYi4='
              
    def run(self):
        self.root=Tk()
        self.screen_width=self.root.winfo_screenwidth()
        self.screen_height=self.root.winfo_screenheight()
        self.base_pos=(self.screen_width+self.x_offset,self.screen_height+self.y_offset)
        self.root.overrideredirect(1)
        self.root.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        self.root.title('')
        self.root.resizable(0,0)
        self.root.attributes('-topmost',True)
        self.root.attributes('-transparentcolor',fuchsia)
        self.table=Canvas(self.root,width=self.screen_width,height=self.screen_height,highlightthickness=0,bg=fuchsia)
        self.table.pack(fill=BOTH)
        
        KeyFont.loadLocalFont()
        
        image=pickle.loads(base64.b64decode((self.iconPic().encode())))
        self.menu=[item('颜色:白色',lambda:self.colorChange('white'),default=True,radio=True),
              item('颜色:黑色',lambda:self.colorChange('black'),radio=True),
              item('颜色:红色',lambda:self.colorChange('red'),radio=True),
              item('颜色:蓝色',lambda:self.colorChange('blue'),radio=True),
              item('颜色:黄色',lambda:self.colorChange('yellow'),radio=True),
              item('颜色:绿色',lambda:self.colorChange('green'),radio=True),
              item('颜色:随机色',lambda:self.colorChange('random'),radio=True),
              item('颜色:高贵随机紫',lambda:self.colorChange('random2'),radio=True),
              item('颜色:自定义',self.configColor,radio=True),
              mu.SEPARATOR
              ]
        for f in KeyFont.getFontList():
            self.menu.append(item('字体:'+str(f),self.setFont_wrap(f)))
        self.menu.append(mu.SEPARATOR)
        self.menu.append(item('是否生效',self.enabled_switch))
        self.menu.append(mu.SEPARATOR)
        self.menu.append(item('退出',self.quit_window))
        self.menu=tuple(self.menu)
        
        icon=pystray.Icon('tableKey',image,'tableKey',self.menu)
        threading.Thread(target=icon.run,daemon=True).start()

        self.root.after(10,self.update)
        self.root.mainloop()
        
    def enabled_switch(self):
        self.enabled_status=not self.enabled_status
        
    def configColor(self,*args):
        if not self.configColorWindow:
            self.configColorWindow=True
            self.top=Toplevel(self.root)
            self.top.geometry('200x100')
            self.top.resizable(0,0)
            self.top.attributes('-topmost',1)
            self.top.attributes('-toolwindow',1)
            self.top.bind('<Destroy>',self.closeColorConf)
            self.top.title('修改字体颜色')
            self.e=Entry(self.top,width=22)
            self.e.grid(row=0,column=0,padx=15,pady=15)
            submit=Button(self.top,text='修改',width=18,command=self.colorChangeCheck)
            submit.grid(row=1,column=0,padx=15,pady=5)
        
    def colorChangeCheck(self):
        checkStr='0123456789ABCDEF'
        ret=self.e.get().upper()
        if len(ret)==7 and ret[0]=='#' and ret[1] in checkStr and ret[2] in checkStr and ret[3] in checkStr \
            and ret[4] in checkStr and ret[5] in checkStr and ret[6] in checkStr:
            self.colorChange(ret)
            self.configColorWindow=False
            self.top.destroy()
        else:
            self.e.delete(0,END)
        
    def closeColorConf(self,event):
        self.configColorWindow=False
        
    def setFont_wrap(self,f):
        def wrap():
            return KeyFont.setFont(f)
        return wrap
        
    def update(self):
        self.eventLoop()
        removeobj=[]
        for obj in self.objs:
            obj.update()
            if obj.disapear:
                obj.destroy()
                removeobj.append(obj)
        for obj in removeobj:
            self.objs.remove(obj)
        self.root.after(10,self.update)
        
    def keyBoardEvent(self,key):
        try:
            if self.enabled_status:
                if key in save_key:
                    for k in self.objs:
                        if k.keyTrans(key)==k.key:
                            break
                    else:
                        self.objs.append(KeyObj(self.root,self.offset(*self.key_pos[key]),key,KEYCOLOR))
                else:
                    self.objs.append(KeyObj(self.root,self.offset(*self.key_pos[key]),key,KEYCOLOR))
        except:
            with open('error.log','a+') as f:
                traceback.print_exc(file=f)
    
    def easterEggTrigger(self,types):
        s=''
        if types==1:
            s='♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥'
        elif types==2:
            s='你已获得无敌!'
        self.objs.append(KeyObj(self.root,(self.screen_width//2-1000,self.screen_height//2),s,KEYCOLOR if types!=1 else '#FF0000',move=1,loss=1,rsize=64))
    
    def easterEggQueue(self,key):
        if key in ['up','down','left','right','b','B','a','A','w','h','o','i','s','y','u','r','d']:
            self.easterEgg.append(key)
        if len(self.easterEgg)>20:
            self.easterEgg.pop(0)
        match self.easterEgg[-10:]:
            case ['up','up','down','down','left','right','left','right','b'|'B','a'|'A']:
                self.easterEggTrigger(1)
                self.easterEgg.clear()
            case _:
                pass
        match self.easterEgg[-14:]:
            case ['w','h','o','i','s','y','o','u','r','d','a','d','d','y']:
                self.easterEggTrigger(2)
                self.easterEgg.clear()
            case _:
                pass
        match self.easterEgg[-13:]:
            case ['w','h','o','s','y','o','u','r','d','a','d','d','y']:
                self.easterEggTrigger(2)
                self.easterEgg.clear()
            case _:
                pass
                
    def eventLoop(self):
        key_event=self.keyBoardListener.getQueue()
        self.easterEggQueue(key_event)
        if key_event:
            self.keyBoardEvent(key_event)
           

keyboard_listen=KeyBoardListener()
keyboard.on_press(lambda key:keyboard_listen.putQueue(key.name))

main=TableMan(keyboard_listen)
main.run()
