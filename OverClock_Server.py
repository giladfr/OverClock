#! /usr/bin/python

# Gilad's LCD python server
# 4/8/2012

import os
import sys
import serial
import time

CMD_OP = 0xFF
CMD_CLEAR = 0x0A
CMD_BACKLIGHT_OFF = 0xB
CMD_BACKLIGHT_ON = 0xC
CMD_SET_CURSOR = 0xD


class LCDLine(object):
    def __init__(self,num = 0,width = 16):
        self.width = width
        self.str = " " * width

class LCD(object):
    def __init__(self,comport,n_lines = 2,n_col = 16):
        self.n_lines = n_lines
        self.n_col = n_col
        self.ser = serial.Serial(port=comport, baudrate=9600, bytesize=serial.EIGHTBITS,\
                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        self.cur_lines = []
        self.next_lines = []
        for i in range(1,self.n_lines):
            self.cur_lines.append(LCDLine())
            self.next_lines.append(LCDLine())

        time.sleep(1)
        
        

    def write(self,str):
        self.ser.write(str)
    
    def clear(self):
        self._cmd(CMD_CLEAR)

    def set_backlight(self,state):
        if state:
            self._cmd(CMD_BACKLIGHT_ON)
        else:
            self._cmd(CMD_BACKLIGHT_OFF)
    
    def set_cursor(self,col,row):
        self.ser.write(chr(CMD_OP) + chr(CMD_SET_CURSOR) + chr(col) + chr(row))
        
    
    
    def refresh(self):
        # First line is the clock, always update
        self.set_cursor(0,0)
        self.write(time.strftime(" %d/%m %H:%M:%S", time.localtime()))
        line_num = 1
        for n,line in enumerate(self.next_lines):
            if self.next_lines[n].str != self.cur_lines[n].str:
                #self.animate_change(1)
                self.set_cursor(0,line_num)
                self.write(line.str)
                line_num+=1
                self.cur_lines[n].str = line.str

    def animate_change(self,line_num):
        aline = list(" " * self.n_col)
        for i in range(self.n_col):
            aline[i] = "-"
            self.set_cursor(0,line_num)
            self.write("".join(aline))
            time.sleep(0.1)
            
    
    def _cmd(self,cmd):
        self.ser.write(chr(CMD_OP) + chr(cmd))
        
        







class LCDServer(object):
    def __init__(self,lcd):
        self.lcd_update_interval = 1
        self.info_line_interval = 5
        self.lcd = lcd
        # create info lines struct
        pass
    
    def main_loop(self):
        lcd.clear()
        n = 0
        while(1):
            time.sleep(self.lcd_update_interval)
            n += 1
            self.lcd.next_lines[0].str = str(n)
            self.lcd.refresh()
            #lcd.clear()
    
    
#    def animate
    
    
    #def write_info_lines(self):
    #    for num,line in enumerate(self.info_lines):
    #        lcd.set_cursor(0,line.num + 1)
    #        lcd.write(line.str)
            

if __name__ == '__main__':
    lcd = LCD('\\.\COM6')
    srv = LCDServer(lcd)
    srv.main_loop()
    

    #raw_input("Press Enter to continue...")
    #lcd.clear()
    #raw_input("Press Enter to continue...")
    #lcd.write("Crap");
    #raw_input("Press Enter to continue...")
    #lcd.set_cursor(0,0)
    #lcd.write("De La");
    #
    #raw_input("Press Enter to continue...")
    #lcd.write("De La");
    #raw_input("Press Enter to continue...")
    #lcd.clear()
    #raw_input("Press Enter to continue...")
    #lcd.write("Crap");
    #raw_input("Press Enter to continue...")

