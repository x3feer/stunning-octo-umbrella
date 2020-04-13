import tinydb

def Find():

    '''

    >>> Find()
    {}

    '''
    DataBase = tinydb.TinyDB('database/products.db')

    if len(DataBase.all()) == 0:
        DataBase.insert({'Products' : {}})

    return DataBase.all()[0]
