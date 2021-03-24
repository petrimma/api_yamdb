import random
import string


class Generator:
    def __init__(self):
        self.digits = string.digits

    def code_generator(self, length=6):
        """
        Генерирует случайную числовую комбинацию
        :param length: длина числа
        :return:
        """
        return ''.join(random.choice(self.digits)
                       for i in range(length))

    def login_email_generator(self, email, length=5):
        """
        Генерирует рендомный username на основе почтового логина
        :param email: имя почтового ящика для генерации
        :param length: длина случайных чисел добавляемых к имени
        :return:
        """
        email_username = email.split("@")[0]
        return f'{email_username}{self.code_generator(length)}'
