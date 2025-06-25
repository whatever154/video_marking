import video as vidt
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.font as tkFont

def window_closed(event):
    if player.cap != "":
        player.cap.release()

def get_video():
    global vid_name, vid_path
    vid_path = filedialog.askopenfilename(initialdir="/", filetypes=(("Видео", "*.mp4 *.avi"), ))
    vid_name.set(f"Видео: {vidt.os.path.basename(vid_path)}")

def get_xml():
    global xml_name, xml_path
    xml_path = filedialog.askopenfilename(initialdir="/", filetypes=(("", "*.xml"), ))
    xml_name.set(f"xml файл: {vidt.os.path.basename(xml_path)}")

def edit_vid():
    global vid_path, xml_path, new_vid_path, result
    if vid_path == "":
        result.set("Видео не выбрано")
        return
    if xml_path == "":
        result.set("xml файл не выбран")
        return
    new_vid_path = filedialog.asksaveasfilename(initialdir="/", filetypes=(("", "*.avi"), ))
    if new_vid_path == "":
        return
    if not new_vid_path.endswith(".avi"):
        new_vid_path += ".avi"
    frames = vidt.get_positions(xml_path)
    vidt.video_edit(vid=vid_path, change_frames=frames, new_vid=new_vid_path)
    result.set("Редактирование прошло успешно")

    cap = vidt.cv2.VideoCapture(new_vid_path)
    lbl_out_of.config(text=f"/{int(cap.get(vidt.cv2.CAP_PROP_FRAME_COUNT) - 1)}")
    cap.release()
    entry_frame.config(state="normal")
    btn_transition_to_frame.config(state="active")
    player.get_video(new_vid_path)

def transition():
    player.paused = True
    player.paused_before_move = True
    player.move.set(int(entry_frame.get()))
    player.move.event_generate("<Motion>")
    player.move.event_generate("<ButtonRelease-1>")

