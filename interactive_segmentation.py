'''
Segement portions of an image of your choice
'''

import cv2
import argparse
import numpy as np
import os
import shutil 
#import easygui
import pathlib
#import tkinter
import matplotlib

matplotlib.use("TkAgg")

from matplotlib import pyplot as plt

drawing = False #--- true if mouse is pressed
ix, iy = -1,-1

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="dataset rsna or chester")
ap.add_argument("-f", "--folder", required=True,
	help="lung_opacity or normal or not_normal")
args = vars(ap.parse_args())

# def alert_popup(title, message):
#     """Generate a pop-up window for special messages."""
#     root = tkinter.Tk()
#     root.title(title)
#     w = 400     # popup window width
#     h = 200     # popup window height
#     sw = root.winfo_screenwidth()
#     sh = root.winfo_screenheight()
#     x = (sw - w)/2
#     y = (sh - h)/2
#     root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#     m = message
#     m += '\n'
#     m += path
#     w = Label(root, text=m, width=120, height=10)
#     w.pack()
#     b = Button(root, text="Please Check, OK!", command=root.destroy, width=10)
#     b.pack()
#     mainloop()

#--- mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, l, masked_image
    if event == cv2.EVENT_LBUTTONDOWN:
        l = []
        drawing = True
        ix, iy = x, y
        l.append([x, y])

    elif event == cv2.EVENT_MOUSEMOVE: 
        if drawing == True:
                l.append([x, y])
                cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
                #print([x, y])
                
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
        cv2.fillPoly(black, [np.asarray(l)], (255, 255, 255))
        b_th = cv2.threshold(black[:,:,1], 100, 255, cv2.THRESH_BINARY)[1]
        masked_image = cv2.bitwise_and(img2, img2, mask = b_th)
        

move_to = "./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/images/"  
all_images_path = "./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/temp_images/"    
all_images = os.listdir(all_images_path)
for i in range(len(all_images)):  
    tracker=0
    track_temp=[]
    track_images=[]
    def re():
        drawing = False #--- true if mouse is pressed
        ix, iy = -1,-1
    re()
    f=1
    path=all_images_path+all_images[i]
    masks_path="./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/masks/"+all_images[i]
    masked_image_path = "./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/masked_img/"+all_images[i]
    print("Reading next image ... ",path)
    img = cv2.imread(path)
    print("The shape of img",img.shape)
    if img is None:
        print("----not read img!",path)
        continue
    
    masked_image = img.copy()
    black = np.zeros(img.shape, img.dtype)

    img2 = img.copy()
    img3 = img.copy()
    black3 = black.copy()
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', draw_circle)
    
    while(f):
        cv2.imshow('image', img)
        cv2.imshow('black', black)
        cv2.imshow('masked_image', masked_image)

        k = cv2.waitKey(1) & 0xFF
        if k == 32:          #--- Press spacebar to clear screen ---
            img = img3.copy()
            black = black3.copy()
            masked_image = img3.copy()
        elif k == 115:      #--- Press lower case s to save 
            cv2.imwrite(masked_image_path, masked_image)
            cv2.imwrite(masks_path, black)
            destz = shutil.move(path, move_to)
            
            print("The shape of lung img",img.shape)
            print("The shape of masked img",masked_image.shape)
            print("The shape of mask generated img",black.shape)
            t1= pathlib.Path(masks_path)
            if t1.exists():
                print("Mask saved")
                tracker=tracker+1
            else:
                print("Mask not saved")
            t1= pathlib.Path(masked_image_path)
            if t1.exists():
                print("Masked Image saved")
                tracker=tracker+1
            else:
                print("Masked Image NOT saved")
            track_temp=os.listdir("./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/temp_images/")
            track_images=os.listdir("./niramai_data/"+args["dataset"]+"/"+args["folder"]+"/images/")
            track_temp=set(track_temp)
            track_images=set(track_images)
            #print(track_images)
            #print(track_temp)
            if len(track_images.intersection(track_temp)) ==0 :
                print("Moved image from temp_images to images")
                tracker=tracker+1
            else:
                print("Image not moved from temp")
            
            if tracker ==3:
                print("Success")
                tracker=0
            else:
                print("ERROR!")
                #alert_popup("Error", "SOME ERROR OCCURED")
                exit()
            
            # if tracker ==3:
            #     easygui.msgbox('Successfully Completed Segmentation', 'Success')
            #     tracker =0
            # else:
            #     easygui.msgbox('SOME ERROR OCCURED', 'ERROR')

            f=0
            #break
        elif k == 27:       #--- Press 'Esc' to exit without saving ---    
            break


cv2.destroyAllWindows()


# Examples
#alert_popup("Success", "Successfully Completed Segmentation", tracker)
