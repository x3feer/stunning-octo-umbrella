#!/usr/bin/python3

#

import urllib.parse
import hashlib
import tinydb

#

def WhatsappLink(self, telephone, message):

    message = urllib.parse.quote(message)

    return 'https://api.whatsapp.com/send?phone=' + str(telephone) + '&text=' + str(message)

def SetProduct(Telephone, Title, Message):

    Telephone, Title, Message = str(Telephone), str(Title), str(Message)

    Find_, GetID_ = Find(), GetID(Telephone + Title + Message)

    if not GetID_ in Find_['Products'].keys():

        Find_['Products'][GetID_] = {
            'Telephone' : Telephone, 'Title' : Title, 'Message' : Message,
            'WhatsappLink' : WhatsappLink(Telephone + Message)
        }
        
        Update(Find_)
        return True

    else:
        return False

def Delete(ID):

    Find_ = Find()

    if ID in Find_['Products'].keys():

        del Find_['Products'][ID]
        Update(Find_)
        return True

    else:
        return False

def GetID(query):

    '''
    >>> GetID('320145ABC')
    f970e2767d0cfe75876ea857f92e319b
    '''

    return hashlib.md5(str(query).encode()).hexdigest()

def Update(query):

    '''

    >>> Update({'chat' : { ... }})
    True

    '''

    DataBase = tinydb.TinyDB('database/moderation.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Products' : {}})

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
    DataBase = tinydb.TinyDB('database/products.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Products' : {}})

    return DataBase.all()[0]
