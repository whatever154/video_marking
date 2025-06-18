import video as vidt
from tkinter import *
from tkinter import filedialog

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
    result.set("Загрузка")
    root.after(50)
    frames = vidt.get_positions(xml_path)
    vidt.video_edit(vid=vid_path, change_frames=frames, new_vid=new_vid_path)
    result.set("Редактирование прошло успешно")
    btn_play_video.config(state="active")
    player.get_video(new_vid_path)
    """cap = vidt.cv2.VideoCapture(new_vid_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            vidt.cv2.imshow('Frame', frame)
            if vidt.cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap.release()
    vidt.cv2.destroyAllWindows()"""

def play_video():
    global new_vid_path
    cap = vidt.cv2.VideoCapture(new_vid_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            vidt.cv2.imshow('Frame', frame)
            if vidt.cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    vidt.cv2.destroyAllWindows()

class VideoPlayer(Frame):

    def __init__(self):
        super().__init__(relief=GROOVE, borderwidth=2)
        for i in range(1): self.rowconfigure(index=i,  weight=1)
        for i in range(1): self.columnconfigure(index=i,  weight=1)
        self.player = Canvas(self, background="white")
        self.player.pack(fill=BOTH, expand=True)
        self.fr_control = Frame(self)
        for i in range(1): self.fr_control.rowconfigure(index=i,  weight=1)
        for i in range(1): self.fr_control.columnconfigure(index=i,  weight=1)

        self.btn_play_in = False
        self.btn_play_is_pressed = False
        self.btn_play = Canvas(self.fr_control, height=20, width=20, borderwidth=3, relief=RAISED)
        self.btn_play.bind("<Enter>", self.__btn_play_enter)
        self.btn_play.bind("<Leave>", self.__btn_play_leave)
        self.btn_play.bind("<ButtonPress-1>", self.__btn_play_pressed)
        self.btn_play.bind("<ButtonRelease-1>", self.__btn_play_released)
        points = ((7, 4), (7, 24), (23, 14))
        self.btn_play.create_polygon(*points)
        self.btn_play.grid(row=0, column=0)
        self.move = Scale(self.fr_control, orient=HORIZONTAL, state="disabled")
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
        self.btn_play_is_pressed = True
        self.btn_play.config(relief=SUNKEN)
    
    def __btn_play_released(self, event):
        self.btn_play_is_pressed = False
        self.btn_play.config(relief=RAISED)
    
    def get_video(self, vid):
        self.cap = vidt.cv2.VideoCapture(vid)
        self.paused = False
        self.move.config(state="active", from_=0, to=self.cap.get(vidt.cv2.CAP_PROP_FRAME_COUNT))
    
    def __play(self):
        ret, frame = self.cap.read()




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
btn_play_video = Button(fr_btns, text="Проиграть видео", state="disabled", command=play_video)
btn_play_video.grid(row=0, column=3, padx=5, pady=5)

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

fr_up.pack(anchor=NW)

player = VideoPlayer()
player.pack(fill=BOTH, expand=True, padx=5, pady=5)

root.mainloop()