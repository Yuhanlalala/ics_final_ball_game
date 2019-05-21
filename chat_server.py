"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import os

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        self.dic_score = {}
        # sonnet
        # self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        # self.sonnet = pkl.load(self.sonnet_f)
        # self.sonnet_f.close()
        self.sonnet = indexer.PIndex("AllSonnets.txt")
    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        #move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        #add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        #load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name]=pkl.load(open(name+'.idx','rb'))
                            except IOError: #chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                    else: #a client under this name has already logged in
                        mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print ('wrong code received')
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
#==============================================================================
# handle connect request
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action":"connect", "status":"self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action":"connect", "status":"success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
                else:
                    msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, msg)
#==============================================================================
# handle messeage exchange: one peer for now. will need multicast later
#==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                #said = msg["from"]+msg["message"]
                said = text_proc(msg["message"], from_name)
                self.indices[from_name].add_msg_and_index(said)
                the_guys = self.group.list_me(from_name)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    mysend(to_sock, json.dumps({"action":"exchange", "from":from_name,'message':msg['message']}))
                    # mysend(to_sock, "...index the messages before sending, or search won't work")





                    # ---- end of your code --- #
#==============================================================================
#                 listing available peers
#==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                # IMPLEMENTATION
                # ---- start your code ---- #
                msg = str(self.group.list_all(from_name))
                
                #  msg = "...needs to use self.group functions to work"





                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"list", "results":msg}))
#==============================================================================
#             retrieve a sonnet
#==============================================================================
            elif msg["action"] == "poem":
                # IMPLEMENTATION
                # ---- start your code ---- #
                poem_list = self.sonnet.get_poem(int(msg['target']))
                poem = ''
                for i in poem_list:
                    poem += i+'\n'
                # poem = "...needs to use self.sonnet functions to work"
                print('here:\n', poem)





                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"poem", "results":poem}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))
#==============================================================================
#                 search
#==============================================================================
            elif msg["action"] == "search":
                # IMPLEMENTATION
                # ---- start your code ---- #
                # name = self.logged_sock2name[from_sock]
                
                # if name in self.indices.keys():
                search_rslt = ''
                for i in self.indices.keys():
                    a = self.indices[i].search(msg['target'])
                    if len(a) == 0:
                        continue
                    else:
                        for m in a:
                            search_rslt += m[1] + '\n'
                            #string = a[m]
                            #search_rslt += str(string[1])
                        # string=a[1]
                        # search_rslt+=string
                # assert search_rslt is None, search_rslt
                            # + str(string[1])
                # search_rslt = str(self.indices[name].search(msg['target']))+'\n'
                # search_rslt = "needs to use self.indices search to work"
                print('server side search: ' + search_rslt)
                # else:
                #     search_rslt = 'no foundqq'





                # ---- end of your code --- #
                mysend(from_sock, json.dumps({"action":"search", "results":search_rslt}))
#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action":"disconnect"}))
                else:
                    for i in the_guys:
                        to_sock = self.logged_name2sock[i]
                        mysend(to_sock, json.dumps({"action":"quit", 'from':from_name}))
#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================
            elif msg["action"] == "game":
                mysend(from_sock, json.dumps({"action":"game","from": msg["from"], "results":'Game time now!!'}))
                # os.system('python my_game_key.py')
            elif msg['action'] == 'score':
                from_name = self.logged_sock2name[from_sock]
                self.dic_score[from_name] = msg['message']
            elif msg['action'] == 'get_score':
                from_name = self.logged_sock2name[from_sock]
                winner=''
                maxi_score=0
                for key,value in  self.dic_score.items():
                    if value>maxi_score:
                        winner=key
                        maxi_score=value
                the_guys = self.group.list_me(from_name)
                mysend(from_sock, json.dumps({"action":"exchange", "from":'system','message':'the winner is '+winner + ' and the score '+str(maxi_score)}))
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    mysend(to_sock, json.dumps({"action":"exchange", "from":'system','message':'the winner is '+winner + ' and the score '+str(maxi_score)}))
                self.dic_score = {}
                    # mysend(to_sock, "...index the messages before sending, or search won't work")

        else:
            #client died unexpectedly
            self.logout(from_sock)

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)

def main():
    server=Server()
    server.run()

main()
