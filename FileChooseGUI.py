# -*- coding: utf-8 -*-
import os
from Tkinter import *
import tkMessageBox
from tkFileDialog import *
import multiprocessing
import DisplayObj


class DisPlayObjGUI(Frame):

    def __init__(self, root, **kw):
        Frame.__init__(self, root, **kw)
        self.root = root
        self.file_path_sv = StringVar()
        self.make_main_win()

    def make_main_win(self):
        file_frame = FrameUtil.make_entry_button(self.root, "obj文件", "选择", self.file_path_sv, self.fileopen)
        play_button = FrameUtil.make_button(self.root, "显示", self.display)

        file_frame.grid(row=0, column=0, sticky=W)
        play_button.grid(row=1, column=0)

    def display(self):
        path = self.file_path_sv.get()
        file_type = path.split('.')[-1]
        if not os.path.exists(path):
            tkMessageBox.showerror(u"文件打开失败", u"文件不存在！", parent=self.root)
            return
        if file_type != 'obj':
            tkMessageBox.showerror(u"文件类型错误", u"应选择 .obj 格式文件！", parent=self.root)
            return
        t = multiprocessing.Process(target=DisplayObj.display, args=(path,))
        t.start()

    def fileopen(self):
        file_type = [('obj', 'OBJ')]
        self.file_path_sv.set('')
        print "open file:", os.path.pardir + '/resources/'
        file_name = askopenfilename(filetypes=file_type, initialdir=os.path.pardir + '/resources/')
        if file_name:
            self.file_path_sv.set(file_name)


class FrameUtil:

    @staticmethod
    def make_button(root, text, command):
        button = Button(root, width=20, text=text, command=command)
        return button

    @staticmethod
    def make_entry(root, title, sv):
        frame = Frame(root)
        label = Label(frame, width=20, text=title)
        entry = Entry(frame, width=50, textvariable=sv)
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        return frame

    @staticmethod
    def make_entry_button(root, title, button_text, sv, command):
        frame = Frame(root)
        frame_entry = FrameUtil.make_entry(frame, title, sv)
        button = FrameUtil.make_button(frame, button_text, command)
        frame_entry.grid(row=0, column=0)
        button.grid(row=0, column=1)
        return frame


def main():
    multiprocessing.freeze_support()
    root = Tk()
    root.title("显示模型")
    DisPlayObjGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()