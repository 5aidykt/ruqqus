import os
import logging
import redis
import gevent
from flask import *
from flask_socketio import *

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.get import *
from ruqqus.__main__ import app, socketio

REDIS_URL = app.config["CACHE_REDIS_URL"]

#app = Flask(__name__)
#app.debug = 'DEBUG' in os.environ

redis = redis.from_url(REDIS_URL)

@socketio.on('connect')
def socket_connect_auth_user():

    v, client=get_logged_in_user()

    if client or not v:
        send("Not logged in")
        disconnect()




@socketio.on('my event')
#@auth_desired
def socket_test(json, v=None):

    print(f"received json {str(json)}")
    emit('my response',{'test':'foobar'})


@app.route("/socket_home")
@auth_required
def socket_home(v):

    return render_template("chat/chat_test.html", v=v)


# class ChatBackend(object):
#     """Interface for registering and updating WebSocket clients."""

#     def __init__(self, guildname):
#         self.clients = list()
#         self.pubsub = redis.pubsub()
#         self.pubsub.subscribe(guildname)

#     def __iter_data(self):
#         for message in self.pubsub.listen():
#             data = message.get('data')
#             if message['type'] == 'message':
#                 app.logger.info(u'Sending message: {}'.format(data))
#                 yield data

#     def register(self, client):
#         """Register a WebSocket connection for Redis updates."""
#         self.clients.append(client)

#     def send(self, client, data):
#         """Send given data to the registered client.
#         Automatically discards invalid connections."""
#         try:
#             client.send(data)
#         except Exception:
#             self.clients.remove(client)

#     def run(self):
#         """Listens for new messages in Redis, and sends them to clients."""
#         for data in self.__iter_data():
#             for client in self.clients:
#                 gevent.spawn(self.send, client, data)
#             if not self.clients:
#                 gevent.sleep(10)
#                 if not self.clients:
#                     break

#     def start(self):
#         """Maintains Redis subscription in the background."""
#         gevent.spawn(self.run)

# CHATS = {}


# @sockets.route('/chat/<guildname>/inbox')
# #@is_not_banned
# def inbox(ws, guildname):

#     print('submit websocket')
#     """Receives incoming chat messages, inserts them into Redis."""

#     #guild=get_guild(guildname, graceful=True)
#     guild=get_guild(guildname, graceful=True)
#     #if not guild or guild.is_banned:
#     #    ws.close()
#     #    return

#     if guild.name not in CHATS:
#         CHATS[guild.name]=ChatBackend(guild.name)
#         CHATS[guild.name].start()

#     while not ws.closed:
#         # Sleep to prevent *constant* context-switches.
#         gevent.sleep(0.1)
#         message = ws.receive()

#         if message:
#             #app.logger.info(f'Inserting message: {message}')
#             redis.publish(guild.name, message)

# @sockets.route('/chat/<guildname>/outbox')
# #@is_not_banned
# def outbox(ws, guildname):
#     #print(args)

#     #guild=get_guild(guildname, graceful=True)
    
#     guild=get_guild(guildname, graceful=True)
#     #if not guild or guild.is_banned:
#     #    ws.close()
#     #    return

#     if guild.name not in CHATS:
#         CHATS[guild.name]=ChatBackend(guild.name)
#         CHATS[guild.name].start()

#     """Sends outgoing chat messages, via `ChatBackend`."""
#     CHATS[guild.name].register(ws)

#     while not ws.closed:
#         # Context switch while `ChatBackend.start` is running in the background.
#         gevent.sleep(0.1)


# @app.route("/+<guildname>/chat", methods=["GET"])
# @is_not_banned
# def guild_chat_get(guildname, v):

#     b=get_guild(guildname)

#     return render_template(
#         "chat/chat.html",
#         v=v,
#         b=b
#         )