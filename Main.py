import tkinter as tk
from tkinter import ttk
from tkinter import *
import webbrowser
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import customtkinter



def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    id = (txt.get())
    name = (txt2.get())
    if (name.isalpha()) or (' ' in name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sample_num = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sample_num = sample_num + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + id + '.' + str(sample_num) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sample_num > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + id
        row = [serial, '', id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if name.isalpha() == False:
            res = "Enter Correct name"
            message.configure(text=res)


def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()


def new_reg():
    global mast, txt, txt2, clock, message1
    mast = tk.Tk()
    mast.state("zoomed")
    mast.resizable(False, False)
    mast.title("New Registration")
    mast.configure(background="white")
    message3 = tk.Label(mast, text="New Registration using Face Recognition", fg="black", bg="#caddf8",
                        width=35, height=1, font=('Times New Roman', 29, ' italic '))
    message3.place(x=290, y=10)
    # Date and time frame
    frame3 = tk.Frame(mast, bg="#c4c6ce")
    frame3.place(relx=0.20, rely=0.12)
    frame4 = tk.Frame(mast, bg="#c4c6ce")
    frame4.place(relx=0.01, rely=0.12)
    datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |", fg="black", bg="white", width=15,
                     height=1, font=('comic', 20, ' bold '))
    datef.pack(fill='both', expand=4)
    clock = tk.Label(frame3, fg="black", bg="white", width=9, height=1, font=('comic', 20, ' bold '))
    clock.pack(fill='both', expand=1)
    tick()

    lbl = tk.Label(mast, text="Enter ID", fg="black", bg="#c79cff", font=('Times New Roman', 17, ' bold '))
    lbl.place(relx=0.2, rely=0.21, relwidth=0.17, relheight=0.07)

    txt = tk.Entry(mast, width=32, fg="black", font=('Times New Roman', 15, ' bold '))
    txt.place(relx=0.4, rely=0.21, relwidth=0.27, relheight=0.07)

    lbl2 = tk.Label(mast, text="Enter Name", fg="black", bg="#c79cff", font=('Times New Roman', 17, ' bold '))
    lbl2.place(relx=0.2, rely=0.31, relwidth=0.17, relheight=0.07)

    txt2 = tk.Entry(mast, fg="black", font=('Times New Roman', 15, ' bold '))
    txt2.place(relx=0.4, rely=0.31, relwidth=0.27, relheight=0.07)

    clearButton = tk.Button(mast, text="Clear", command=clear, fg="black", bg="#ff7221", width=11,
                            activebackground="white", font=('Times New Roman', 11, ' bold '))
    clearButton.place(relx=0.67, rely=0.21, relwidth=0.17, relheight=0.07)
    clearButton2 = tk.Button(mast, text="Clear", command=clear2, fg="black", bg="#ff7221", width=11,
                             activebackground="white", font=('Times New Roman', 11, ' bold '))
    clearButton2.place(relx=0.67, rely=0.31, relwidth=0.17, relheight=0.07)

    message1 = tk.Label(mast, text="1) Take Images\n\n2) Save Profile", bg="#c79cff", fg="black", width=20, height=5,
                        activebackground="#3ffc00", font=('comic', 15, ' bold '))
    message1.place(x=50, y=290)
    takeImg = tk.Button(mast, text="Take Image", command=TakeImages, fg="black", bg="#68ffd4", width=34, height=1,
                        activebackground="#fff1f5", font=('Times New Roman', 15, ' bold '))
    takeImg.place(x=420, y=380)
    trainImg = tk.Button(mast, text="Save Profile", command=psw, fg="black", bg="#68ffd4", width=34, height=1,
                         activebackground="#fff1f5", font=('Times New Roman', 15, ' bold '))
    trainImg.place(x=420, y=450)
    message = tk.Label(mast, text="", bg="#c79cff", fg="black", width=28, height=1, activebackground="#3ffc00",
                       font=('Times New Roman', 16, ' bold '))
    message.place(x=450, y=550)
    quitWindow = customtkinter.CTkButton(master=mast, text="QUIT", command=mast.destroy, corner_radius=20,
                                         border_width=2, border_color="#4e5157", text_color="#000000",
                                         hover_color="#ff8800"
                                         , border_spacing=20, fg_color=("#000000", "#ff7600"))
    quitWindow.place(x=950, y=610, anchor=customtkinter.CENTER)

    res = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
    else:
        res = 0
    message.configure(text='Total Registrations till now  : ' + str(res))


def psw():
    global message
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')


def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    id = (txt.get())
    name = (txt2.get())
    if (name.isalpha()) or (' ' in name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sample_num = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sample_num = sample_num + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + id + '.' + str(sample_num) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sample_num > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + id
        row = [serial, '', id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, id = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(id))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(id[0]))



def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        ids.append(id)
    return faces, ids


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                id = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                id = str(id)
                id = id[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(id), '', bb, '', str(date), '', str(timeStamp)]

            else:
                id = 'Unknown'
                bb = str(id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if i > 1:
                if i % 2 != 0:
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()


def change_psd():
    global master
    master = tk.Tk()
    master.geometry("450x180+400+250")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='Enter Old Password     ',bg='white',font=('Times New Roman', 14, ' bold '))
    lbl4.place(x=10, y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('Times New Roman', 12, ' bold '),show='*')
    old.place(x=220,y=10)
    lbl5 = tk.Label(master, text='Enter New Password     ', bg='white', font=('Times New Roman', 14, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('Times New Roman', 12, ' bold '),show='*')
    new.place(x=220, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password     ', bg='white', font=('Times New Roman', 14, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('Times New Roman', 12, ' bold '),show='*')
    nnew.place(x=220, y=80)
    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="#f6303c", height=1,width=20 , activebackground = "white" ,font=('Times New Roman', 10, ' bold '))
    cancel.place(x=250, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#30fd6c", height=1, width=20, activebackground="white", font=('Times New Roman', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()


def report_issue():
    webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSe6w2a06GnBHHMoSUH1SHQ0b-2r8FBD-R8JgIcRN3LApnKoMA/viewform")


# def license():

def about_us():
    mess._show(title='Our Team', message="1. Yash Singh\n"
                                         "2. Neeraj Kumar Prajapati\n"
                                         "3. Shashwat Singh\n"
                                         "4. Vinay Vyas\n"
                                         "5. Aman Kumar")


def license():
    mess._show(title='License', message="MIT License\n\nThe following terms and conditions must be met in order for "
                                        "anyone who obtains a copy of this software and any related documentation "
                                        "files (the \"Software\") to be allowed to deal with it without restriction."
                                        "This includes the freedom to use, copy, modify, merge, publish, distribute, "
                                        "sublicense, and/or sell copies of the software, as well as the ability to "
                                        "allow others to do the same. All copies or significant portions of the "
                                        "Software must have the aforementioned copyright notice and permission notice "
                                        "attached.\n\nThe software is given and comes with no express or "
                                        "implied warranties of any kind, including but not limited to the warranties "
                                        "of merchantability, fitness for a particular purpose, and noninfringement. "
                                        "The authors and copyright holders disclaim all liability for claims, damages, "
                                        "and other liabilities arising from, arising out of, or connected with the "
                                        "software, or from using or otherwise utilising the software, whether in a "
                                        "contract, tort, or other action.\n\n Copyright ©")


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good Morning"

    elif 12 <= hour < 18:
        return "Good Afternoon"

    else:
        return "Good Evening"


def welcome_message():
    global wel
    wel = tk.Tk()
    wel.geometry("800x400+250+150")
    wel.resizable(False, False)
    wel.title("Welcome Message")
    lbl4 = tk.Label(wel, text='Welcome to our Face Matrix Attendance System', font=('Comic sans MS', 14, ' bold '))
    lbl5 = tk.Label(wel, text='A python GUI integrated attendance system using face recognition to take attendance.',
                    font=('Times New Roman', 14, ' bold '))
    lbl6 = tk.Label(wel, text='FEATURES', font=('Times New Roman', 14, ' bold '))
    lbl7 = tk.Label(wel, text='1) Easy to use with interactive GUI support.',
                    font=('Times New Roman', 14, ' bold '))
    lbl8 = tk.Label(wel, text='2) Password protection for new person registration.',
                    font=('Times New Roman', 14, ' bold '))
    lbl9 = tk.Label(wel, text='3) Creates/Updates CSV file for details of students on registration.',
                    font=('Times New Roman', 14, ' bold '))
    lbl10 = tk.Label(wel, text='4) Creates a new CSV file everyday for attendance and',
                     font=('Times New Roman', 14, ' bold '))
    lbl11 = tk.Label(wel, text='marks attendance with proper date and time.', font=('Times New Roman', 14, ' bold '))
    lbl12 = tk.Label(wel, text='5) Displays live attendance updates for the day on the',
                     font=('Times New Roman', 14, ' bold '))
    lbl13 = tk.Label(wel, text='main screen in tabular format with Id, name, date and time.',
                     font=('Times New Roman', 14, ' bold '))
    lbl4.place(x=170, y=10)
    lbl5.place(x=20, y=70)
    lbl6.place(x=20, y=100)
    lbl7.place(x=20, y=130)
    lbl8.place(x=20, y=160)
    lbl9.place(x=20, y=190)
    lbl10.place(x=20, y=220)
    lbl11.place(x=45, y=250)
    lbl12.place(x=20, y=280)
    lbl13.place(x=45, y=310)


def file_exit():
    window.quit()


global key, wish
key = ''
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'}


window = tk.Tk()
window.state("zoomed")  # For Full Screen
window.resizable(False, False)
window.title("Face Attendance System")  # Title
window.configure(background='#fffbe2')  # background Colour
title_im = PhotoImage(file='Icon/top.2.png')
window.iconphoto(False, title_im)  # Adding title image
# Heading "Face Matrix Attendance System"
message3 = tk.Label(window, text="Face Matrix Attendance System", fg='#002f76', bg='#fffbe2',
                    width=25, height=1, font=('Times New Roman', 29, ('italic', 'bold')))
message3.place(x=374, y=15)

# frame for date and time
frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.01, rely=0.05)
frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.11, rely=0.05)
datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |", fg="black", bg="#fffbe2", width=15,
                 height=1, font=('Book Antiqua', 12, 'bold'))
