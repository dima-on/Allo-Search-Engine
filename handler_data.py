import until
import sys
from html_handler import HandlerBlock
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

    def set_rating(self, rating: dict[str, float]):
        self.rating = rating

    def get_data(self):
        print(f'Name: {self.name}')
        print(f'Link: {self.link}')
        print(f'Price: {self.price}')
        try:
            print(f'{self.rating["general"]}')
        except:
            pass
    
    def set_all_characteristics_params(self, all_characteristics: dict):
        new = {}
        for key in list(all_characteristics.keys()):
            new[key] = self.characteristics.get(key)

        self.all_characteristics = new

    def to_dict(self):
        info_dict = {
            "name": self.name,
            "link": self.link,
            "price": self.price,
            "image": self.image,
            "characteristics": self.characteristics,
            "rating": self.rating,
            "all_characteristics": self.all_characteristics

        }

        return info_dict

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
    
    def get_rate(self, product: Product) -> Product:
        try:
            general_rating = self.classes_data["/[document]/product-estimate/average-estimate/average-estimate__rating"][0].text
            general_rating = general_rating[11:]

            more_ratings = self.classes_data["/[document]/product-estimate/product-estimate__center/detail-estimate/detail-estimate-list/detail-estimate-list__item"]
            all_rating = {
                "general": float(general_rating)
            }
            for el in more_ratings:

                HB_class = HandlerBlock(str(el))
                classes, others = HB_class.Handler()
                name_rate = classes["/[document]/detail-estimate-list__item/detail-estimate-list__label"][0].text
                value_rate = classes["/[document]/detail-estimate-list__item/detail-estimate-list__value/detail-estimate-list__rating"][0].text

                all_rating[name_rate] = float(value_rate)

            product.set_rating(all_rating)

            return product
        except:
            product.set_rating(rating=None)
            return product
            






