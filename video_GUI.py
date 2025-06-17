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
    frames = vidt.get_positions(xml_path)
    vidt.video_edit(vid=vid_path, change_frames=frames, new_vid=new_vid_path)
    result.set("Редактирование прошло успешно")
    btn_play_video.config(state="active")
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




root = Tk()
root.geometry("450x100")
for i in range(1): root.rowconfigure(index=i,  weight=1)
for i in range(1): root.columnconfigure(index=i,  weight=1)

fr_btns = Frame()
for i in range(1): fr_btns.rowconfigure(index=i,  weight=1)
for i in range(3): fr_btns.columnconfigure(index=i,  weight=1)
btn_get_videp = Button(fr_btns, text="Выбрать видео", command=get_video)
btn_get_videp.grid(row=0, column=0, padx=5, pady=5)
btn_get_xml = Button(fr_btns, text="Выбрать xml файл", command=get_xml)
btn_get_xml.grid(row=0, column=1, padx=5, pady=5)
btn_edit_video = Button(fr_btns, text="Изменить видео", command=edit_vid)
btn_edit_video.grid(row=0, column=2, padx=5, pady=5)
btn_play_video = Button(fr_btns, text="Проиграть видео", state="disabled", command=play_video)
btn_play_video.grid(row=0, column=3, padx=5, pady=5)

fr_btns.grid(row=0, column=0, sticky=NW)

fr_data = Frame()
vid_path = ""
xml_path = ""
new_vid_path = ""
for i in range(2): fr_data.rowconfigure(index=i,  weight=1)
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

fr_data.grid(row=1, column=0, sticky=NW)

root.mainloop()