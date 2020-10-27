import re

class House(object):
    def __init__(self, city, address, link, price, image, size):
        self.city = city
        self.address = address
        self.link = link
        self.price = price
        self.image = image
        self.size = size

    def toMarkdown(self) -> str:
        return self.escape(f"""
{self.link}

{self.size}, {self.price}
""")

    def escape(self, text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'

        return re.sub('([{}])'.format(re.escape(escape_chars)), r'\\\1', text)
