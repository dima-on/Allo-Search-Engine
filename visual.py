from flask import Flask, render_template, jsonify, request
import main
app = Flask(__name__)

class Visual:
    def __init__(self, port: int = 800) -> None:
        self.port = port

    def start_app(self):
        app.run('0.0.0.0', port=self.port)

    @app.route('/')
    def render_tamplate():
        return render_template('index.html')
    
    @app.route('/get_orders', methods=['GET'])
    def get_orders():
        products = main.test()
        products_list = []
        for el in products:
            # print(el.all_characteristics)
            # print("________" * 100)
            products_list.append(el.to_dict())
        # for el in products_list:
        #     print(el["all_characteristics"])
        #     print("_" * 30)
        return jsonify({'message': 'Получено значение!', "test": products_list})


    

if __name__ == "__main__":
    visual_class = Visual()
    visual_class.start_app()