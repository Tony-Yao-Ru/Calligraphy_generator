from bs4 import BeautifulSoup
import requests as re
import re as req
import tkinter as tk
import os
from PIL import Image, ImageTk

def send_request():
    r = re.post(url, headers = header, data=datas)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("img")
    file_name = tag[0].get('src').split('/')[1]
    new_url = url + tag[0].get('src')
    png_arr.append(file_name)
    r = re.get(new_url, stream=True)
    file = open(file_name, 'wb')
    file.write(r.content)
    file.close()

def create_package(str1, str2):
    header = {'Content-encoding': 'gzip',\
    'user-agent': 'Mozilla/5.0 (Macintosh; \
    Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0'}

    datas["word"] = str1
    datas["fonts"] = str2
    datas["sizes"] = '60'
    datas["fontcolor"] = '#000000'
    datas["colors"] = '#FFFFFF'
    datas["touming"] = 'on'

def define_layout(obj, cols=1, rows=1):
    def method(trg, col, row):
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)
    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows) 

class Window_for_newCall:
    def __init__(self, master, num_index, new_enter_word):
        self.master = master
        self.num_index = num_index
        self.new_enter_word = new_enter_word
        self.master.title("Choose new calligraphy")
        self.reg1 = tk.Frame(master,  width=img_size , height=img_size , bg='blue')
        self.reg2 = tk.Frame(master,  width=img_size , height=img_size , bg='blue')

        #smallwin_size = min( master.winfo_width(), master.winfo_height())
        self.reg1.grid(column=0, row=0, padx=pad, pady=pad, columnspan=1, sticky=align_mode)
        self.reg2.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)

        define_layout(master, cols=1, rows=1)
        define_layout([self.reg1, self.reg2])

        state = 'No\t' + new_enter_word + '\tin this calligraphy'
        self.labl2 = tk.Label(self.reg1, text = state, height=10 )
        self.labl2.grid(column=0, row=0, sticky=align_mode)

        self.OptionList2 = url_arr
        self.Opt2 = tk.StringVar()
        self.Opt2.set("Calligraphy")
        self.Optmenu2 = tk.OptionMenu(self.reg2, self.Opt2, *self.OptionList2, self)
        self.Optmenu2.grid(column=0, row=0, sticky=align_mode)

        self.btn1 = tk.Button(self.reg2, text='Enter', bg='green', fg='black', command=self.choose_new)
        self.btn2 = tk.Button(self.reg2, text='Exit', bg='green', fg='black', command=self.leave)

        self.btn1.grid(column=1, row=0, sticky=align_mode)
        self.btn2.grid(column=2, row=0, sticky=align_mode)

        define_layout(master, cols=3, rows=3)
        define_layout(self.reg1)
        define_layout(self.reg2, rows=1)

    def choose_new(self):
        new_style = url_arr_name[int(self.Opt2.get().split('.')[0])-1]
        png_arr.pop(self.num_index)
        create_package(self.new_enter_word, new_style)
        send_request()
        if os.path.getsize(png_arr[self.num_index])> 200:
            self.labl2.configure(text = 'success')

    def leave(self):
        self.master.quit() ## Cannot use 'Destroy()' because it will suspend all the program

class Window_linking:
    def __init__(self, master):
        self.master = master
        master.title("連線到網站")
        self.labl = tk.Label(master, text = url, height=10 )
        self.labl.pack()
        create_package('我', 'lt.ttf')
        r = re.post(url, headers = header, data=datas)
        if r.status_code == '200':
            self.labl.configure(text = 'success')
        # Analyze the response from the website
        soup = BeautifulSoup(r.content, 'html.parser')
        while (url_arr == []):
            a_tags = soup.find_all("option", value = req.compile("[0-9a-z]{2,4}\.ttf"))
            for tag in a_tags:
                url_arr.append(tag.string)
                url_arr_name.append(tag.get('value'))
        self.button = tk.Button(master, text = "enter the system", command = self.close_window)
        self.button.pack()
    
    def close_window(self):
        self.master.destroy()

