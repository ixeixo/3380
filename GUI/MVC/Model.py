import re


class Model:
    def __init__(self, email):
        self.email = email




    # sample code 

    #@property
    #def email(self):
    #    return self.__email

    #@email.setter
    #def email(self, value):
    #    """
    #    Validate the email
    #    :param value:
    #    :return:
    #    """
    #    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    #    if re.fullmatch(pattern, value):
    #        self.__email = value
    #    else:
    #        raise ValueError(f'Invalid email address: {value}')

    #def save(self):
    #    """
    #    Save the email into a file
    #    :return:
    #    """
    #    with open('emails.txt', 'a') as f:
    #        f.write(self.email + '\n')