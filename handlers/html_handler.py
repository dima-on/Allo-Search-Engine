import handlers.until as until

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
    