class Window_background:
    def __init__(self, master):
        self.master = master
        self.master.title('Background Selection')
        self.region1 = tk.Frame(master,  width=img_size , height=img_size , bg='blue')
        self.region2 = tk.Frame(master,  width=img_size , height=img_size , bg='blue')

        backwin_size = min( master.winfo_width(), master.winfo_height())
        self.region1.grid(column=0, row=0, padx=pad, pady=pad, columnspan=1, sticky=align_mode)
        self.region2.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)

        define_layout(master, cols=1, rows=1)
        define_layout([self.region1, self.region2])
        
        self.im_background = Image.open('white.png').convert("RGBA")
        self.im_background_TK = ImageTk.PhotoImage( self.im_background.resize( (img_size, img_size) ) )
        self.image_main = tk.Label(self.region1, image=self.im_background_TK)
        self.image_main['height'] = img_size
        self.image_main['width'] = img_size
        self.image_main.grid(column=0, row=0, sticky=align_mode)

        self.backList = ['白底', '山水畫', '花朵']
        self.backtitle = tk.StringVar()
        self.backtitle.set("Background")
        self.Optmenu = tk.OptionMenu(self.region2, self.backtitle, *self.backList, command=self.background_selection)
        self.Optmenu.grid(column=0, row=1, sticky=align_mode)

        self.bt_leave = tk.Button(self.region2, text='Finish', bg='green', fg='black', command=self.close_window)
        self.bt_leave.grid(column=1, row=1, sticky=align_mode)
        
        define_layout(master, cols=2, rows=2)
        define_layout(self.region1)
        define_layout(self.region2)
    
    def background_selection(self, *args):
        global BKimg
        if self.backtitle.get() == '白底':
            BKimg = 'white.png'
            im_background = Image.open('white.png').convert("RGBA")
            self.im_background_TK = ImageTk.PhotoImage( im_background.resize( (img_size, img_size) ) )
            self.image_main.configure(image = self.im_background_TK)
            self.image_main.image = self.im_background_TK
        elif self.backtitle.get() == '山水畫':
            BKimg = 'background_2.png'
            im_background = Image.open('background_2.png').convert("RGBA")
            self.im_background_TK = ImageTk.PhotoImage( im_background.resize( (img_size, img_size) ) )
            self.image_main.configure(image = self.im_background_TK)
            self.image_main.image = self.im_background_TK
        else:
            BKimg = 'background_1.png'
            im_background = Image.open('background_1.png').convert("RGBA")
            self.im_background_TK = ImageTk.PhotoImage( im_background.resize( (img_size, img_size) ) )
            self.image_main.configure(image = self.im_background_TK)
            self.image_main.image = self.im_background_TK

    def close_window(self):
        self.master.destroy()

