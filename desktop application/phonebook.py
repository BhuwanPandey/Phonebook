from tkinter import * 
from tkinter import ttk
import mysql.connector
from  tkinter import filedialog 
from tkinter import messagebox
from PIL import Image
import os 

print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.abspath(__file__))

class MainClass:
    def __init__(self,root):
        # images path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

        
        self.root=root
        self.root.title('PhoneBook-REcorder')
        self.root.geometry('600x550+100+100')
        self.root.configure(bg='white')
        # self.root.resize(0)
        # variables 
        self.name_var=StringVar()
        self.contact_var=StringVar()


        imageFrame=Frame(self.root,width=150,height=150,bd=2,bg='black')
        imageFrame.place(x=20,y=20)

        dataFrame=Frame(self.root,bd=3,bg='white',height=150,relief=RIDGE)
        dataFrame.place(x=200,y=20)

        titleLabel=Label(self.root,bd=0,text='Create New Record',font=('times new roman',15,'bold'),bg='white')
        titleLabel.place(x=210,y=10)

        lblName=Label(dataFrame,text='Name:',font=('times new roman',15,'bold'),bg='white')
        lblName.grid(row=0,column=0,pady=(30,10),padx=(0,20),sticky='w')
        EntryName=Entry(dataFrame,font=('times new roman',15,'bold'),bd=2,textvariable=self.name_var)
        EntryName.grid(row=0,column=1,pady=(30,10),padx=(0,50),columnspan=2)
        EntryName.focus()

        lblContact=Label(dataFrame,text='Contact:',font=('times new roman',15,'bold'),bg='white')
        lblContact.grid(row=1,column=0,pady=10,padx=(0,20),sticky='w')
        EntryContact=Entry(dataFrame,font=('times new roman',15,'bold'),bd=2,textvariable=self.contact_var)
        EntryContact.grid(row=1,column=1,pady=10,padx=(0,50),columnspan=2)

        lblImage=Label(dataFrame,text='Image:',font=('times new roman',15,'bold'),bg='white')
        lblImage.grid(row=2,column=0,pady=10,sticky='w')
        btnImage=Button(dataFrame,text='Choose File',bd=2,command=self.openfile)
        btnImage.grid(row=2,column=1,ipadx=10)
        self.lblimage=Label(dataFrame,text='No Choosen File',bg='grey',bd=2)
        self.lblimage.grid(row=2,column=2,sticky='w',ipadx=8)

        btnSubmit=Button(dataFrame,text='Add Record',bg='grey',font=('times new roman',15),command=self.add_Record)
        btnSubmit.grid(row=3,column=2,ipadx=20)
        self.create_tree_view()
        self.delete_modify_widgets()
        self.fetch_data()
        self.prev_file=''
        self.call=False

    def create_tree_view(self):
        self.treeframe=Frame(self.root,relief=GROOVE,bd=3)
        self.treeframe.place(x=1,y=290,width=600,height=210)
        scroll_x=Scrollbar(self.treeframe,orient=HORIZONTAL)
        scroll_y=Scrollbar(self.treeframe,orient=VERTICAL)
        self.tree=ttk.Treeview(self.treeframe,columns=('Name','PhoneNumber','imagestatus'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)
        self.tree.heading('Name',text="Name")
        self.tree.heading('PhoneNumber',text='Phone Number')
        self.tree.heading('imagestatus',text='Image Status')
        self.tree['show']='headings'
        self.tree.column('Name',width=200)
        self.tree.column('PhoneNumber',width=200)
        self.tree.column('imagestatus',width=200)
        self.tree.pack(fill=BOTH,expand=1)
        self.tree.bind("<ButtonRelease-1>",self.get_cursor)
        # self.tree.heading('#0',text='Name',anchor='w')
        # self.tree.heading(2,text='Phone Number',anchor='w') 
    
    def delete_modify_widgets(self):
        btndelete=Button(self.root,text='Delete Selected',bg='crimson',font=('timew new roman',15),command=self.delete_data)
        btndelete.place(x=1,y=500,)
        btnmodify=Button(self.root,text='Modify Selected',bg='blue',font=('timew new roman',15),command=self.modify_data)
        btnmodify.place(x=160,y=500,)

#  Show All Records
    def fetch_data(self):
        con=mysql.connector.connect(host="localhost",user="root",password="",database="Phone_book")
        cur=con.cursor()
        sql="select * from blog_phonebook"
        cur.execute(sql)
        self.myresult=cur.fetchall()
        names=[]
        contact=[]
        imagestatus=[]
        for id,name,cont,imagelink in self.myresult:
            names.append(name)
            contact.append(cont)
            if len(imagelink) >0:
                imagestatus.append('True')
            else:
                imagestatus.append('False')
        result=zip(names,contact,imagestatus)
       
        #  show  data in Tree 
        self.tree.delete(*self.tree.get_children())
        for row in result:
                self.tree.insert('',END,values=row)      
        con.commit()
        con.close()

#  For open file
    def openfile(self):
        self.call=True
        self.prev_file=filedialog.askopenfilename(defaultextension='.png',filetypes=[('All files','*.*'),('Images','.jpeg')])
        if self.prev_file=='':
            self.prev_file=''
            self.lblimage.config(text=f"No choosen File")
        else:
            self.link=self.prev_file.split('/')
            self.lblimage.config(text=f"{self.link[-1]}")
            self.paths= 'images/'+self.link[-1]
            # link=self.file.split('/')
            # path=self.file
            # imag1=Image.open(path)    
            # imag1.save(r'C:\Users\hp\Desktop\phonebook\media\images\{}'.format(link[-1]))

#  Add  all Records
    def add_Record(self):
        var1=self.name_var.get()
        var2=self.contact_var.get()

        if var1=="" or var2=="":
            messagebox.showerror('ERROR',"Name and Contact cannot be Empty...!")
        else:
            con=mysql.connector.connect(host="localhost",user="root",password="",database="Phone_book")
            cur=con.cursor()
            sql="select * from blog_phonebook where contact='{}'".format(var2)
            cur.execute(sql)
            row=cur.fetchall()
            if len(row)==0:
                if self.prev_file=="":
                    self.emptyImage=""
                    sql="insert into blog_phonebook(name,contact,images) values(%s,%s,%s)" 
                    val=(self.name_var.get(),self.contact_var.get(),self.emptyImage)
                else:
                    imag1=Image.open(self.prev_file)
                    image_path=os.path.join(self.MEDIA_ROOT,f"{self.paths}")
                    imag1.save(image_path)
                    # imag1.save(r'C:\Users\hp\Desktop\phonebook\media\images\{}'.format(self.link[-1]))
                    sql="insert into blog_phonebook(name,contact,images) values(%s,%s,%s)" 
                    val=(self.name_var.get(),self.contact_var.get(),self.paths)
                cur.execute(sql,val)
                con.commit()
            else:
                messagebox.showwarning("warning","Contact number already exits ")
            self.fetch_data()
            self.clear()
            con.close()

    # selected data fetch
    def get_cursor(self,ev):
        self.status=''
        cursor_row=self.tree.focus()
        content=self.tree.item(cursor_row)
        # print(content)
        row=content['values']
        try:
            self.name_var.set(row[0])
            self.contact_var.set(row[1])
            con=mysql.connector.connect(host="localhost",user="root",password="",database="Phone_book")
            cur=con.cursor()
            sql="select * from blog_phonebook where contact='{}'".format(row[1])
            cur.execute(sql)
            selected_data=cur.fetchone()
            print(selected_data)
            self.Selected_id=selected_data[0]
            imagelink=selected_data[-1]
            link=imagelink.split('/')
            self.paths='images/'+link[-1]
            print(link)
            print(self.paths)
            print(self.MEDIA_ROOT)
            self.pre_file=os.path.join(self.MEDIA_ROOT,f"{self.paths}")
            # self.pre_file=r'C:\Users\hp\Desktop\phonebook\media\images\{}'.format(self.paths)
            print(self.pre_file)
            # print(self.id)
            if row[2]=='True':
                self.prev_file=self.pre_file
                self.status="True"
                self.lblimage.config(text=f"{self.paths}")
            else:
                self.prev_file=''
                self.status='False'
                self.lblimage.config(text="No Choosen File")
        except:
            messagebox.showerror('Error','please don\'t click on empty part ')

#  Delete 
    def delete_data(self):
        if self.name_var.get()=="" or self.contact_var.get()=="":
            messagebox.showerror("error",'Please provide name and contact')
        else:
            con=mysql.connector.connect(host="localhost",user="root",password="",database="Phone_book")
            cur=con.cursor()
            
            if self.status=='True':
                os.remove(self.pre_file)
            if self.status=='False':
                pass
            sql="delete from blog_phonebook where contact=%s"
            val=(self.contact_var.get(),)
            cur.execute(sql,val)
            con.commit()
            con.close()
            self.fetch_data()
            self.clear()
#  Update 
    def modify_data(self):
        if self.name_var.get()=="" or self.contact_var.get()=="":
            messagebox.showerror("error",'Please provide name and contact')
        else:
            con=mysql.connector.connect(host="localhost",user="root",password="",database="Phone_book")
            cur=con.cursor()
            if self.prev_file=="":
                self.emptyImage=""
                sql="update blog_phonebook set name=%s,contact=%s,images=%s where id=%s"
                val=(self.name_var.get(),self.contact_var.get(),self.emptyImage,self.Selected_id)
                if self.status=='True':
                    os.remove(self.pre_file)
            else:
                sql="update blog_phonebook set name=%s,contact=%s,images=%s where id=%s"
                val=(self.name_var.get(),self.contact_var.get(),self.paths,self.Selected_id)
                if self.status=='True':
                    if self.call==True:
                        os.remove(self.pre_file)
                        imag1=Image.open(self.prev_file)
                        self.pre_file=os.path.join(self.MEDIA_ROOT,f"{self.paths}")
                        # self.pre_file=r'C:\Users\hp\Desktop\phonebook\media\images\{}'.format(self.paths)
                        imag1.save(self.pre_file)

                self.pre_file=os.path.join(self.MEDIA_ROOT,f"{self.paths}")
                # self.pre_file=r'C:\Users\hp\Desktop\phonebook\media\images\{}'.format(self.paths)
                if self.status=='False':
                    imag1=Image.open(self.prev_file)
                    imag1.save(self.pre_file)

                
                    
            cur.execute(sql,val)
            con.commit()
            self.fetch_data()
            self.clear()
            con.close()
            
#  Clear all data
    def clear(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.prev_file=""
        self.lblimage.config(text="No Choosen File")
        self.call=False

root=Tk()
obj=MainClass(root)
root.mainloop()        
        