
from .Find import Find
from .Update import Update

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

        if len(Mode['Guests']) == 0:
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
