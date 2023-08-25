#!/bin/env python3
import os
import signal
import copy
# pip3 install getch
from getch import getch

def sig_handler(signum, frame):
    pass

class VtColor():
    CONFIG = '.vtcolor'
    def __init__(self):
        self.homedir = os.path.expanduser("~")
        self.configfile = os.path.join(self.homedir, self.CONFIG)
        self.read_settings()
    
    def read_settings(self):
        # デフォルト値
        self.config = {
            'VTBACKGROUND': [0,0,0]
        }
        try:
            with open(self.configfile, 'r') as f:
                for line in f:
                    kv = line.split('=')
                    title = kv[0]
                    val = [
                        int(kv[1][1:3], 16),
                        int(kv[1][3:5], 16),
                        int(kv[1][5:7], 16)
                    ]
                    self.config[title] = val
        except FileNotFoundError:
            pass
        except Exception:
            raise
        # 設定値のバックアップ
        self.config_backup = copy.deepcopy(self.config)

    def write_settings(self):
        with open(self.configfile, 'w') as f:
            for k,val in self.config.items():
                f.write(f'{k}=#{val[0]:02x}{val[1]:02x}{val[2]:02x}\n')

    def loop(self):
        # ctrl+Cでgetchが例外を出力するためSIGINTを無効化
        signal.signal(signal.SIGINT, sig_handler)
        try:
            max_changepos = 3 * 3 - 1
            title = 'VTBACKGROUND'
            changepos = 2
            # メインループ
            update = True
            end = False
            while not end:
                if update:
                    val = self.config[title]
                    line = f'{title} {val[0]:>3} {val[1]:>3} {val[2]:>3}'
                    curpos = self.changepos2curpos(title, changepos)
                    self.printline(line, curpos)
                    update = False
                c = getch()
                if c == '\x0a':
                    end = True
                    ret = 0
                elif c == '\x1b':
                    c = getch()
                    if c == '\x1b':
                        end = True
                        ret = 1
                    elif c == '[':
                        c = getch()
                        if c == 'A':
                            # UP
                            self.inc_val(title, changepos)
                            update = True
                        elif c == 'B':
                            # DOWN
                            self.dec_val(title, changepos)
                            update = True
                        elif c == 'C':
                            # RIGHT
                            changepos = changepos + 1
                            if (changepos > max_changepos):
                                changepos = 0
                            update = True
                        elif c == 'D':
                            # LEFT
                            changepos = changepos - 1
                            if (changepos < 0):
                                changepos = max_changepos
                            update = True
            # 改行出力
            print('')
            return ret
        except Exception:
            # 改行出力
            print('')
            return 1

    def printline(self, line, curpos):
        print('\r' + line + '\r' + line[:curpos], end="", flush=True)

    def changepos2curpos(self, title, changepos):
        val_no = int(changepos / 3)
        digit = changepos % 3
        curpos = len(title) + val_no* 4 + digit + 1
        return curpos
    
    def inc_val(self, title, changepos):
        val_no = int(changepos / 3)
        digit = changepos % 3
        n = 10 ** (2 - digit)
        self.config[title][val_no] = min(self.config[title][val_no] + n, 255)
        self.apply_color()

    def dec_val(self, title, changepos):
        val_no = int(changepos / 3)
        digit = changepos % 3
        n = 10 ** (2 - digit)
        self.config[title][val_no] = max(self.config[title][val_no] - n, 0)
        self.apply_color()

    def apply_color(self):
        val = self.config['VTBACKGROUND']
        self.set_vtcolor(val)
    
    def set_vtcolor(self, val):
        print(f'\x1b]11;#{val[0]:02x}{val[1]:02x}{val[2]:02x}\x1b\\', end="", flush=True)

    def restore(self):
        self.config = copy.deepcopy(self.config_backup)
        self.apply_color()


def main():
    c = VtColor()
    if c.loop() == 0:
        c.write_settings()
    else:
        c.restore()

if __name__ == '__main__':
    main()
        
