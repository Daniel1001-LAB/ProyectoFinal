from tkinter import *
import tkinter as tk
import pymysql
con = pymysql.connect(
        host="localhost", port=3306, user="root",
        passwd="", db="dbdatos"
    )
ventana = tk.Tk()
ventana.title ("Listado de placas")
ventana.geometry ("1800x850+0+0")
class Table: 
      
    def _init_(self,root): 
          
        
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = tk.Entry(root, width=20, fg='black', 
                               font=('Arial',16))
                  
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
  
lst = [] 
cursor=con.cursor()
cursor.execute(
			"SELECT * FROM personas"
			)	
datos=cursor.fetchall()
for data in datos:
            lst.append(data)
total_rows = len(lst) 
total_columns = len(lst[0]) 
   

t = Table(ventana) 
ventana.mainloop()