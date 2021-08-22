import cv2

import pytesseract
import pymysql

def CamaraEscritorio():


    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    placa = []

    image = cv2.imread('placa.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))
    canny = cv2.Canny(gray,150,200)
    canny = cv2.dilate(canny,None,iterations=1)

    cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    conn = pymysql.connect(
        host="localhost", port=3306, user="root",
        passwd="", db="dbdatos"
    )

    for c in cnts:
        area = cv2.contourArea(c)

        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        
        if len(approx)==4 and area>9000:
            print('area=',area)
          

            aspect_ratio = float(w)/h
            if aspect_ratio>2.4:
                placa = gray[y:y+h,x:x+w]
                text = pytesseract.image_to_string(placa,config='--psm 11')
                
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3)
                cursor = conn.cursor()
                cursor.execute(
                "SELECT * FROM personas where placa= %s",str(text)
                )
                personas = cursor.fetchall()
                for persona in personas:
                  
                    print(persona[1])

    # Guardar cambios.
    conn.commit()
    conn.close()
    cv2.imshow('Image',image)
    cv2.moveWindow('Image',45,10)
    cv2.waitKey(0)