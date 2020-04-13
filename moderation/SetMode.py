
from .Find import Find
from .Update import Update
from .GetRef import GetRef

def SetMode(Chat, User):

    '''

    >>> SetMode(-111, 2222)
    True

    '''

    if type(User) != list:

        User = str(User).replace(',', ' ').split()

    Chat = str(Chat)
    Find_ = Find()

    if not Chat in Find_['Chat'].keys():
        Find_['Chat'][Chat] = {}

    for ID in User:

        if not ID in Find_['Chat'][Chat].keys():

            Find_['Chat'][Chat][ID] = {'Ref' : GetRef(ID), 'Guests' : [], 'Count' : 0}

    if Find() != Find_:

        Update(Find_)
        return True

    else:
        return False
