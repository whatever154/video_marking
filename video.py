import cv2
from bs4 import BeautifulSoup
import os
import colordict
import random


def get_positions(xml):
    with open(xml, "r") as f:
        file_data = f.read()
    frames = dict()
    Bs_data = BeautifulSoup(file_data, "xml")
    Bs_data = Bs_data.find_all("object")
    colors = list(colordict.ColorDict(mode="rgb").values())
    for k in Bs_data:
        obj_coolor = colors.pop(random.randint(0, len(colors) - 1))[-2::-1]
        for i in k.find_all("data:bbox"):
            framespan = i.get("framespan").split(":")
            for j in range(int(framespan[0]), int(framespan[1]) + 1):
                if j not in frames:
                    frames[j] = []
                frames[j].append({"color": obj_coolor,"height": int(i.get("height")), "width": int(i.get("width")), "x": int(i.get("x")), "y": int(i.get("y"))})
    return frames

def video_edit(vid, change_frames, new_vid):
    cap = cv2.VideoCapture(vid)
    edited_cap = cv2.VideoWriter(new_vid, cv2.VideoWriter_fourcc(*'DIVX'), cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            if count in change_frames:
                overlay = frame.copy()
                for i in change_frames[count]:
                    cv2.rectangle(overlay, (i["x"], i["y"]), (i["x"] + i["width"], i["y"] + i["height"]),  tuple(int(x) for x in i["color"]), -1)
                alpha = 0.4
                new_frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
                for i in change_frames[count]:
                    cv2.rectangle(new_frame, (i["x"], i["y"]), (i["x"] + i["width"], i["y"] + i["height"]), (200, 0, 0), 1)
                edited_cap.write(new_frame)
            else:
                edited_cap.write(frame)
            count += 1
        else:
            break
    cap.release()
    edited_cap.release()
    cv2.destroyAllWindows()
