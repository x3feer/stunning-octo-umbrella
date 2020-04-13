
from .Find import Find
from .Update import Update

def Delete(Chat):

    '''

    >>> Delete(-111)
    True

    '''
    Chat = str(Chat)
    Find_ = Find()

    if Chat in Find_['Chat'].keys():

        del Find_['Chat'][Chat]
        Update(Find_)
        return True

    else:
        return False
