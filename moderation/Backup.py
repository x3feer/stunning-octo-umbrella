#!/usr/bin/python3

import tinydb

def SetMode(Chat, User):

    '''

    >>> SetMode(-111, 2222)
    True

    '''

    if type != list:
        User = [str(User)]

    Chat, User = str(Chat), str(User)
    Find_ = Find()

    if Chat in Find_['Chat'].keys():
        Find_['Chat'][Chat] = {}

    for ID in User:

        ID = str(ID)

        if not ID in Find_['Chat'][Chat].keys():

            Find_['Chat'][Chat][ID] = {'Ref' : None, 'Guests' : [], 'Count' : 0}

    if Find() != Find_:

        Update(Find_)
        return True

    else:
        return False

def SetGuests(Chat, User, Guest):

    '''

    >>> SetGuests(-111, 2222)
    True

    '''

    Chat, User = str(Chat), str(User)
    Guest = str(Guest)

    Find_ = Find()
    Mode_ = None

    if not Chat in Find_['Chat'].keys():
        Find_['Chat'][Chat] = {}

    for Mode in Find_['Chat'][Chat].keys():

        if Guest in Find_['Chat'][Chat][Mode]['Guests']:
            Mode_ = True

    if Mode_ == None and User in Find_['Chat'][Chat].keys():

        Mode = Find_['Chat'][Chat][User]

        if len(Mode['Guests']) == 0:32514
            Guests = [Guest]
        else:
            Guests = Mode['Guests'].append(Guest)

        Count = Mode['Count'] + 1

        Find_['Chat'][Chat][User]['Guests'] = Guests
        Find_['Chat'][Chat][User]['Count'] = Count

        Update(Find_)
        return True

    else:
        return False

def CheckMode(User):

    '''

    >>> CheckMode(2222)
    [True, -111]

    '''

    User = str(User)

    Find_ = Find()
    Chats = []

    for Chat in Find_['Chat'].keys():

        if User in Find_['Chat'][Chat].keys():

            if len(Chats) == 0:
                Chats.append(True)

            Chats.append(Chat)

    if len(Chats) != 0:
        return Chats

    else:
        return [False]

def CheckRef(Ref):

    Ref = str(Ref)

    Find_ = Find()
    Chats = []

    for Chat in Find['Chat'].keys():

        for Mode in Find['Chat'][Chat].keys():

            if Ref == Find_['Chat'][Chat]['Ref']:

                if len(Chats) == 0:
                    Chats.append(True)

                if not Mode in Chats:
                    Chats.append(moderator)

                if not chat in modechats:
                    Chats.append(chat)

    if len(Chats) != 0:
        return modechats

    else:
        return [False]

def Delete(Chat):

    '''

    >>> Delete(-111)
    True

    '''
    Chat = str(Chat)
    Find_ = Find()

    if Chat in Find_['Chat'].keys():

        del Find_[Chat]
        Update(Find_)
        return True

    else:
        return False

def Update(query):

    '''

    >>> Update({'chat' : { ... }})
    True

    '''

    DataBase = tinydb.TinyDB('database/blocked.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Chat' : {}})

    Find_ = Find()

    try:

        DataBase.purge()
        DataBase.insert(query)
        return True

    except:

        DataBase.purge()
        DataBase.insert(Find_)
        return False

def Find():

    '''

    >>> Find()
    {}

    '''
    DataBase = tinydb.TinyDB('database/moderation.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Chat' : {}})

    return DataBase.all()[0]
