import cv2 as cv
import numpy as np
import pyautogui
import time

class eventFinder:
    def __init__(self):
        self.message="hello from detect events"

    def check(self):
        print(self.message)
        time.sleep(5)
        print("done")



    def detect_kills(self):
        while(True):
            img = pyautogui.screenshot() 
            screenshotArr = np.array(img)

            resized_image = cv.resize(screenshotArr, (1920, 1080))
            img_rgb=cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)






            # Read the template 
            template = cv.imread('template.jpg', 0) 


            # Store width and height of template in w and h 
            w, h = template.shape[::-1] 

            # Perform match operations. 
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED) 

            # Specify a threshold 
            threshold = 0.8

            # Store the coordinates of matched area in a numpy array 
            loc = np.where(res >= threshold) 


            cnt=0
            # Draw a rectangle around the matched region. 
            for pt in zip(*loc[::-1]): 
                cnt+=1
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
                # if cnt==10:
                #     break
            # Show the final image with the matched area. 




            cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL) 
            cv.resizeWindow("Resized_Window", 1920, 1080) 
            cv.imshow("Resized_Window", img_rgb) 



            # press 'q' with the output window focused to exit.
            # press 'f' to save screenshot as a positive image, press 'd' to 
            # save as a negative image.
            # waits 1 ms every loop to process key presses 
            key = cv.waitKey(1)
            if key == ord('q'):
                cv.destroyAllWindows()
                break







    def detect_round_start(self):
        while(True):
            img = pyautogui.screenshot() 
            screenshotArr = np.array(img)

            resized_image = cv.resize(screenshotArr, (1920, 1080))
            img_rgb=cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)






            # Read the template 
            template = cv.imread('buyTemplate.jpg', 0) 


            # Store width and height of template in w and h 
            w, h = template.shape[::-1] 

            # Perform match operations. 
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED) 

            # Specify a threshold 
            threshold = 0.8

            # Store the coordinates of matched area in a numpy array 
            loc = np.where(res >= threshold) 


            cnt=0
            # Draw a rectangle around the matched region. 
            for pt in zip(*loc[::-1]): 
                cnt+=1
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
                # if cnt==10:
                #     break
            # Show the final image with the matched area. 
            if cnt>=1:
                return 1



            # cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL) 
            # cv.resizeWindow("Resized_Window", 1920, 1080) 
            # cv.imshow("Resized_Window", img_rgb) 



            # press 'q' with the output window focused to exit.
            # press 'f' to save screenshot as a positive image, press 'd' to 
            # save as a negative image.
            # waits 1 ms every loop to process key presses 
            # key = cv.waitKey(1)
            # if key == ord('q'):
            #     cv.destroyAllWindows()
            #     break
            # elif key == ord('f'):
            #     cv.imwrite('positive/{}.jpg'.format(loop_time), img_rgb)
            # elif key == ord('d'):
            #     cv.imwrite('negative/{}.jpg'.format(loop_time), img_rgb)