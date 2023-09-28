from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas

#functionality part


def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=bachelorTable.get_children()
    newlist=[]
    for index in indexing:
        content=bachelorTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')





def toplevel_data(title,button_text,command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False,False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    bachelor_button  = ttk.Button(screen,text=button_text,command=command)
    bachelor_button.grid(row=7, columnspan=2, pady=15)

    if title== 'Update Student':
     indexing = bachelorTable.focus()
    content = bachelorTable.item(indexing)
    lidata = content['values']
    idEntry.insert(0, lidata[0])
    nameEntry.insert(0, lidata[1])
    phoneEntry.insert(0, lidata[2])
    emailEntry.insert(0, lidata[3])
    addressEntry.insert(0, lidata[4])
    genderEntry.insert(0, lidata[5])
    dobEntry.insert(0, lidata[6])



def update_data():
    query='update bachelor set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_student()



def delete_student():
    indexing=bachelorTable.focus()
    print(indexing)
    content=bachelorTable.item(indexing)
    content_id=content['values'][0]
    query='delete  from bachelor where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted successfully')
    query='select * from bachelor'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    bachelorTable.delete(*bachelorTable.get_children())
    for data in fetched_data:
        bachelorTable.insert('',END,values=data)

def show_student():
    query = 'select * from bachelor'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    bachelorTable.delete(*bachelorTable.get_children())
    for data in fetched_data:
         bachelorTable.insert('',END,values=data)

def search_data():
    query='select * from bachelor where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
    bachelorTable.delete(*bachelorTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
         bachelorTable.insert('',END,values=data)



def add_data():
         if  idEntry.get()=='' or nameEntry.get()=='' or  phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()==''or genderEntry.get()==''or dobEntry.get()=='':
             messagebox.showerror('Error','All Fields are required',parent=screen)



         else:
              try:
                query='insert into bachelor values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),
                                 genderEntry.get(),dobEntry.get(),date,currenttime))

                con.commit()
                result = messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)

                else:
                    pass

              except:
                messagebox.showerror('Error', 'Id can not be repeated', parent=screen)
                return

              query='select * from bachelor'
              mycursor.execute(query)
              fetched_data=mycursor.fetchall()
              bachelorTable.delete(*bachelorTable.get_children())

              for data in fetched_data:
                 bachelorTable.insert('',END,values=data)




def connect_database():
    def connect():
         global mycursor,con
         try:
             con=pymysql.connect(host='localhost',user='root',password='Abcd1234@')
             mycursor=con.cursor()

         except:
             messagebox.showerror('Error','Invalid Details',parent=connectWindow)
             return
         try:
             query='create database studentmanagementsystem'
             mycursor.execute(query)
             query = 'use studentmanagementsystem'
             mycursor.execute(query)
             query = 'create table Bachelor(id int not null primary key, name varchar(30),mobile varchar(10),email varchar(30),address varchar(100),gender varchar(20),dob varchar(20),date varchar(50), time varchar(50) )'
             mycursor.execute(query)
         except:
             query = 'use studentmanagementsystem'
             mycursor.execute(query)
         messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
         connectWindow.destroy()
         addbachelorButton.config(state=NORMAL)
         searchbachelorButton.config(state=NORMAL)
         updatebachelorButton.config(state=NORMAL)
         showbachelorButton.config(state=NORMAL)
         ExportbachelorButton.config(state=NORMAL)
         deletebachelorButton.config(state=NORMAL)



    connectWindow=Toplevel( )
    connectWindow.grab_set()

    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+= 1
    sliderLabel.after(300,slider)

def clock():
    global date,currenttime
    date=time.strftime('%d:%m:%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'     Date: {date}\nTime:{currenttime}')
    datetimeLabel.after(1000,clock)




#GUI part

root=ttkthemes.ThemedTk()
root.get_themes()

root.set_theme('radiance')



root.geometry('1358x695+0+0')

root.title('student management System')

root.resizable(0,0)

datetimeLabel=Label(root,text='hello',font=('times new roman',20,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='Student management system'  #s[count]=S when count is 0
sliderLabel=Label(root,text=s,font=('arial',28,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database )
connectButton.place(x=1000,y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addbachelorButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda :toplevel_data('Add Student','Add',add_data))
addbachelorButton.grid(row=1,column=0,pady=10)

searchbachelorButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda :toplevel_data('Search Student','Search',search_data))
searchbachelorButton.grid(row=2,column=0,pady=10)

deletebachelorButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletebachelorButton.grid(row=3,column=0,pady=10)

updatebachelorButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda :toplevel_data('Update Student','Update',update_data))
updatebachelorButton.grid(row=4,column=0,pady=10)

showbachelorButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showbachelorButton.grid(row=5,column=0,pady=10)

ExportbachelorButton=ttk.Button(leftFrame,text=' Export data',width=25,state=DISABLED,command=export_data)
ExportbachelorButton.grid(row=6,column=0,pady=10)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=10)

rightFrame=Frame(root )
rightFrame.place(x=350,y=80,width=820,height=600)



scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient= VERTICAL)

bachelorTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile No','Email','Address','Gender',
                                 'D.O.B','Added Date','Added Time'),
                         xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command= bachelorTable.xview)
scrollBarY.config(command= bachelorTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

bachelorTable.pack(fill=BOTH,expand=1)

bachelorTable.heading('Id',text='Id')
bachelorTable.heading('Name',text='Name')
bachelorTable.heading('Mobile No',text='Mobile No')
bachelorTable.heading('Email',text='Email')
bachelorTable.heading('Address',text='Address')
bachelorTable.heading('Gender',text='Gender')
bachelorTable.heading('D.O.B',text='D.O.B')
bachelorTable.heading('Added Date',text='Added Date')
bachelorTable.heading('Added Time',text='Added Time')



bachelorTable.column('Id',width=50,anchor=CENTER)
bachelorTable.column('Name',width=200,anchor=CENTER)
bachelorTable.column('Mobile No',width=200,anchor=CENTER)
bachelorTable.column('Email',width=200,anchor=CENTER)
bachelorTable.column('Address',width=300,anchor=CENTER)
bachelorTable.column('Gender',width=100,anchor=CENTER)
bachelorTable.column('D.O.B',width=100,anchor=CENTER)
bachelorTable.column('Added Date',width=200,anchor=CENTER)
bachelorTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',15,'bold'),foreground='blue',background='skyblue')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='brown')







bachelorTable.config(show='headings')
root.mainloop()