class VideoPlayer(Frame):

    def __init__(self):
        super().__init__(relief=GROOVE, borderwidth=2)
        for i in range(1): self.rowconfigure(index=i,  weight=1)
        for i in range(1): self.columnconfigure(index=i,  weight=1)
        self.cap = ""
        self.player = Canvas(self, bg="black")
        self.player.pack(fill=BOTH, expand=True)
        self.fr_control = Frame(self)
        for i in range(1): self.fr_control.rowconfigure(index=i,  weight=1)
        for i in range(1): self.fr_control.columnconfigure(index=i,  weight=1)

        self.fr_control_btns = Frame(self.fr_control)
        for i in range(1): self.fr_control_btns.rowconfigure(index=i, weight=1)
        for i in range(4): self.fr_control_btns.columnconfigure(index=i, weight=1)

        self.btn_left = Button(self.fr_control_btns, text="<", command=self.__left, state="disabled")
        self.btn_left.grid(row=0, column=0)

        self.btn_right = Button(self.fr_control_btns, text=">", command=self.__right, state="disabled")
        self.btn_right.grid(row=0, column=2)

        self.btn_play_in = False
        self.btn_play_is_pressed = False
        self.btn_play = Canvas(self.fr_control_btns, height=20, width=20, borderwidth=3, relief=RAISED, state="disabled")
        self.btn_play.bind("<Enter>", self.__btn_play_enter)
        self.btn_play.bind("<Leave>", self.__btn_play_leave)
        self.btn_play.bind("<ButtonPress-1>", self.__btn_play_pressed)
        self.btn_play.bind("<ButtonRelease-1>", self.__btn_play_released)
        points = ((7, 4), (7, 24), (23, 14))
        self.btn_play.create_polygon(*points)
        self.btn_play.grid(row=0, column=1, padx=1)

        self.fr_control_btns.grid(row=0, column=0)

        self.move = Scale(self.fr_control, orient=HORIZONTAL, state="disabled")
        self.move.bind("<ButtonPress-1>", self.__move_pressed)
        self.move.bind("<ButtonRelease-1>", self.__move_released)
        self.move.bind("<Motion>", self.__moved)
        self.move.grid(row=1, column=0, sticky=EW)

        self.fr_control.pack(fill=X)
    
    def __btn_play_enter(self, event):
        self.btn_play_in = True
        if self.btn_play_is_pressed:
            self.btn_play.config(relief=SUNKEN)
    
    def __btn_play_leave(self, event):
        self.btn_play_in = False
        if self.btn_play_is_pressed:
            self.btn_play.config(relief=RAISED)
    
    def __btn_play_pressed(self, event):
        if self.btn_play.cget("state") == "disabled":
            return
        self.btn_play_is_pressed = True
        self.btn_play.config(relief=SUNKEN)
    
    def __btn_play_released(self, event):
        if self.btn_play.cget("state") == "disabled":
            return
        self.btn_play_is_pressed = False
        self.btn_play.config(relief=RAISED)
        if self.btn_play_in:
            self.paused = not self.paused
            self.__play()

    def __move_pressed(self, event):
        self.paused_before_move = self.paused
        self.paused = True
    
    def __move_released(self, event):
        if not self.paused_before_move:
            self.paused = False
            self.__play()
    
    def  __moved(self, event):
        self.cap.set(vidt.cv2.CAP_PROP_POS_FRAMES, int(self.move.get()))
        ret, frame = self.cap.read()
        if ret:
            img1 = Image.fromarray(vidt.cv2.cvtColor(frame, vidt.cv2.COLOR_BGR2RGB))
            self.mod = img1.height / img1.width
            if self.player.winfo_height() < self.player.winfo_width():
                if self.player.winfo_height() / self.mod > self.player.winfo_width():
                    img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
                else:
                    img1 = img1.resize((int(self.player.winfo_height() / self.mod), self.player.winfo_height()))
            else:
                img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
            photo = ImageTk.PhotoImage(image=img1)
            self.player.image = photo
            self.player.create_image(self.player.winfo_width() / 2, self.player.winfo_height() / 2, image=photo, anchor=CENTER)

    def __left(self):
        self.paused = True
        self.paused_before_move = True
        if self.move.get() > self.move.cget("from"):
            self.move.set(self.move.get() - 1)
            self.move.event_generate("<Motion>")
            self.move.event_generate("<ButtonRelease-1>")

    def __right(self):
        self.paused = True
        self.paused_before_move = True
        if self.move.get() < self.move.cget("to"):
            self.move.set(self.move.get() + 1)
            self.move.event_generate("<Motion>")
            self.move.event_generate("<ButtonRelease-1>")
        
    def get_video(self, vid):
        if player.cap != "":
            player.cap.release()
        self.cap = vidt.cv2.VideoCapture(vid)
        self.paused = False
        self.frame_count = self.cap.get(vidt.cv2.CAP_PROP_FRAME_COUNT)-1
        self.move.config(state="active", from_=0, to=self.frame_count)
        self.btn_right.config(state="active")
        self.btn_left.config(state="active")
        self.btn_play.config(state="normal")
        ret, frame = self.cap.read()
        if ret:
            img1 = Image.fromarray(vidt.cv2.cvtColor(frame, vidt.cv2.COLOR_BGR2RGB))
            self.mod = img1.height / img1.width
            if self.player.winfo_height() < self.player.winfo_width():
                if self.player.winfo_height() / self.mod > self.player.winfo_width():
                    img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
                else:
                    img1 = img1.resize((int(self.player.winfo_height() / self.mod), self.player.winfo_height()))
            else:
                img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
            photo = ImageTk.PhotoImage(image=img1)
            self.player.image = photo
            self.player.create_image(self.player.winfo_width() / 2, self.player.winfo_height() / 2, image=photo, anchor=CENTER)
            self.framerate = int(1000 / self.cap.get(vidt.cv2.CAP_PROP_FPS )) - 15
            self.after(self.framerate, self.__play)
     
    def __play(self):
        if not self.paused and self.move.get() < self.frame_count:
            if self.cap.isOpened:
                ret, frame = self.cap.read()
                if ret :
                    img1 = Image.fromarray(vidt.cv2.cvtColor(frame, vidt.cv2.COLOR_BGR2RGB))
                    self.mod = img1.height / img1.width
                    if self.player.winfo_height() < self.player.winfo_width():
                        if self.player.winfo_height() / self.mod > self.player.winfo_width():
                            img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
                        else:
                            img1 = img1.resize((int(self.player.winfo_height() / self.mod), self.player.winfo_height()))
                    else:
                        img1 = img1.resize((int(self.player.winfo_width()), int(self.player.winfo_width()*self.mod)))
                    photo = ImageTk.PhotoImage(image=img1)
                    self.player.image = photo
                    self.player.create_image(self.player.winfo_width() / 2, self.player.winfo_height() / 2, image=photo, anchor=CENTER)
                    self.move.set(self.move.get() + 1)
                    self.after(self.framerate, self.__play)

