from bs4 import BeautifulSoup
class Parser:
    def __init__(self) -> None:
        pass

    def from_str_to_int(self, start: str, flag: tuple) ->float:
        end_str: str = ""
        for el in start:
            if el in flag:
                continue
            else:
                end_str += el
        
        return float(end_str)
    
    def get_normal_text(self, text: str) -> str:
        text = text[17:]
        end_index = text.find('\n')
        text = text[:end_index]

        return text


class Finder:
    def __init__(self, html_code: str) -> None:
        self.html_code = BeautifulSoup(html_code, 'html.parser')

    def find_classes(self, type_item, class_name) -> list:
        if class_name:
            return self.html_code.find_all(type_item, class_=class_name)
        else:
            return self.html_code.find_all(class_=True)
    
    def find_without_class(self) ->list:
        return self.html_code.find_all()

    


        