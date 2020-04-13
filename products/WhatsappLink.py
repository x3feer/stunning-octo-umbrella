
import urllib.parse

def WhatsappLink(telephone, message):

    '''

    >>> WhatsappLink(9999999, 'Hello Word!')

    https://api.whatsapp.com/send?phone= ....

    '''

    message = urllib.parse.quote(message)

    return 'https://api.whatsapp.com/send?phone=' + str(telephone).replace(' ', '') + '&text=' + str(message).replace(' ', '')