root = Tk()
root.geometry("1000x800")

fr_up = Frame()
for i in range(1): fr_up.rowconfigure(index=i,  weight=1)
for i in range(1): fr_up.columnconfigure(index=i,  weight=1)

fr_btns = Frame(fr_up)
for i in range(1): fr_btns.rowconfigure(index=i,  weight=1)
for i in range(2): fr_btns.columnconfigure(index=i,  weight=1)
btn_get_videp = Button(fr_btns, text="Выбрать видео", command=get_video)
btn_get_videp.grid(row=0, column=0, padx=5, pady=5)
btn_get_xml = Button(fr_btns, text="Выбрать xml файл", command=get_xml)
btn_get_xml.grid(row=0, column=1, padx=5, pady=5)
btn_edit_video = Button(fr_btns, text="Изменить видео", command=edit_vid)
btn_edit_video.grid(row=0, column=2, padx=5, pady=5)

fr_btns.grid(row=0, column=0, sticky=NW, rowspan=1)

fr_data = Frame(fr_up)
vid_path = ""
xml_path = ""
new_vid_path = ""
for i in range(3): fr_data.rowconfigure(index=i,  weight=1)
for i in range(1): fr_data.columnconfigure(index=i,  weight=1)
vid_name = StringVar()
xml_name = StringVar()
result = StringVar()
vid_name.set("Видео: ")
xml_name.set("xml файл:")
lbl_vid = Label(fr_data, textvariable=vid_name)
lbl_vid.grid(row=0, column=0, sticky=NW)
lbl_xml = Label(fr_data, textvariable=xml_name)
lbl_xml.grid(row=1, column=0, sticky=NW)
lbl_result = Label(fr_data, textvariable=result)
lbl_result.grid(row=2, column=0, sticky=NW)

fr_data.grid(row=1, column=0, sticky=NW, padx=5)

fr_frame_transition = Frame(fr_up, relief="groove", borderwidth=2)

Label(fr_frame_transition, text="Покадровывй переход", font=tkFont.Font(size=10)).grid(row=0, column=0)

fr_select_frame = Frame(fr_frame_transition)

lbl_out_of = Label(fr_select_frame, text="/0")
lbl_out_of.grid(row=1, column=1, sticky=W)

btn_transition_to_frame = Button(fr_frame_transition, text="Перейти", state="disabled", command=transition)
btn_transition_to_frame.grid(row=2, column=0, sticky=W, padx=3)

def validate_pos(inp):
    global lbl_out_of
    try:
        int(inp)
    except:
        if inp == '': 
            btn_transition_to_frame.config(state="disabled")
            return True
        return False
    if int(inp) >= 0:
        if int(inp) > int(lbl_out_of.cget("text")[1:]):
            btn_transition_to_frame.config(state="disabled")
        else:
            btn_transition_to_frame.config(state="active")
        return True
    return False

transition_to_frame = IntVar()
entry_frame = Entry(fr_select_frame, textvariable=transition_to_frame, validate='key', validatecommand=(root.register(validate_pos), "%P"), width=6, state="disabled")
entry_frame.grid(row=1, column=0, sticky=W, padx=1)

fr_select_frame.grid(row=1, column=0, sticky=W, pady=5, padx=3)

fr_frame_transition.grid(row=0, column=1, rowspan=2, sticky=NSEW)

fr_up.pack(anchor=NW, fill=X)

player = VideoPlayer()
player.pack(fill=BOTH, expand=True, padx=5, pady=5)

root.bind("<Destroy>", window_closed)
root.mainloop()