class Window_main:
    def __init__(self, master):
        self.master = master
        self.master.title('Calligraphy Generator')
        self.div1 = tk.Frame(master,  width=img_size , height=img_size , bg='blue')
        self.div2 = tk.Frame(master,  width=div_size , height=div_size , bg='orange')
        self.div3 = tk.Frame(master,  width=div_size , height=div_size , bg='green')
        self.div4 = tk.Frame(master,  width=div_size , height=div_size , bg='green')

        win_size = min( master.winfo_width(), master.winfo_height())

        self.div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=3, sticky=align_mode)
        self.div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
        self.div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)
        self.div4.grid(column=1, row=2, padx=pad, pady=pad, sticky=align_mode)

        define_layout(master, cols=2, rows=2)
        define_layout([self.div1, self.div2, self.div3, self.div4])

        self.im_background = Image.open(BKimg).convert("RGBA")
        self.im_background_TK = ImageTk.PhotoImage( self.im_background.resize( (img_size, img_size) ) )
        self.image_main = tk.Label(self.div1, image=self.im_background_TK)
        self.image_main['height'] = img_size
        self.image_main['width'] = img_size
        self.image_main.grid(column=0, row=0, sticky=align_mode)

        # Enter the word
        self.lbl_text = tk.Entry(self.div2, bg = 'white', font = 40, fg='black')
        self.lbl_text.grid(column=0, row=0, sticky=align_mode)

        # Decide the size of the word
        self.Spin = tk.Spinbox(self.div3, from_=1, to=20)
        self.Spin.grid(column=0, row=0, sticky=align_mode)

        # Decide the calligraphy 
        self.OptionList = url_arr
        self.Opt = tk.StringVar()
        self.Opt.set("Calligraphy")
        self.Optmenu = tk.OptionMenu(self.div3, self.Opt, *self.OptionList, self)
        self.Optmenu.grid(column=0, row=1, sticky=align_mode)

        ##Check button for the arrangement in row or in collumn##
        self.chk_left_var = tk.IntVar()
        self.chk_right_var = tk.IntVar()

        self.chk_left = tk.Checkbutton(self.div4, text = "column", variable = self.chk_left_var,\
                          onvalue=1, offvalue=0, command = self.check_selection)
        self.chk_left.grid(column=0, row=0, sticky=align_mode)

        self.chk_right = tk.Checkbutton(self.div4, text = "row", variable = self.chk_right_var,\
                           onvalue=1, offvalue=0, command = self.check_selection)
        self.chk_right.grid(column=1, row=0, sticky=align_mode)

        # Decide the position of the word in the figure
        self.image_main.bind('<Double 1>', self.getpoint) # Decide the oringin of the word by double-click

        state2 = 'Double click \n in Figure\n to decide the oringin of \n your word'
        self.la = tk.Label(self.div4, text = state2, height=10 )
        self.la.grid(column=0, row=1, sticky=align_mode)

        self.bigBt = tk.Button(self.div4, text='Decide the position', bg='green', fg='black', command=self.position_selection)
        self.bigBt.grid(column=1, row=1, sticky=align_mode)

        # Button for saving and reviewing
        self.bt1 = tk.Button(self.div4, text='Review', bg='green', fg='black', command=self.mainfunction)
        self.bt2 = tk.Button(self.div4, text='Save', bg='green', fg='black', command=self.save_picture)

        self.bt1.grid(column=0, row=2, sticky=align_mode)
        self.bt2.grid(column=1, row=2, sticky=align_mode)

        define_layout(master, cols=3, rows=3)
        define_layout(self.div1)
        define_layout(self.div2, rows=1)
        define_layout(self.div3, rows=2, cols=1)
        define_layout(self.div4, rows=1, cols=1)
    
    # The action of hitting the review button
    def mainfunction(self):
        def picture_link(arr=[]):
            num = 0
            if(self.chk_right_var.get() is 1):
                final_im = Image.new('RGBA', (int(len(self.lbl_text.get()))*110,158)) # Crop the domain of downloaded figure
                for elem in arr:
                    im_buffer=Image.open(elem)
                    final_im.paste(im_buffer, (0+num*110, 0))
                    num += 1
                final_im.save('final.png')
                final_im.close()
            else:
                final_im = Image.new('RGBA', (110,int(len(self.lbl_text.get()))*158))
                for elem in arr:
                    im_buffer=Image.open(elem)
                    final_im.paste(im_buffer, (0, 0+num*158))
                    num += 1
                final_im.save('final.png')
                final_im.close()

        ## Split the user-entering word one-by-one and send to the website respectively 
        for index_text in range(len(self.lbl_text.get())):
            enter_word = self.lbl_text.get()[index_text]
            style = url_arr_name[int(self.Opt.get().split('.')[0])-1]
            create_package(enter_word, style)
            send_request()
            ### Identify the existance of the word in that calligraphy by the size of the image (=150 bytes)
            if os.path.getsize(png_arr[index_text])< 200:
                os.remove(png_arr[index_text])
                rt = tk.Tk()
                app1 = Window_for_newCall(rt, index_text, enter_word)
                rt.mainloop()
                rt.destroy()
            ###
        ##       
        picture_link(png_arr)
        #### Combine the linked picture with the background
        self.im_background = Image.open(BKimg).convert("RGBA")
        im = Image.open('final.png').convert("RGBA")
        (w_im, h_im) = im.size
        new_im = im.resize( ( int(w_im*float(self.Spin.get())/10), int(h_im*float(self.Spin.get())/10) ) )
        self.im_background.paste(new_im, (x_pos,y_pos), mask = new_im) # x_pos and y_pos are decided by getpoint()
        ####
        self.final_img_TK = ImageTk.PhotoImage( self.im_background.resize( (img_size, img_size) ) )
        self.image_main.configure(image = self.final_img_TK) # Reniew the image window
        self.image_main.image = self.final_img_TK
        os.remove('final.png')
        for elem in png_arr:
            os.remove(elem)
        png_arr.clear()

    # Make user not select the column and the row at the same time
    def check_selection(self):
        if (self.chk_left_var.get() == 1 and self.chk_right_var.get() == 1):
            self.chk_right_var.set(0)
            self.chk_left_var.set(0)
    
    def position_selection(self):
        global x_pos, y_pos
        x_pos = x_event
        y_pos = y_event

    def getpoint(self, event):
        global x_event, y_event
        x_event, y_event = event.x, event.y
        #self.div3.create_oval(self.eventorigin.x-2, self.eventorigin.y-2, \
        #                        self.eventorigin.x+2, self.eventorigin.y+2)
        self.la.configure(text = 'x = %d, y = %d' % (x_event, y_event) )

    def save_picture(self):
        self.im_background.save("final.png")
    
def main():
    root = tk.Tk()
    app = Window_linking(root)
    root.mainloop()
    root = tk.Tk()
    app = Window_background(root)
    root.mainloop()
    root = tk.Tk()
    app = Window_main(root)
    root.mainloop()

if __name__ == '__main__':
    align_mode = 'nswe'
    pad = 5
    div_size = 200
    img_size = div_size * 2
    header = {}
    datas = {}
    url = 'http://www.akuziti.com/mb/'
    png_arr = []
    url_arr = []
    url_arr_name = []
    BKimg = ''
    change_png = ''
    main()
