
from .Find import Find
from .Update import Update

def Check(User):

    '''

    >> Check(3215)
    True

    '''

    User = str(User)
    Find_ = Find()
    Chats = []

    for Chat in Find_['Chat'].keys():

        if User in Find_['Chat'][Chat]:

            if len(Chats) == 0:
                Chats.append(True)
            Chats.append(Chat)

    if len(Chats) != 0:
        return Chats
    else:
        return [False]
