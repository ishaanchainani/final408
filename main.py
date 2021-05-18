from tkinter import Tk, Button,Label,Scrollbar,Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as pyo

con = pyo.connect(	user='root', password="password*1", host= "localhost", database = "hsplayerdb")
#print(con)

cursor = con.cursor()


class playersdb:
    def __init__(self):
        self.con = pyo.connect(	user='root', password="password*1", host= "localhost", database = "hsplayerdb")
        self.cursor = con.cursor()
        print("You have connected to the  database")
        print(con)

    def __del__(self):
        self.con.close()

    def report1(self):
        self.cursor.execute("SELECT * FROM player")
        rows = self.cursor.fetchall()
        return rows

    def report2(self):
        self.cursor.execute("SELECT * FROM player WHERE player_points > 10")
        rows = self.cursor.fetchall()
        return rows

    def report3(self):
        self.cursor.execute("SELECT * FROM player WHERE player_team = 'varsity' ")
        rows = self.cursor.fetchall()
        return rows


    def report4(self):
        self.cursor.execute("SELECT AVG(player_points) FROM player WHERE player_team = 'varsity' ")
        rows = self.cursor.fetchall()
        return rows


    def report5(self):
        self.cursor.execute("SELECT player_name FROM player WHERE player_points = (SELECT MAX(player_points) FROM player)")
        rows = self.cursor.fetchall()
        return rows


    def insert(self, player_name, player_team, player_points):
        sql=("INSERT INTO player (player_name,player_team,player_points) VALUES (%s,%s,%s)")
        values =[player_name, player_team, player_points]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Player Database",message="New player added to database")

    def update(self, player_id, player_name, player_team, player_points):
        tsql = 'UPDATE player SET  player_name = %s, player_team = %s, player_points = %s WHERE player_id=%s'
        self.cursor.execute(tsql, [player_name,player_team,player_points, player_id])
        self.con.commit()
        messagebox.showinfo(title="Player Database", message="Player Updated")

    def delete(self, player_id):
        delquery ='DELETE FROM player WHERE player_id = %s'
        self.cursor.execute(delquery, [player_id])
        self.con.commit()
        messagebox.showinfo(title="Player Database", message="Player Deleted")

db = playersdb()

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    player_name_entry.delete(0, 'end')
    player_name_entry.insert('end', selected_tuple[1])
    player_team_entry.delete(0, 'end')
    player_team_entry.insert('end', selected_tuple[2])
    player_points_entry.delete(0, 'end')
    player_points_entry.insert('end', selected_tuple[3])

def report1_records():
    list_bx.delete(0, 'end')
    for row in db.report1():
        list_bx.insert('end', row)

def report2_records():
    list_bx.delete(0, 'end')
    for row in db.report2():
        list_bx.insert('end', row)

def report3_records():
    list_bx.delete(0, 'end')
    for row in db.report3():
        list_bx.insert('end', row)

def report4_records():
    list_bx.delete(0, 'end')
    for row in db.report4():
        list_bx.insert('end', row)

def report5_records():
    list_bx.delete(0, 'end')
    for row in db.report5():
        list_bx.insert('end', row)





def add_player():
    db.insert(player_name_text.get(),player_team_text.get(),player_points_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (player_name_text.get(),player_team_text.get(),player_points_text.get()))
    player_name_entry.delete(0, "end") # Clears input after inserting
    player_team_entry.delete(0, "end")
    player_points_entry.delete(0, "end")
    con.commit()

def delete_records():
    db.delete(selected_tuple[0])
    con.commit()

def clear_screen():
    list_bx.delete(0,'end')
    player_name_entry.delete(0,'end')
    player_team_entry.delete(0,'end')
    player_points_entry.delete(0,'end')

def update_records():
    db.update(selected_tuple[0], player_name_text.get(), player_team_text.get(), player_points_text.get())
    player_name_entry.delete(0, "end") # Clears input after inserting
    player_team_entry.delete(0, "end")
    player_points_entry.delete(0, "end")
    con.commit()

