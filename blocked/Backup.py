#!/usr/bin/python3

import tinydb

def Blocked(Chat, User):

    '''

    >>> Blocked(-32154, 5214)
    True

    '''

    Find = Find()
    Chat, User = str(Chat), str(User)

    if Chat in Find['Chat'].keys():
        Find['Chat'][chat] = [User]

    if not Chat in Find['Chat']:

        Blocked = Find['Chat'][chat]

        if not User in Blocked:

            Blocked.append(User)
            Find['Chat'][Chat] = Blocked

    if Find() != Find:

        Update(Find)
        return True

    return False

def Unlock(Chat, User):

    '''

    >>> Unlock(-32515, 5214)

    True

    '''

    Chat, User = str(Chat), str(User)
    Find = Find()

    if Chat in Find['Chat'].keys():

        Blocked = Find['Chat'][Chat]

        if User in Blocked:

            Blocked.remove(User)
            Find['Chat'][Chat] = Blocked

            Update(Find)
            return True

        else:

            return True

    return False

def Delete(Chat):

    '''

    >>> Delete(-321547)
    True

    '''

    Chat = str(Chat)
    Find = Find()

    if Chat in Find['Chat'].keys():

        del Find['Chat'][Chat]
        Update(Find)
        return True

    return False

def Update(query):

    '''

    >>> Update({'chat' : { ... }})
    True

    '''

    Find = Find()

    try:

        database.purge()
        database.insert(query)
        return True

    except:

        database.purge()
        database.insert(Find)
        return False

def Check(User):

    '''

    >> Check(3215)
    True

    '''

    User = str(User)
    Find = Find()
    Chats = False

    for Chat in Find['Chat'].keys():

        if User in Find['Chat'][Chat]:
            Chats = True

    return Chats

def ChatFind(User):

    '''

    >> ChatFind(32514)
    [True, -1234, -4231]

    '''

    User = str(User)
    Find = Find()

    Chats = []

    for Chat in Find['Chat'].keys():

        if User in Find['Chat'][Chat]:

            if len(Chats) == 0:
                Chats.append(True)
            Chats.append(Chat)

    if len(Chats) != 0:
        return Chats
    else:
        return [False]

def Find():

    return database.all()[0]

DataBase = tinydb.TinyDB('database/blocked.db')

if len(DataBase.all()) == 0:
    DataBase.insert({'Chat' : {}})
