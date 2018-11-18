# coding: utf8

from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from bs4 import BeautifulSoup
import wikipedia
import vk_api
import requests

def main():
    session = requests.Session()

    '''авторизоваться как пользователь'''

    # login, password = 'login','password'
    # vk.session = vk_api.VkApi(login, password)
    #
    # try:
    #     vk.session.auth()
    # except vk_api.AuthError as error_msg:
    #     print(error_msg)

    ''' авторизоваться как сообщество'''

    vk_session = vk_api.VkApi(token = '')
    vk = vk_session.get_api()
    upload = VkUpload(vk_session) # для изображений
    longpool = VkLongPoll(vk_session)
    wikipedia.set_lang('ru')

    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('id_vk{}: "{}"'.format(event.user_id, event.text), end = ' ')

            try:
                wiki = wikipedia.page(event.text)
                content = wiki.content
                stop = content.find('==')
                text = content[0:stop] + "\n Страница в Wiki: " + wiki.url

            except wikipedia.exceptions.DisambiguationError as e:
                #wiki = wikipedia.page(event.text)
                #text = "Имеется множество страниц. Подробнее в Wiki: " + wiki.url
                #continue
                #text = {0}.format(e)
                #one = e
                #two = ''.join(wiki.url)
                text = e
            except wikipedia.exceptions.PageError as e:
                #wiki = wikipedia.page(event.text)
                text = e


                #continue
            if not text:
                vk.message.send(
                    user_id = event.user_id,
                    message = 'Я запутался')
                print('no result')
                continue

            attachments = []
            vk.messages.send(
                user_id = event.user_id,
                attachments = ','.join(attachments),
                message = text)
            print('Выполнено')

if __name__ == '__main__':
    main()

