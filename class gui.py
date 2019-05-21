'''from chat_client_class import *
import client_state_machine as csm'''
from tkinter import *
'''import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp'''

class login:
    def __init__(self):
        self.name=''
        self.new=Tk()
        self.new.geometry('320x240')
        self.new.title('log-in')
        self.lb=Label(self.new, text="Welcome to the chat system!\nWhat's your name?")
        self.lb.place(relx=0.2,rely=0.15)
        self.entry_new=Entry(self.new)
        self.entry_new.place(relx=0.2,rely=0.5, relwidth=0.5,relheight=0.1)
        self.send=Button(self.new,text='confirm',command=self.new_input)
        self.send.place(relx=0.7,rely=0.7)
        
    def new_input(self):
        text=self.entry_new.get()
        self.entry_new.delete(0,END)
        username=text
        self.new.destroy()
        #client.run_chat(username)
        main_page(username)



class main_page:
    def __init__(self,name):
        self.name=name
        self.root=Tk()
        self.root.title('Chat')
        self.root.geometry('800x600')

        self.title=Label(self.root,text='Welcome '+self.name,fg="green",font=('Times',30))
        self.title.place(relx=0.4,y=0)

        self.menu=Label(self.root,text='Menu:',fg="Blue",font=('Times',25))
        self.menu.place(x=680,y=78)

        #Entry
        self.entry=Entry(self.root)
        self.entry.place(x=70,y=500, relwidth=0.8,relheight=0.05)
        self.send=Button(self.root,text='send',command=self.user_input)
        self.send.place(relx=0.8,rely=0.9,relwidth=0.1,relheight=0.05)

        #menu button
        button1=Button(self.root,text='User',command=self.user)
        button1.place(relx=0.85,rely=0.2,relwidth=0.1,relheight=0.07)
        button2=Button(self.root,text='Connect',command=self.connect)
        button2.place(relx=0.85,rely=0.3,relwidth=0.1,relheight=0.07)
        button3=Button(self.root,text='Poem',command=self.poem)
        button3.place(relx=0.85,rely=0.4,relwidth=0.1,relheight=0.07)
        button4=Button(self.root,text='History',command=self.history)
        button4.place(relx=0.85,rely=0.5,relwidth=0.1,relheight=0.07)
        button5=Button(self.root,text='Game',command=self.game)
        button5.place(relx=0.85,rely=0.6,relwidth=0.1,relheight=0.07)

        #text
        self.txt=Text(self.root)
        self.txt.place(relx=0.1, rely=0.1,relheight=0.6)

        #self.root.mainloop()

    def text_out(self,text):
        self.txt.insert(END,text+'\n')
        
    def user_input(self):
        text=self.entry.get()
        self.entry.delete(0,END)
    
    def user(self):
        self.txt.insert(END,'user\n')

    
            
    def connect(self):
        def new_input():
            text=entry_new.get()
            entry_new.delete(0,END)
            self.txt.insert(END, text+'\n')
            new.destroy()
            #csm.connect_to(text)
            
        new=Toplevel(self.root)
        new.geometry('320x240')
        new.title('connection')
        lb=Label(new, text='Who you want to connect?')
        lb.place(relx=0.2,rely=0.2)
        entry_new=Entry(new)
        entry_new.place(relx=0.2,rely=0.5, relwidth=0.5,relheight=0.1)
        send=Button(new,text='confirm',command=new_input)
        send.place(relx=0.7,rely=0.7)
    
    def poem(self):
        def new_input():
            text=entry_new.get()
            entry_new.delete(0,END)
            self.txt.insert(END, text+'\n')
            new.destroy()
            
        new=Toplevel(self.root)
        new.geometry('320x240')
        new.title('poem')
        lb=Label(new, text='Which poem do you want to read?')
        lb.place(relx=0.2,rely=0.2)
        entry_new=Entry(new)
        entry_new.place(relx=0.2,rely=0.5, relwidth=0.5,relheight=0.1)
        send=Button(new,text='confirm',command=new_input)
        send.place(relx=0.7,rely=0.7)

    def history(self):
        def new_input():
            text=entry_new.get()
            entry_new.delete(0,END)
            self.txt.insert(END, text+'\n')
            new.destroy()
        new=Toplevel(self.root)
        new.geometry('320x240')
        new.title('history')
        lb=Label(new, text='What do you want to search?')
        lb.place(relx=0.2,rely=0.2)
        entry_new=Entry(new)
        entry_new.place(relx=0.2,rely=0.5, relwidth=0.5,relheight=0.1)
        send=Button(new,text='confirm',command=new_input)
        send.place(relx=0.7,rely=0.7)

    def game(self):
        self.txt.insert(END,'haha')
        

login()
