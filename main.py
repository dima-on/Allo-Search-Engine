import requests
import until
from bs4 import BeautifulSoup
import sys
from handler_data import Product, DataHendler
import config
from html_handler import HandlerBlock
from handler_order import HendlerOrder
sys.stdout.reconfigure(encoding='utf-8')


class Req_part:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_html_code(self, prompt: str) -> str:
        params: dict[str, any] = {"q": prompt}
        response = requests.get(self.url, params=params)
        return response.content

    def get_element(self, element_type: str, element_class: str, html_code: str) -> list:
        finder = until.Finder(html_code=html_code)
        find_elements: list = finder.find_classes(element_type, element_class)

        return find_elements

class HandlerCode:
    def __init__(self, url, find_items: str, prompt: str) -> None:
        self.url = url
        self.prompt = prompt
        self.find_items = find_items
        self.filters: dict = {}

    def make_req(self, url: str, find_items: str, prompt: str) -> list:
        RP_class = Req_part(url=url)
        html_code = RP_class.get_html_code(prompt=prompt)
        elements = RP_class.get_element("div", find_items, html_code=html_code)

        return elements
    
    def hendler_blocks(self, blocks: list):
        products = []
        ind = 0
        for block in blocks:
            if ind >= 5:
                break
            HB_class = HandlerBlock(str(block))
            classes, others = HB_class.Handler()

            DH_class = DataHendler(classes_data=classes, others_data=others)

            product = DH_class.get_base_data()
 
            RP_class = Req_part(url=product.link)
            html_code = RP_class.get_html_code(None)

            product = self.get_characteristics(html_code=html_code, RP_class=RP_class, product=product)

            find_items= "product-estimate"
            HB_class = HandlerBlock(str(RP_class.get_element("div", find_items, html_code=html_code)[0]))
            classes, others = HB_class.Handler()

            DH_class = DataHendler(classes_data=classes, others_data=others)
            product = DH_class.get_rate(product)
            product.get_data()

            products.append(product)
            ind += 1

        return products

    def get_characteristics(self, html_code: str, RP_class: Req_part, product: Product) -> Product:
            find_items = "p-view__specs"
            HB_class = HandlerBlock(str(RP_class.get_element("div", find_items, html_code=html_code)[0]))
            classes, others = HB_class.Handler()

            DH_class = DataHendler(classes_data=classes, others_data=others)
            product = DH_class.get_characteristics(product)


            return product

    def get_all_order(self, max_page: int = 3):
        "https://allo.ua/ru/catalogsearch/result/index/cat-48"
        links: list[str] = []
        for page_index in range(max_page):
            links.append(str(f'{self.url}/{config.REQ_PARAMS["page"]}{page_index + 1}/'))

        for link in links:
            elements = self.make_req(url=link, find_items=self.find_items, prompt=self.prompt)
            return self.hendler_blocks(blocks=elements)

    def add_filter(self, filter:str, value: any):
        self.filters[config.REQ_PARAMS[filter]] = value

    def apply_param(self):
        for key in list(self.filters.keys()):
            self.url = f'{self.url}/{key}{self.filters[key]}'


def test():
    url = "https://allo.ua/ru/catalogsearch/result/index/"
    find_items = "product-card"
    prompt = "монитор"
    HC_class = HandlerCode(url=url, prompt=prompt, find_items=find_items)
    # HC_class.add_filter(filter="price from", value=30000)
    # HC_class.add_filter(filter="price to", value=31000)

    HC_class.apply_param()
    products = HC_class.get_all_order(max_page=1)
    

    HO = HendlerOrder(products=products)
    HO.sort_orders()

    HO.get_colums()

    HO.get_all_characteristics()

    return HO.products
