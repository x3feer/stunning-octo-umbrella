
from .Find import Find
from .Update import Update

def Blocked(Chat, User):

    '''

    >>> Blocked(-32154, 5214)
    True

    '''

    Find_ = Find()
    Chat, User = str(Chat), str(User)

    if Chat in Find_['Chat'].keys():
        Find_['Chat'][Chat] = [User]

    if not Chat in Find_['Chat'].keys():

        Find_['Chat'][Chat] = []

        Blocked = Find_['Chat'][Chat]

        if not User in Blocked:

            Blocked.append(User)
            Find_['Chat'][Chat] = Blocked

    if Find() != Find_:

        Update(Find_)
        return True

    return False
