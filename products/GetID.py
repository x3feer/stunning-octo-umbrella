import hashlib

def GetID(query):

    '''
    >>> GetID('320145ABC')
    f970e2767d0cfe75876ea857f92e319b
    '''

    return hashlib.md5(str(query).encode()).hexdigest()
