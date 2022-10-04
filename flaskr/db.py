from bson import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flaskr.configmodule import DB_SERVER

from flaskr.user import User

#connecting to the datebase and getting each of the collections
client = MongoClient(DB_SERVER,connect=False)

db = client["YouTubeWaterDB"]
users = db["users"]
rooms = db["rooms"]
room_members = db["room_members"]
states = db["states"]

def get_user(username):
    """
    If the user exists, return a User object with the username and password, otherwise return None
    
    :param username: The username of the user to be retrieved
    :return: A User object
    """
    user = users.find_one({"_id":username})
    return User(user["email"],user["_id"],user["password"]) if user else None

def save_user(email, username, pw):
    """
    It takes a username and password, hashes the password, and then inserts a document into the users
    collection with the username as the _id and the hashed password as the password
    
    :param username: the username of the user
    :param pw: the password you want to save
    """
    pw_hash = generate_password_hash(pw)
    
    users.insert_one({'_id':username,'email':email,'password':pw_hash})

def add_room_member(room_id,vid_id,username,is_admin=False):
    """
    It inserts a document into the room_members collection with the room_id and username as the _id, and
    the vid_id and is_admin as the other fields
    
    :param room_id: The id of the room
    :param vid_id: The id of the video that the room is for
    :param username: The username of the user who is joining the room
    :param is_admin: True if the user is an admin of the room, False otherwise, defaults to False
    (optional)
    """
    room_members.insert_one( {'_id':{'room_id':ObjectId(room_id),'username':username},'vid_id':vid_id,'is_admin':is_admin})

def get_room(room_id):
    return rooms.find_one({'_id':ObjectId(room_id)})

def get_room_of_user(username):
    return list(room_members.find({'_id.username':username}))

def get_room_members(room_id):
    """
    It returns a list of all the members in a room.
    
    :param room_id: the id of the room
    :return: A list of dictionaries.
    """
    return list(room_members.find({'_id.room_id':ObjectId(room_id)}))

def save_room(vid_id, admin_id):
    """
    It creates a new room in the database, and adds the admin as a member of that room
    
    :param vid_id: The id of the video that the room is for
    :param admin_id: The user id of the admin
    :return: The room_id
    """
    room_id = rooms.insert_one({'vid_id':vid_id,'admin':admin_id}).inserted_id
    add_room_member(room_id,vid_id,admin_id,is_admin=True)
    return room_id

def is_room_admin(room_id,admin_id):
    return room_members.count_documents( {'_id':{'room_id':ObjectId(room_id),'username':admin_id},'is_admin':True})

def is_room_member(room_id,username):
    return room_members.count_documents( {'_id':{'room_id':ObjectId(room_id),'username':username}})

def remove_room_members(room_id,usernames):
    room_members.delete_many({'_id':{'$sin':[{'room_id':room_id,'username':username}for username in usernames] }})

def update_vid_id(room_id,vid_id):
    """
    The function takes in a room_id and a vid_id and updates the vid_id of the room
    
    :param room_id: The id of the room that the user is in
    :param vid_id: the id of the video that is getting changed
    """
    rooms.update_one( {'_id': ObjectId(room_id)},{'$set':{'vid_id':vid_id}})

def save_state(room_id,state):
    """
    If there is a document in the states collection with the room_id, delete it, then insert a new
    document with the room_id, state, and time.
    
    :param room_id: The id of the room you want to save the state of
    :param state: {'state':'state','time':'time'}
    """
    print(state['time'])
    if(states.count_documents({'room_id': ObjectId(room_id)})):
        states.update_one( {'room_id': ObjectId(room_id)},{'$set':{'state':state['state'],'time':state['time']}})
    else:
        states.insert_one( {'room_id': ObjectId(room_id),'state':state['state'],'time':state['time']})


def get_most_recent_state(room_id):
    """
    > Get the most recent state for a given room
    
    :param room_id: The room ID of the room you want to get the state of
    :return: A dictionary of the most recent state of the room.
    """
    tmp = states.find_one({'room_id':ObjectId(room_id)})
    return { 'state':tmp['state'],'time':tmp['time'] }