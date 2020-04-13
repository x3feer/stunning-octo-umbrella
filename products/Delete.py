
from .Update import Update
from .Find import Find

def Delete(ID):

    '''
    Delete('f970e2767d0cfe75876ea857f92e319b')
    True
    '''

    Find_ = Find()

    if ID in Find_['Products'].keys():

        del Find_['Products'][ID]
        Update(Find_)
        return True

    else:
        return False
