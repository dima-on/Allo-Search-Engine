import requests
import until
from bs4 import BeautifulSoup
import sys
import handler
import config
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

class HandlerBlock:
    def __init__(self, block_code: str) -> None:
        self.block_code = block_code

    def Handler(self) -> tuple[dict, dict]:
        class_data = self.handler_classes()
        element_data = self.handler_element_without_classes()

        return class_data, element_data
    def handler_classes(self) -> dict:
        finder = until.Finder(self.block_code)
        classes = finder.find_classes("", None)

        out_put: dict[str, list] = {}


        for item in classes:
            path = self.get_item_path(finder=finder, item=item, element_type="class")

            if out_put.get(path) != None:
                out_put[path].append(item)

            else:
                out_put[path] = [item]

        return out_put

    def handler_element_without_classes(self) -> dict:
        finder = until.Finder(self.block_code)
        elements = finder.find_without_class()
        out_put: dict[str, list] = {}


        for item in elements:
            path = self.get_item_path(finder=finder, item=item, element_type=None)

            if out_put.get(path) != None:
                out_put[path].append(item)
                

            else:
                out_put[path] = [item]

        return out_put


    def get_item_path(self, finder: until.Finder, item, element_type:str) -> str:
        ex = []
        if element_type == None:
            element_type = "class"
        while item != None:
            if element_type:
                name = item.get(element_type)
                if name == None:
                    name = [item.name]

            if name != None:
                ex.append(name[0])
            item = item.parent
        
        ex_str: str = ""
        ex.reverse()
        for el in ex:
            ex_str += f'/{el}'

        return ex_str
    
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

        for block in blocks:
            HB_class = HandlerBlock(str(block))
            classes, others = HB_class.Handler()

            DH_class = handler.DataHendler(classes_data=classes, others_data=others)

            product = DH_class.get_base_data()
 
            RP_class = Req_part(url=product.link)
            html_code = RP_class.get_html_code(None)

            find_items = "p-view__specs"
            HB_class = HandlerBlock(str(RP_class.get_element("div", find_items, html_code=html_code)[0]))
            classes, others = HB_class.Handler()

            DH_class = handler.DataHendler(classes_data=classes, others_data=others)
            product = DH_class.get_characteristics(product)

            product.get_data()
            products.append(product)

    def get_all_order(self, max_page: int = 3):
        "https://allo.ua/ru/catalogsearch/result/index/cat-48"
        links: list[str] = []
        for page_index in range(max_page):
            links.append(str(f'{self.url}/{config.REQ_PARAMS["page"]}{page_index + 1}/'))

        for link in links:
            elements = self.make_req(url=link, find_items=self.find_items, prompt=self.prompt)
            self.hendler_blocks(blocks=elements)

    def add_filter(self, filter:str, value: any):
        self.filters[config.REQ_PARAMS[filter]] = value

    def apply_param(self):
        for key in list(self.filters.keys()):
            self.url = f'{self.url}/{key}{self.filters[key]}'


class HendlerOrder:
    pass


if __name__ == "__main__":
    url = "https://allo.ua/ru/catalogsearch/result/index/cat-48/"
    find_items = "product-card"
    prompt = "телефон"
    HC_class = HandlerCode(url=url, prompt=prompt, find_items=find_items)
    HC_class.add_filter(filter="price from", value=30000)
    HC_class.add_filter(filter="price to", value=31000)

    HC_class.apply_param()
    HC_class.get_all_order(max_page=1)
