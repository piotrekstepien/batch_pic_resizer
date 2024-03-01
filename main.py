import sys, os
import PySimpleGUI as sg
import cv2


def batch_res():
    # max_val = 0
    # counter = 0
    # def update_counter (path, max_val, counter):
    #     for root, dirs, files in os.walk(path):
    #         max_val = len(files)
    #         for file in files:
    #             counter += 1
    #     return max_val, counter


    def resize_image(image, longer_edge):
        if image.shape[0] > image.shape[1]:
            r = longer_edge / image.shape[0]
            dim = (int(image.shape[1] * r), int(longer_edge))
        else:
            r = longer_edge / image.shape[1]
            dim = (int(longer_edge), int(image.shape[0] * r))
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized


    def create_new_dir(path):
        try:
            directory = "small"
            new_path = os.path.join(path, directory)
            return os.mkdir(new_path)
        except: return None


    def resize_no_overwrite(path, longer_edge):
            for root, dirs, files in os.walk(path):
                str(root)
                create_new_dir(root)
                for file in files:
                    try:
                        open_path = (root + "/" + file)
                        save_path = (root + "/" + "small" + "/" + file)
                        image = cv2.imread(open_path)
                        small_image = resize_image(image, longer_edge)
                        cv2.imwrite(save_path, small_image)
                    except: continue


    def resize_overwrite(path, longer_edge):
        for root, dirs, files in os.walk(path):
            str(root)
            for file in files:
                try:
                    file_path = (root + "/" + file)
                    image = cv2.imread(file_path)
                    small_image = resize_image(image, longer_edge)
                    cv2.imwrite(file_path, small_image)
                except : continue


    layout = [[sg.Text(key="-IN-", enable_events=True)],
              [sg.FolderBrowse(key="-BROWSE-", button_text="find pictures", enable_events=True, target="-IN-"),
               sg.Checkbox(key = "-OVERWRITE-", text = "overwrite?", enable_events=True, default= True)],
              [sg.Text("longer edge: "), sg.Combo(key="-RES-",values=("900", "1024", "2048"), default_value="900", enable_events=True)],
              [sg.Button(key = "-START-", button_text = "Start", enable_events=True)]]#, [sg.VPush(),sg.ProgressBar(100, key="-BAR-", )]]
    window = sg.Window("PicResizer", layout, resizable=True)

    while True:
        event, values = window.read()
        try:
            longer_edge = int(values["-RES-"])
        except: break
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-START-":
            path = str(values["-BROWSE-"])
            # max, count = update_counter(path, max_val, counter)
            # window["-BAR-"].update_bar(current_count = count)
            if values["-OVERWRITE-"]:
                resize_overwrite(path, longer_edge)
            else:
                resize_no_overwrite(path, longer_edge)

            sg.Popup("Done!", no_titlebar=True)

    window.close()

batch_res()