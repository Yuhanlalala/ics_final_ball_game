import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading
from tkinter import *


def main_page():
    def send_msg():
        send_text=str(user_input.get())
        entry.delete(0,END)
        text.insert(INSERT, send_text+'\n')
        result.append(send_text)
        
    root = Tk()
    root.title('Chat system')
    root.configure(width=200, height=100)

    #text
    text = Text(root,width=65,height=40,highlightthickness=1,borderwidth=2)
    text.grid(row=0,column=0,padx=(10, 30))
    
    #button
    confirm = Button(root,text='Confirm',width = 6,height = 1,command = send_msg)
    confirm.place(relx=0.8,rely=0.95)

    #input
    user_input = StringVar()
    entry = Entry(root,textvariable = user_input,width = 23)
    entry.place(relx=0.1,rely=0.95,relwidth=0.7,relheight=0.05)
    result = []

    client = Client(text, result,args=None)
    t = threading.Thread(target=client.run_chat)
    t.start()
    root.mainloop()

    
class Client:
    def __init__(self,txt, user_input,args=None):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.user_input= user_input
        self.txt = txt

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER #if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.txt.insert(INSERT, self.system_msg + '\n')
            self.txt.update()
            self.system_msg = ''

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            if len(self.user_input)!=0: 
                self.console_input.append(self.user_input.pop()) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)

main_page()
