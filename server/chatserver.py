#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The most basic chat protocol possible.

run me with twistd -y chatserver.py, and then connect with multiple
telnet clients to port 1025
"""

from twisted.protocols import basic
from pprint import pprint as pp
class FlipprChat(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
        self.factory.clients.append(self)
        self.nick = "Nanashi"
        self.room_name = None

    def getMyRoom(self):
        return self.factory.rooms.get(self.room_name, None)

    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)
        if (self.room_name):
            self.getMyRoom().remove(self)
            if not self.getMyRoom():
                del(self.factory.rooms[self.room_name])

    def lineReceived(self, line):
        l = repr(line)
        join_position = l.find("join")
        if (join_position == 1):
            ## only one room can be joined by one person
            if self.room_name:
                return
            ## Adds this client to certain room
            room_name = l[6:-1]
            room = self.factory.rooms.get(room_name, None)
            if (room):
                room.append(self)
            else:
                self.factory.rooms[room_name] = [self]
            self.room_name = room_name
            self.message("Server:You has joined " + room_name + "\n")
            pp(room_name)
            return

        nick_position = l.find("nick")
        pp(nick_position)
        pp(len(l))
        if (nick_position == 1):
            ## Adds the nickname to the user
            self.nick = l[l.find(' '):-1]
            self.message('Server:You are known as ' + self.nick)
            return
        print "received", repr(line)
        if self.room_name:
            room = self.getMyRoom()
            for c in room:
                c.message(self.nick + ":" + line)
        else:
            self.message("Server:You need to join some room")
#        for c in self.factory.clients:
#            c.message(line)

    def message(self, message):
        self.transport.write(message + '\n')


from twisted.internet import protocol
from twisted.application import service, internet

factory = protocol.ServerFactory()
factory.protocol = FlipprChat
factory.clients = []
factory.rooms = {}

application = service.Application("chatserver")
internet.TCPServer(1025, factory).setServiceParent(application)
