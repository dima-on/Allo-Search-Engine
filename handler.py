import until
import sys
sys.stdout.reconfigure(encoding='utf-8')


class Product:
    def __init__(self) -> None:
        pass

    def set_base_data(self, **kwargs):
        self.name = kwargs.get("name")
        self.link = kwargs.get("link")
        self.price = kwargs.get("price")
        self.image = kwargs.get("image")

    def set_characteristics(self, characteristics: dict):
        self.characteristics = characteristics

    def get_data(self):
        print(f'Name: {self.name}')
        print(f'Link: {self.link}')
        print(f'Price: {self.price}')


class DataHendler:
    def __init__(self, classes_data:dict, others_data:dict) -> None:
        self.classes_data = classes_data
        self.others_data = others_data

    def get_base_data(self) -> Product:
        header = self.classes_data["/[document]/product-card/product-card__content/product-card__title"]
        name = header[0].text
        link = header[0]["href"]

        parser = until.Parser()
        price = self.classes_data["/[document]/product-card/product-card__content/product-card__buy-box/v-pb/v-pb__cur/sum"][0].text
        price = parser.from_str_to_int(price, flag=" ")
        
        image = self.classes_data["/[document]/product-card/product-card__pictures/product-card__img/image-carousel/image-carousel__container/image-carousel__slides/is-active/gallery__img"][0]
        image = image.get("src")

        product = Product()
        product.set_base_data(name=name, link=link, price=price, image=image)

        return product


    def get_characteristics(self, product: Product) -> Product:
        params = self.others_data["/[document]/p-view__specs/p-specs/p-specs__groups-list/p-specs__group/tbody/tr/p-specs__cell"]
        param_dict = {}
        parser = until.Parser()
        for index in range(len(params) - 1):
            if index % 2 == 0:
                param_dict[parser.get_normal_text(params[index].text)] = params[index + 1].text

        product.set_characteristics(characteristics=param_dict)

        return product



