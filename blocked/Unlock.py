
from .Find import Find
from .Update import Update

def Unlock(Chat, User):

    '''

    >>> Unlock(-32515, 5214)

    True

    '''

    Chat, User = str(Chat), str(User)
    Find_ = Find()

    if Chat in Find_['Chat'].keys():

        Blocked = Find_['Chat'][Chat]

        if User in Blocked:

            Blocked.remove(User)
            Find_['Chat'][Chat] = Blocked

            Update(Find_)
            return True

        else:

            return True

    return False
