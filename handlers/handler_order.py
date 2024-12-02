class HendlerOrder:
    def __init__(self, products) -> None:
        self.products = products

    def sort_orders(self):
        sort_products = self.products

        for index in range(len(sort_products)):
            for index_sorts in range(len(sort_products) - 1):
                try:
                    if sort_products[index_sorts].rating["general"] < sort_products[index_sorts + 1].rating["general"]:
                        sort_products[index_sorts], sort_products[index_sorts + 1] = sort_products[index_sorts + 1], sort_products[index_sorts]
                except:
                    pass

        self.products = sort_products


    
    def get_colums(self):
        colums = {}
        
        for product in self.products:
            for key in list(product.characteristics.keys()):
                colums[key] = "-"

        self.colums = colums

    def get_all_characteristics(self):
        for product_index in range(len(self.products)):
            self.products[product_index].set_all_characteristics_params(self.colums)


    def get_colums_rate(self):
        colums = {}
        for product in self.products:
            for key in list(product.rating.keys()):
                colums[key] = "-"
                

        self.colums_rate = colums

    def get_all_rate(self):
        for product_index in range(len(self.products)):
            self.products[product_index].set_all_rate(self.colums_rate)
    

        


        

        