def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd


root = Tk()  # Creates application window

root.title("My Players Database Application") # Adds a title to application window
root.configure(background="light pink")  # Add background color to application window
root.geometry("1500x700")  # Sets a size for application window
root.resizable(width=False,height=False) # Prevents the application window from resizing

# Create Labels and entry widgets

player_name_label =ttk.Label(root,text="Player Name",background="light pink",font=("TkDefaultFont", 16))
player_name_label.grid(row=0, column=0, sticky=W)
player_name_text = StringVar()
player_name_entry = ttk.Entry(root,width=24,textvariable=player_name_text)
player_name_entry.grid(row=0, column=1, sticky=W)

player_team_label =ttk.Label(root,text="Team Name",background="light green",font=("TkDefaultFont", 16))
player_team_label.grid(row=0, column=2, sticky=W)
player_team_text = StringVar()
player_team_entry = ttk.Entry(root,width=24,textvariable=player_team_text)
player_team_entry.grid(row=0, column=3, sticky=W)

player_points_label =ttk.Label(root,text="Points",background="light green",font=("TkDefaultFont", 16))
player_points_label.grid(row=0, column=4, sticky=W)
player_points_text = StringVar()
player_points_entry = ttk.Entry(root,width=24,textvariable=player_points_text)
player_points_entry.grid(row=0, column=5, sticky=W)

# Add a button to insert inputs into database

add_btn = Button(root, text="Add Player", bg='black', fg='black', font="helvetica 16 bold", command=add_player)
add_btn.grid(row=0, column=6, sticky=W)

# Add  a listbox  to display data from database
list_bx = Listbox(root,height=16,width=40,font="helvetica 13",bg="light blue")
list_bx.grid(row=3,column=1, columnspan=14,sticky=W + E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)

# Add scrollbar to enable scrolling
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8, rowspan=14,sticky=W )

list_bx.configure(yscrollcommand=scroll_bar.set) # Enables vertical scrolling
scroll_bar.configure(command=list_bx.yview)

# Add more Button Widgets

modify_btn = Button(root, text="Modify Record",bg="purple",fg="black",font="helvetica 10 bold",command=update_records)
modify_btn.grid(row=15, column=4)

delete_btn = Button(root, text="Delete Record",bg="red", fg="black",font="helvetica 10 bold",command=delete_records)
delete_btn.grid(row=15, column=5)

## Reports
reports_label =ttk.Label(root,text="Reports",background="light green",font=("TkDefaultFont", 16))
reports_label.grid(row=12, column=1, sticky=W)

report1_btn = Button(root, text="All Players",bg="black",fg="black",font="helvetica 10 bold",command=report1_records)
report1_btn.grid(row=13, column=1)#, sticky=tk.N)

report2_btn = Button(root, text="Top Players",bg="black",fg="black",font="helvetica 10 bold",command=report2_records)
report2_btn.grid(row=14, column=1)#, sticky=tk.N)

report3_btn = Button(root, text="Varsity Players", bg="black",fg="black",font="helvetica 10 bold",command=report3_records)
report3_btn.grid(row=15, column=1)#, sticky=tk.N)

report4_btn = Button(root, text="Varsity Average", bg="black",fg="black",font="helvetica 10 bold",command=report4_records)
report4_btn.grid(row=16, column=1)#, sticky=tk.N)

report5_btn = Button(root, text="Leading Scorer", bg="black",fg="black",font="helvetica 10 bold",command=report5_records)
report5_btn.grid(row=16, column=1)#, sticky=tk.N)






#########
clear_btn = Button(root, text="Clear Screen",bg="maroon",fg="black",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=15, column=2)#, sticky=tk.W)

exit_btn = Button(root, text="Exit  Application",bg="blue",fg="black",font="helvetica 10 bold",command=root.destroy)
exit_btn.grid(row=15, column=3)






root.mainloop()  # Runs the application until exit
