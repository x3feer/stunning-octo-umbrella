from .Find import Find
from .Update import Update

def CheckRef(Ref):

    Ref = str(Ref)

    Find_ = Find()
    Chats = []

    for Chat in Find_['Chat'].keys():

        for Mode in Find_['Chat'][Chat].keys():

            if Ref == Find_['Chat'][Chat][Mode]['Ref']:
                
                if len(Chats) == 0:
                    Chats.append(True)


                if not Mode in Chats:
                    Chats.append(Mode)

                if not Chat in Mode:
                    Chats.append(Chat)

    if len(Chats) != 0:
        return Chats

    else:
        return [False]
