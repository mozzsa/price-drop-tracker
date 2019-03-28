import re
from passlib.hash import pbkdf2_sha512

class Utils(object):

    #checks if the e-mail is valid
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    # returns sha512->pbkdf2_sha512 encrypted password
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    #hashed_password: pbkdf2_sha512 encrypted password
    #password : sha512-hashed password
    @staticmethod
    def check_hashed_password(password, hashed_password):
       return pbkdf2_sha512.verify(password, hashed_password)

    #convert price string to float , it does not matter whether price text represented with "," or "."
    @staticmethod
    def get_price_float(price_text):
        index = re.search(r"[,.]", price_text[::-1]).start()
        begin = price_text[:len(price_text) - index]
        end = price_text[len(price_text) - index:]
        return float(re.sub(r"([.,])", "", begin) + "." + end)
