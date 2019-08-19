from lxml import html
import requests

page = requests.get('https://testnet.faircoin.world/')
tree = html.fromstring(page.content)

div = tree.xpath('//div[@class="class"]/text()')

table = tree.xpath('//table[@class="table table-condensed table-striped table-hover"]/text()')

print(div, table)
