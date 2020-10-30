import re

class House(object):
    def __init__(self, address, link, price, size = '? m²'):
        self.address = address
        self.link = link
        self.price = price
        self.size = size

    def __str__(self):
        return self.address

    def toMarkdown(self) -> str:
        return self.escape(f"""
{self.link}

{self.size}, {self.price}
""")

    def escape(self, text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'

        return re.sub('([{}])'.format(re.escape(escape_chars)), r'\\\1', text)
