# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 11:30:56 2018
@author: x00428488
"""

import os
import sys
import json
from PIL import Image, ImageFont, ImageDraw
import win32api
import win32con
import win32gui
import random
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import threading
from tkinter import Tk, Label
from tkinter import StringVar
import tkinter as tk
from tkinter import ttk


root = Tk(screenName="WallPaper")
poem_text = StringVar()


def reformat(string):
    string_lst = string.splitlines()
    format_string = []
    for line in string_lst:
        for i in range(len(line) // 25 + 1):
            format_string.append(line[i * 25:25 * (i + 1)])
    return '\n'.join(format_string)


def set_wallpaper_from_bmp(bmp_path):

    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


def random_poems(poet_files):
    poet_file = random.choice(poet_files)
    with open(poet_file, 'r', encoding='utf-8') as json_file:
        poems = json.load(json_file)
    poem = random.choice(poems)
    poem_content = poem['paragraphs'][0]
    poem['paragraphs'] = [reformat(poem_content)]
    poem_string = '\n'.join(
        [poem['title'], poem['author']] + poem['paragraphs'])
    return poem_string


def set_wallpaper(img_files, poem_files, fonts_dir):
    global text
    # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    img_path = random.choice(img_files)
    img_dir = os.path.dirname(img_path)
    bmpImage = Image.open(img_path)
    bmpImage = bmpImage.resize((1920, 1080), Image.ANTIALIAS)
    draw = ImageDraw.Draw(bmpImage)
    font = random.choice([os.path.join(fonts_dir, file)
                          for file in os.listdir(fonts_dir)])
    # print(font)
    fnt = ImageFont.truetype(font, 40)
    poem_str = random_poems(poem_files)

    poem_text.set(poem_str)
    print(poem_str)

    width, height = bmpImage.size
    draw.multiline_text((width / 4, height / 5), poem_str, fill='#000000',
                        font=fnt, anchor='center', spacing=10, align="center")
    new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    bmpImage.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(os.path.abspath(new_bmp_path))


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    # poet_path = 'json'
    pic_path = os.path.join(bundle_dir, 'bgpics')
    # poet_files = [os.path.join(poet_path, file) for file in os.listdir(poet_path)
    #               if 'poet' in file]
    pic_files = [os.path.join(pic_path, file) for file in os.listdir(pic_path)
                 if 'wallpaper' not in file]

    poet_files = [os.path.join(bundle_dir, 'mottos.json')]
    fonts_dir = os.path.join(bundle_dir, 'fonts')

    set_wallpaper(pic_files, poet_files, fonts_dir)

    scheduler = BlockingScheduler()
    trigger_interval = IntervalTrigger(seconds=60)
    scheduler.add_job(set_wallpaper, args=(pic_files, poet_files, fonts_dir),
                      trigger=trigger_interval)  # 设置间隔时间
    # scheduler.add_job(set_wallpaper, args=(pic_files, poet_files,),
    #                   trigger='interval', seconds=120)  # 设置间隔时间
    # scheduler.start()

    def start_bg():
        global scheduler
        # print(scheduler.state)
        if not scheduler.state:
            set_wallpaper(pic_files, poet_files, fonts_dir)
            scheduler = BlockingScheduler()
            scheduler.add_job(set_wallpaper, args=(pic_files, poet_files, fonts_dir),
                              trigger=trigger_interval)  # 设置间隔时间
            t = threading.Thread(target=scheduler.start)
            t.start()
            print("started...")

    def stop_bg():
        global scheduler
        # print(scheduler.state)
        if scheduler.state:
            scheduler.shutdown()
            print("stopped...")

    def random_bg():
        set_wallpaper(pic_files, poet_files, fonts_dir)

    root.title('WallPaper')
    root.geometry('700x400+400+100')
    root.iconbitmap(os.path.join(bundle_dir, 'panda.ico'))
    root.option_add('*tearOff', False)
    lb = Label(root, relief='flat',
               textvariable=poem_text, font=('宋体', 20, 'bold'),
               bg='honeydew', fg='olive')
    lb.pack(expand=True, fill=tk.BOTH)
    style1 = ttk.Style()
    style1.configure("TButton", padding=0, relief='flat', font=('times', 12, 'bold italic'),
                     background='honeydew', foreground='olive')
    startbtn = ttk.Button(lb, text='Start', width=8,
                          cursor='hand2', command=start_bg, style="TButton")
    startbtn.pack(anchor="ne",)
    stopbtn = ttk.Button(
        lb, text='Stop', command=stop_bg, width=8, cursor='hand2', style="TButton")
    stopbtn.pack(anchor="ne")
    randombtn = ttk.Button(lb, text='Random', width=8,
                           cursor='hand2', command=random_bg, style="TButton")
    randombtn.pack(anchor="ne",)
    root.mainloop()
    if scheduler.state:
        scheduler.shutdown()
