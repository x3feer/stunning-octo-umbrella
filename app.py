#!/usr/bin/python3

#

from telepot.namedtuple import InlineKeyboardMarkup
from telepot.namedtuple import InlineKeyboardButton

import telepot

import moderation
import blocked
import products
import onetime

import urllib3
import time
import re

#

class Features: # Features

    def __init__(self):
        pass

    def GetModerators(self, Chat_ID):

        (Chat_ID, Moderators) = (str(Chat_ID), [])

        for Moderator in Bot.getChatAdministrators(Chat_ID):
            Moderators.append(str(Moderator['user']['id']))

        return Moderators

    def GetMe(self):
        return Bot.getMe()

#

class Private: # Private chat

    def __init__(self, Message):

        #

        self.Message_Type = None
        self.Message = Message

        try:

            self.Query_ID, self.Chat_ID, self.Query_Data = telepot.glance(self.Message, flavor='callback_query')
            self.Message_Type = 'Callback'

        except:

            self.Content_Type, self.Chat_Type, self.Chat_ID = telepot.glance(self.Message)
            self.Message_Type = 'Chat'

        #

        if self.Message_Type == 'Chat':

            if self.Message['text'] in ['/start', '/menu']:
                self.Menu()

            elif self.Message['text'].count('-') == 2:
                self.Products()

            elif self.Message['text'].count('-') == 7:
                self.Unlock()

            elif re.findall('[\d]+', self.Message['text']):
                self.Products()

        #

        if self.Message_Type == 'Callback':

            print(self.Query_Data)

            if self.Query_Data in ['back_to_menu']:
                self.Menu()

            elif self.Query_Data in ['back_to_menu']:
                self.Menu()

            elif self.Query_Data in ['products', 'new_product', 'del_product', 'confirm_new_product', 'confirm_del_product', 'show_product', 'show_product_user']:
                self.Products()

            elif len(self.Query_Data) == 32:
                self.Products()

            elif self.Query_Data in ['account']:
                self.Account()

            elif self.Query_Data in ['report']:
                self.Report()

            elif self.Query_Data in ['unlock', 'unlock_info', 'unlock_group_list']:
                self.Unlock()

            elif re.findall('\-[\d]+', self.Query_Data):
                self.Unlock()

    def Menu(self): # Menu

        Select_Button[self.Chat_ID] = 'Menu'

        if self.Message_Type == 'Callback':

            (Name, MessageID) = (self.Message['message']['chat'], None)
            try:
                Bot.deleteMessage((self.Chat_ID,  self.Message['message']['message_id']))
            except:
                pass

        if self.Message_Type == 'Chat':

            (Name, MessageID) = (self.Message['chat'], self.Message['message_id'])
            try:
                Bot.deleteMessage((self.Chat_ID,  self.Message['message_id'] - 1))
            except:
                pass
        Name = Name['first_name'].split()[0].title()

        Message = '🎉 [ Menu ]\n\n'
        Message = '🎉 Olá, {0}! Como posso \nte ajudar? 😀'.format(Name)
        Message+= '\n\n- x -\n\n'

        if moderation.CheckMode(self.Chat_ID)[0] == True:

            Keyboard = InlineKeyboardMarkup(inline_keyboard=[

                [InlineKeyboardButton(text='Minha Conta', callback_data='account')],
                [InlineKeyboardButton(text='Meus Produtos', callback_data='products')],
                [InlineKeyboardButton(text='Meu Relatorio', callback_data='report')]

            ])

            return Bot.sendMessage(self.Chat_ID, Message, reply_to_message_id=MessageID, reply_markup=Keyboard)

        else:

            Check = blocked.Check(self.Chat_ID)

            Keyboard = []

            if Check[0] == True:

                ExportChatInvitedLink = Bot.exportChatInviteLink(Check[1])
                Keyboard.append(InlineKeyboardButton(text='Voltar ao Grupo', url=ExportChatInvitedLink))

            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Desbloquear Acesso ', callback_data='unlock')],
                [InlineKeyboardButton(text='Mostrar Produtos', callback_data='show_product_user')],
                Keyboard
            ])

            return Bot.sendMessage(self.Chat_ID, Message, reply_to_message_id=MessageID, reply_markup=Keyboard)

    def Products(self): # Products

        global Select_Button
        global Select_Product
        global _Secret

        if self.Message_Type == 'Callback':
            try:
                Bot.deleteMessage((self.Chat_ID, self.Message['message']['message_id']))
            except:
                pass
        if self.Message_Type == 'Chat':
            try:
                Bot.deleteMessage((self.Chat_ID,  self.Message['message_id'] - 1))
            except:
                pass

        if not self.Chat_ID in Select_Button.keys():
            return False

        if moderation.CheckMode(self.Chat_ID)[0] == True and self.Message_Type == 'Chat':

            if self.Message['text'].count('-') == 2 and Select_Button[self.Chat_ID] == 'new_product':

                Telephone, Title, Message = self.Message['text'].split('-')
                #
                Select_Product[self.Chat_ID] = {'Telephone' : Telephone, 'Title' : Title, 'Message' : Message, 'Attempt' : 0}
                Select_Button[self.Chat_ID] = '2fa_new_product'
                #
                Message = '🎉 [ Codico de Confirmação ]\n\n'
                Message+= '📌 Para prosseguirmos insira o códico do 2FA do Google Autenticador.\n\n'
                Message+= '- x - \n\n'
                #

                Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')],
                ])

                Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

            elif re.findall('[\d]+', self.Message['text']):

                if not self.Chat_ID in Select_Product.keys():
                    return False

                if Select_Button[self.Chat_ID] in ['2fa_new_product', '2fa_del_product']:

                    #

                    Attempt = Select_Product[self.Chat_ID]['Attempt']
                    Coding = re.findall('[\d]+', self.Message['text'])[0]

                    #

                    if onetime.CheckCode(_Secret, Coding) == True and Attempt < 3:

                        #
                        OptionsMessage = {
                            '2fa_del_product' : 'deletar',
                            '2fa_new_product' : 'adicionar'
                        }[Select_Button[self.Chat_ID]]
                        #

                        Message = '🎉 Você tem certeza que quer {0} este produto? 🤔'.format(OptionsMessage)
                        Message+= '\n\n - x -\n\n'

                        OptionsCallbackData = {
                            '2fa_del_product' : 'confirm_del_product',
                            '2fa_new_product' : 'confirm_new_product'
                        }[Select_Button[self.Chat_ID]]
                        #

                        Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Confirmar ✅' , callback_data=OptionsCallbackData)],
                            [InlineKeyboardButton(text=' Cancelar ❌' , callback_data='products')]
                        ])
                        #
                        OptionsAccept = {
                            '2fa_del_product' : '2fa_del_product_accept',
                            '2fa_new_product' : '2fa_new_product_accept'
                        }[Select_Button[self.Chat_ID]]

                        Select_Button[self.Chat_ID] = OptionsAccept
                        #

                        return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                    elif Attempt >= 3:

                        #
                        Message = '🎉 Você não tem mais tentativas disponíveis!'
                        Message+= '\n\n - x - \n\n'

                        Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Voltar' , callback_data='products')],
                        ])

                        #

                        return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)
                        #

                    else:

                        Select_Product[self.Chat_ID]['Attempt'] = Attempt + 1
                        #
                        Message = '🎉 [ Códico Inválido ]\n\n'
                        Message+= '📌 Seu código está incorreto por favor insira outro código novamente!\n\n'
                        #
                        if Attempt == 1:
                            Message += '📌 Caso não tenha sucesso, verifique se a hora do seu dispositivo está correta.\n\n'
                        #
                        Message += '- x - \n\n'

                        Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Cancelar ❌' , callback_data='products')],
                        ])

                        return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

        elif self.Message_Type == 'Callback':

            if self.Query_Data in ['show_product_user', 'show_product']:

                print(self.Query_Data)

                Message = '🎉 [ Produtos ] \n\n'
                Message+= '📌 Estes são alguns dos nossos produtos. '
                Message+= 'Caso tenha interesse em algum deles, basta clicar no botão referente ao produto desejado 😁'
                Message+= '\n\n - x - \n\n'

                Products_ = []

                for product in products.Find()['Products'].keys():

                    product_ = products.Find()['Products'][product]
                    Products_.append(InlineKeyboardButton(text=product_['Title'], url=product_['WhatsappLink']))

                callback_data = {
                    'show_product_user' : 'back_to_menu',
                    'show_product' : 'products'
                }[self.Query_Data]

                Keyboard = InlineKeyboardMarkup(inline_keyboard=[Products_, [InlineKeyboardButton(text='Voltar', callback_data=callback_data)]])

                return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

            elif moderation.CheckMode(self.Chat_ID)[0] == True:

                if not self.Chat_ID in Select_Button.keys():
                    return None

                if self.Query_Data == 'products': # Products menu

                    if self.Chat_ID in Select_Product.keys():
                        del Select_Product[self.Chat_ID]
                    #
                    Select_Button[self.Chat_ID] = 'products'

                    Message = '🎉 [ Gerenciador de Produtos ]\n\n'
                    Message+= '📌 Você pode adicionar novos produtos ou deletar algum produto do Bot 😁'
                    Message+= '\n\n - x - \n\n'
                    #
                    Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Adicionar Produto 🛒' , callback_data='new_product')],
                        [InlineKeyboardButton(text='Deletar Produto 🛒', callback_data='del_product')],
                        [InlineKeyboardButton(text='Mostrar Produtos 🛒', callback_data='show_product')],
                        [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')]
                    ])
                    #
                    return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                elif self.Query_Data == 'new_product': # New Product

                    Select_Button[self.Chat_ID] = 'new_product'
                    #
                    Message = '🎉 [ Adicionando Produto ]\n\n'
                    Message+= '📌 Para adicionar um novo produto basta seguir este padrão de mensagem é enviar no chat 😁\n\n'
                    Message+= '>> Telefone - Titulo - Menssagem\n\n'
                    Message+= 'Exemplo:``` 9999999 - Camiseta - Olá! Poderia me falar mais sobre as camisetas```'
                    Message+= '\n\n - x - \n\n'
                    #
                    Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Voltar', callback_data='products')],
                    ])
                    #
                    return Bot.sendMessage(self.Chat_ID, Message, parse_mode='Markdown', reply_markup=Keyboard)

                elif self.Query_Data == 'confirm_new_product': # Confirm new product

                    if Select_Button[self.Chat_ID] == '2fa_new_product_accept':

                        if not self.Chat_ID in Select_Product.keys():
                            return None

                        Product = Select_Product[self.Chat_ID]

                        Telefone, Title, Message = Product['Telephone'], Product['Title'], Product['Message']
                        SetProduct_ = products.SetProduct(Telefone, Title, Message)

                        if SetProduct_ == True:

                            del Select_Product[self.Chat_ID]

                            Message = '🎉 Parabéns! Este produto foi adicionado com sucesso 😁'
                            Message+= '\n\n- x - \n\n'

                            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='Voltar', callback_data='products')],
                            ])

                            return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                        else:

                            Message = '🎉 Ops! Não foi possível adicionar este produto!'
                            Message+= '\n\n - x - \n\n'

                            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='Voltar', callback_data='products')],
                            ])

                            return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                elif self.Query_Data == 'confirm_del_product':

                    if Select_Button[self.Chat_ID] == '2fa_del_product_accept':

                        if not self.Chat_ID in Select_Product.keys():
                            return None

                        del_product = Select_Product[self.Chat_ID]['ID']

                        if products.Delete(del_product) == True:

                            Message = '🎉 Parabéns! Você conseguiu deletar o produto com sucesso 😁'
                            Message+= '\n\n - x - \n\n'

                            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')],
                            ])

                            return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                        else:

                            Message = '🎉 Ops! Vou não conseguiu deletar o produto ☹️'
                            Message+= '\n\n - x - \n\n'

                            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')],
                            ])

                            return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                elif self.Query_Data == 'del_product':

                    Select_Button[self.Chat_ID] = 'del_product'
                    #
                    Message = '🎉 [ Deletando Produto ]\n\n'
                    Message+= '📌 Selecione o produto que deseja deletar 😁\n\n'
                    Message+= ' - x - \n\n'
                    #
                    Products_Find = products.Find()['Products']
                    Products_All = []

                    for product_id in Products_Find.keys():
                        Products_All.append(InlineKeyboardButton(text=Products_Find[product_id]['Title'] + '❌', callback_data=product_id))
                    #
                    Keyboard = InlineKeyboardMarkup(inline_keyboard=[Products_All, [InlineKeyboardButton(text='Voltar', callback_data='products')]])

                    return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

                elif len(self.Query_Data) == 32:

                    if Select_Button[self.Chat_ID] == 'del_product':

                        #
                        Select_Button[self.Chat_ID] = '2fa_del_product'
                        Select_Product[self.Chat_ID] = {'ID' : self.Query_Data, 'Attempt' : 0}
                        #
                        Message = '🎉 [ Codico de Confirmação ]\n\n'
                        Message+= '📌 Para prosseguirmos insira o códico do 2FA do Google Autenticador.\n\n'
                        Message+= '- x - \n\n'
                        #
                        Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')],
                        ])

                        return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

    def Account(self): # Account

        if self.Message_Type == 'Callback':
            try:
                Bot.deleteMessage((self.Chat_ID, self.Message['message']['message_id']))
            except:
                pass
        if self.Message_Type == 'Chat':
            try:
                Bot.deleteMessage((self.Chat_ID,  self.Message['message_id'] - 1))
            except:
                pass

        if moderation.CheckMode(self.Chat_ID)[0] == True:

            Chats = moderation.CheckMode(self.Chat_ID)
            Find_ = moderation.Find()
            Count = 0

            for Chat in Chats:

                if Chat != True:
                    Count += Find_['Chat'][Chat][str(self.Chat_ID)]['Count']

            Message = '🎉 [ Minha Conta ]\n\n'
            Message+= '📌 Você convidou cerca de 0 pessoas com seu código de referência 😁\n\n'
            Message+= 'Código: ```{}```\n\n'.format(moderation.GetRef(self.Chat_ID))
            Message+= '- x - \n\n'

            Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Voltar', callback_data='back_to_menu')],
            ])

            Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard, parse_mode='Markdown')

    def Report(self): # Report

        if moderation.CheckMode(self.Chat_ID)[0] == True:

            Find_ = moderation.Find()
            Data_ = 'Nome, User, Convite, Count'

            for Chat in Find_['Chat'].keys():

                for Mode in Bot.getChatAdministrators(Chat):

                    Name, UserID = Mode['user']['first_name'].split()[0].title(), Mode['user']['id']
                    Convite, Count = moderation.GetRef(UserID), 0
                    Chats = moderation.CheckMode(UserID)

                    if Chats[0] == True:

                        for Chat in Chats:

                            if Chat != True:
                                Count += Find_['Chat'][Chat][str(UserID)]['Count']

                    if 'username' in Mode['user'].keys():
                        username = Mode['user']['username']
                    else:
                        username = UserID

                    Data_ += '\n{0}, {1}, {2}, {3}'.format(Name, username, Convite, Count)

            if len(Data_) > 26:

                file = open('report.csv', 'w')
                file.write(Data_)
                file.close()

                Bot.sendDocument(self.Chat_ID, open('report.csv', 'rb'))

    def Unlock(self): # Unlock

        global Select_Group
        global Select_Button

        try:
            Bot.deleteMessage((self.Chat_ID, self.Message['message']['message_id']))
        except:
            pass

        Chats = blocked.ChatFind(self.Chat_ID)

        if Chats[0] == True and self.Message_Type == 'Chat':

            try:
                Bot.deleteMessage((self.Chat_ID, self.Message['message']['message_id']))
            except:
                pass

            if not self.Chat_ID in Select_Button.keys():
                return False

            if Select_Button[self.Chat_ID] == 'unlock_info' and self.Message['text'].count('-') == 7:

                Ref = moderation.CheckRef(self.Message['text'])

                print(Ref)

                if Ref[0] == True and blocked.Check(self.Chat_ID)[0] == True:

                    if not self.Chat_ID in Select_Group.keys():
                        return None

                    Group_ID = Select_Group[self.Chat_ID]
                    Get_Chat = Bot.getChat(Group_ID)

                    if 'username' in Get_Chat.keys():

                        ChatLink = 'https://t.me/' + Get_Chat['username']

                    else:

                        ChatLink = Bot.exportChatInviteLink(Group_ID)

                    FirstName = Get_Chat['title'].split()[0].title()

                    Message = '🎉 [ Desbloqueado ]\n\n'
                    Message+= '📌 Parabéns! Seu acesso ao grupo {0} foi desbloqueado 😁\n\n'.format(FirstName)
                    Message+= '- x - \n\n'

                    Keyboard = InlineKeyboardMarkup(inline_keyboard=[

                        [InlineKeyboardButton(text='Voltar ao Grupo', url=ChatLink)],
                        [InlineKeyboardButton(text='Voltar ao Menu', callback_data='back_to_menu')]

                    ])

                    blocked.Unlock(Group_ID, self.Chat_ID)
                    try:
                        Bot.restrictChatMember(Group_ID, self.Chat_ID, can_send_messages=True, can_send_other_messages=True)
                    except:
                        pass

                    return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

        elif Chats[0] in [True, False] and self.Message_Type == 'Callback':

            if re.findall('\-[\d]+', self.Query_Data) and Select_Button[self.Chat_ID] == 'unlock_group_list':

                Name = self.Message['message']['chat']['first_name']
                Name = str(Name).split()[0].title()

                Message = '🎉 [ Desbloquear Meu Acesso ]'
                Message+= '\n\n📌 {0}! Preciso que você me envie o código de referência que você recebeu de um de nossos administradores 😀'.format(Name)
                Message+= '\n\nExemplo ➡️ 2CRT-71AB-C790-XXXX-XXX-30D2-XXXX-XXX-XXX-XXX'
                Message+= '\n\n - x - \n\n'

                Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Voltar ao Menu', callback_data='back_to_menu')]
                ])

                Select_Button[self.Chat_ID] = 'unlock_info'
                Select_Group[self.Chat_ID] = self.Query_Data

                return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

            elif self.Query_Data == 'unlock':

                Keyboard = []

                for Chat in Chats:

                    if not Chat in [True, False]:

                        name = str(Bot.getChat(Chat)['title']).split()[0].title()
                        Keyboard.append(InlineKeyboardButton(text=str(name) + ' ✔️', callback_data=str(Chat)))

                Message = '🎉 [ Desbloquear Conta ]\n\n'
                Message+= '📌 Escolha o grupo que você deseja inserir o código de referência 😀\n\n'
                Message+= ' - x - \n\n'

                Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    Keyboard, [InlineKeyboardButton(text='Voltar ao Menu', callback_data='back_to_menu')]
                ])

                if Chats[0] == True:
                    Select_Button[self.Chat_ID] = 'unlock_group_list'

                return Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)

