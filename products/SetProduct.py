
from .WhatsappLink import WhatsappLink
from .Find import Find
from .GetID import GetID
from .Update import Update

def SetProduct(Telephone, Title, Message):

    '''
    >>> SetProduct(9999999, 'Send Message', 'Hello!')
    True
    '''

    Telephone, Title, Message = str(Telephone), str(Title), str(Message)

    Find_, GetID_ = Find(), GetID(Telephone + Title + Message)

    if not GetID_ in Find_['Products'].keys():

        Find_['Products'][GetID_] = {
            'Telephone' : Telephone, 'Title' : Title, 'Message' : Message,
            'WhatsappLink' : WhatsappLink(Telephone, Message).replace(' ', '')
        }

        Update(Find_)
        return True

    else:
        return False
