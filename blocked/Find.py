
import tinydb

def Find():

    '''
    >>> Find()
    {}
    '''

    DataBase = tinydb.TinyDB('database/blocked.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Chat' : {}})

    return DataBase.all()[0]