class Public: # public chat

    def __init__(self, Message):

        self.Content_Type, self.Chat_Type, self.Chat_ID = telepot.glance(Message)
        self.Message = Message

        if self.Content_Type == 'text':

            if self.Message['text'] == '/produtos':
                self.product_menu()

            if self.Message['text'] == '/updatemode':
                self.update_mode()

        else:

            self.new_chat_member()
            self.left_chat_member()

    def new_chat_member(self): # new chat member

        if self.Content_Type == 'new_chat_member':

            User = self.Message['new_chat_member']['id']

            if User == Features().GetMe()['id']:

                moderation.SetMode(self.Chat_ID, Features().GetModerators(self.Chat_ID))
                blocked.Blocked(self.Chat_ID, 'None')
                blocked.Unlock(self.Chat_ID, 'None')
                return True

            elif blocked.Check(User)[0] == False and moderation.CheckMode(User)[0] == False:

                Name = self.Message['new_chat_member']['first_name']
                Name = Name.split()[0].title()

                Message = 'Olá, {0}! Bem-vindo (a) ao nosso grupo 😀\n\n'.format(Name)
                Message+= 'Para que eu possa liberar seu acesso, envie o código de referência no meu privado 🔓'
                Message += '\n\n - x - \n\n'

                Keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Desbloquear Accesso 🔓', url='https://t.me/' + Features().GetMe()['username'])]
                ])

                Bot.sendMessage(self.Chat_ID, Message, reply_to_message_id=self.Message['message_id'], reply_markup=Keyboard)
                Bot.restrictChatMember(self.Chat_ID, User, can_send_messages=False, can_send_other_messages=False)

                blocked.Blocked(self.Chat_ID, User)
                return True

    def left_chat_member(self): # left chat member

        if self.Content_Type == 'left_chat_member':

            User = self.Message['left_chat_member']['id']

            if User == Features().GetMe()['id']:

                moderation.Delete(self.Chat_ID)
                blocked.Delete(self.Chat_ID)

                return True

    def update_mode(self): # Update Mode

        AllMode = moderation.Find()['Chat'][str(self.Chat_ID)]

        if str(self.Message['from']['id']) in AllMode.keys():

            Moderators = []

            for Moderator in Features().GetModerators(self.Chat_ID):

                if not str(Moderator) in AllMode.keys():
                    Moderators.append(Moderator)

            if len(Moderators) != 0:

                moderation.SetMode(self.Chat_ID, Features().GetModerators(self.Chat_ID))

                Message = '🎉 [ Atualização ]\n\n'
                Message+= 'Lista de administradores foi atualizada com sucesso 😁'
                Message+= '\n\n - x - \n\n'

                Bot.sendMessage(self.Chat_ID, Message, reply_to_message_id=self.Message['message_id'])

                return True

    def product_menu(self): # product menu

        Message = '🎉 [ Produtos ] \n\n'
        Message+= '📌 Estes são alguns dos nossos produtos. '
        Message+= 'Caso tenha interesse em algum deles, basta clicar no botão referente ao produto desejado 😁'
        Message+= '\n\n - x - \n\n'

        Products_ = []

        for product in products.Find()['Products'].keys():

            product_ = products.Find()['Products'][product]
            Products_.append(InlineKeyboardButton(text=product_['Title'], url=product_['WhatsappLink']))

        if len(Products_) != 0:

            Keyboard = InlineKeyboardMarkup(inline_keyboard=[Products_])
            Bot.sendMessage(self.Chat_ID, Message, reply_markup=Keyboard)
            return True

        else:
            return False

class Telegram: # Select Chat

    def __init__(self, Message):

        self.Message = Message

        if 'message' in Message.keys():
            self.Chat_Type = self.Message['message']['chat']['type']
        else:
            self.Chat_Type = self.Message['chat']['type']

        if self.Chat_Type == 'supergroup':
            Public(self.Message)

        if self.Chat_Type == 'private':
            Private(self.Message)

if __name__ == '__main__':

    Production = False
    Develop = True

    if Production == True:

        proxy_url = 'http://proxy.server:3128'
        telepot.api._pools = {'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),}
        telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

    if Develop == True:

        telepot.api.set_proxy('https://192.168.42.129:44355')

    Token, _Secret = ('', '')

    Select_Button = {}
    Select_Product = {}
    Select_Group = {}

    Bot = telepot.Bot(Token)
    Bot.message_loop(Telegram)

    while True:
        time.sleep(5)
