
from .Find import Find
import tinydb

def Update(query):

    '''

    >>> Update({'chat' : { ... }})
    True

    '''

    DataBase = tinydb.TinyDB('database/products.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Products' : {}})

    Find_ = Find()

    try:

        DataBase.purge()
        DataBase.insert(query)
        return True

    except:

        DataBase.purge()
        DataBase.insert(Find_)
        return False