datef.pack(fill='both', expand=4)
clock = tk.Label(frame3, fg="black", bg="#fffbe2", width=8, height=1, font=('Book Antiqua', 12, 'bold'))
clock.pack(fill='both', expand=1)
tick()

# label of wish me function
lbl3 = tk.Label(window, text=wish_me()+" Kindly mark the Attendance", width=42, fg="black", bg="#fffbe2", height=1
                , font=('cascadia code', 17))
lbl3.place(x=375, y=110)

# round button for Take Attendance
trackImg = customtkinter.CTkButton(master=window, text="Take Attendance", command=TrackImages, corner_radius=20,
                                   border_width=2, border_color="#4e5157", text_color="#000000", hover_color="#13b5de"
                                   , border_spacing=20, fg_color=("#000000", "#0088ab"))
trackImg.place(x=460, y=560, anchor=customtkinter.CENTER)

# tree view of attendance
tv = ttk.Treeview(window, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=85)
tv.column('name', width=150)
tv.column('date', width=160)
tv.column('time', width=160)
tv.grid(row=2, column=0, padx=(365, 0), pady=(200, 0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

# Scroll bar
scroll = ttk.Scrollbar(window, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(200, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)
# Quit command
quitWindow = customtkinter.CTkButton(master=window, text="QUIT", command=window.destroy, corner_radius=20,
                                     border_width=2,border_color="#4e5157",text_color="#000000", hover_color="#ff8800"
                                     , border_spacing=20, fg_color=("#000000", "#ff7600"))
quitWindow.place(x=800, y=560, anchor=customtkinter.CENTER)

# Defining Menu bar
menubar = tk.Menu(window, relief='ridge')
filemenu1 = tk.Menu(menubar, tearoff=0, background='#ffedbc')
filemenu2 = tk.Menu(menubar, tearoff=0, background='#e8ffed')
icon_newr = PhotoImage(file='Icon/newReg.png')
icon_change = PhotoImage(file='Icon/ChangePass.png')
icon_exit = PhotoImage(file='Icon/pass.png')
filemenu1.add_command(label="New Registration",image=icon_newr, compound='left', command=new_reg)
filemenu1.add_command(label="Change Password",image=icon_change, compound='left', command=change_psd)
filemenu1.add_command(label='Exit',image=icon_exit, compound='left', command=window.destroy)
icon_welcome = PhotoImage(file='Icon/welcome.png')
icon_license = PhotoImage(file='Icon/license.png')
icon_report = PhotoImage(file='Icon/report.png')
icon_team = PhotoImage(file='Icon/team.png')
filemenu2.add_command(label="Welcome Message",image=icon_welcome, compound='left', command=welcome_message)
filemenu2.add_command(label="View License",image=icon_license, compound='left', command=license)
filemenu2.add_command(label="Report Issue",image=icon_report, compound='left', command=report_issue)
filemenu2.add_command(label="About our Team",image=icon_team, compound='left', command=about_us)

# Add the Help menu to the menu bar
menubar.add_cascade(label='New', font=('Times New Roman', 29, ' bold '),menu=filemenu1)
menubar.add_cascade(label='Help', font=('Times New Roman', 29, ' bold '),menu=filemenu2)
light = PhotoImage(file="Icon/Darkr.png")
dark = PhotoImage(file="Icon/Lightr.png")

# Defining a function to toggle
switch_value = True


def toggle():
    global switch_value
    if switch_value == True:
        switch.config(image=dark, bg="#1e1f22", activebackground="#191920")
        # Changes the window to dark theme
        window.config(bg="#1e1f22")
        switch_value = False

    else:
        switch.config(image=light, bg="#fffbe2", activebackground="#fffce2")

        # Changes the window to light theme
        window.config(bg="#fffbe2")
        switch_value = True


# Creating a button to toggle
switch = Button(window, image=light, bd=0, bg="#fffbe2", activebackground="#fffce2", command=toggle)
switch.place(x=1180, rely=0.13)
window.config(menu=menubar)

window.mainloop()
