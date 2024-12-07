General Idea of Code:

Overview:
The code is written in Python and JavaScript and is designed to create a search engine called Allo Search. It allows the user to input a prompt and retrieves a list of products along with their characteristics and ratings from the Allo website. 

Features:
1. Input prompt - Users can enter search queries, and the engine will find matching products based on the provided input.
2. Data Extraction - The code extracts product details, such as name, price, image, and characteristics, from the Allo website.
3. Rating Information - The rating information for each product is also retrieved, helping users compare the products better.
4. Sorting - The search results can be sorted based on ratings to help users find the best options.
5. Dynamic Table Generation - The frontend dynamically updates the table displaying the search results, without requiring a page reload.

Structure:
The code is split into different files for better organization and clearer separation of concerns.

1. C:/Users/sinic/Python_Project/Allo_Search/config.py - Contains configuration settings like search parameters.
2. C:/Users/sinic/Python_Project/Allo_Search/handlers/handler_data.py - Contains classes to handle product data.
3. C:/Users/sinic/Python_Project/Allo_Search/handlers/handler_order.py - Contains sorting and arrangement functions for the search results.
4. C:/Users/sinic/Python_Project/Allo_Search/handlers/html_handler.py - Contains HTML parsing and extraction functions.
5. C:/Users/sinic/Python_Project/Allo_Search/handlers/until.py - Helper functions/module for HTML interactions.
6. C:/Users/sinic/Python_Project/Allo_Search/main.py - Main module linking the backend Python code with frontend JavaScript.
7. C:/Users/sinic/Python_Project/Allo_Search/templates/index.html - Frontend HTML template.
8. C:/Users/sinic/Python_Project/Allo_Search/visual.py - Backend Flask server setup.

Usage:
1. Run the Python backend Flask server using the visual.py script.
2. Open the index.html file in a web browser.
3. Enter a search query in the provided field and click the "Get orders" button.
4. The dynamic table will update to display the extracted product data sorted by rating.
# config.py

## Usage

The `config.py` file contains a dictionary object `REQ_PARAMS` with key-value pairs, where the keys are parameter names and the values are their corresponding search parameter templates. This file is used to handle the configuration of search parameters which can be utilized in different parts of an application.

## Methods

This file only contains a dictionary named `REQ_PARAMS`, with the following key-value pairs:

* `"price from"`: `"price_from-"`
* `"price to"`: `"price_to-"`
* `"proizvoditel"`: `"proizvoditel-"`
* `"page"`: `"p-"`

Here's a brief description about each key-value pair:

* **"price from"** - `"price_from-"`: This key-value pair specifies the configuration for the search parameter related to the minimum price value. The `"-"` is used to indicate that the user should provide their value without the '-' symbol.

* **"price to"** - `"price_to-"`: This key-value pair specifies the configuration for the search parameter related to the maximum price value. The `"-"` is used to indicate that the user should provide their value without the '-' symbol.

* **"proizvoditel"** - `"proizvoditel-"`: This key-value pair defines the search parameter configuration for selecting the manufacturer. The `"-"` is used to indicate that the user should provide their value without the '-' symbol.

* **"page"** - `"p-"`: This key-value pair indicates the search parameter configuration for selecting the page number of the search results. The `"-"` is used to indicate that the user should provide their value without the '-' symbol.

With these configurations set, users can easily utilize these search parameters in a unified and consistent manner in their code. To access any of these parameters, you only need to import the `config.py` file and reference the `REQ_PARAMS` variable, like so:

```python
import config

# Accessing a parameter (for example, "price from")
price_from_param = config.REQ_PARAMS["price from"]
```

By utilizing this file, developers can ensure consistency and ease of use when implementing search parameters in their application.
# Data Handler - A Part of Allo_Search Project

This documentation describes the usage and methods of the `handler_data.py` file from the Allo_Search project.

## Classes and Methods

### `Product`

Representing an Allo product with base data, characteristics, and ratings.

```python
def __init__(self) -> None:
    # Initializes a new instance of the Product class
    self.rating = {"general": 0}
```

This method initializes a new `Product` instance with a default `rating` value set to `{"general": 0}`.

```python
def set_base_data(self, **kwargs):
    # Sets the base data for a product
    self.name = kwargs.get("name")
    self.link = kwargs.get("link")
    self.price = kwargs.get("price")
    self.image = kwargs.get("image")
```

This method sets the base data for a product, including name, link, price, and image, using keyword arguments.

```python
def set_characteristics(self, characteristics: dict):
    # Sets characteristics for a product
    self.characteristics = characteristics
```

This method sets the characteristics dictionary for a product.

```python
def set_rating(self, rating: dict[str, float]):
    # Sets the rating for a product
    if rating != None:
        self.rating = rating
```

This method sets the rating dictionary for a product if the provided rating is not `None`.

```python
def get_data(self):
    # Prints the product's data
    print(f'Name: {self.name}')
    print(f'Link: {self.link}')
    print(f'Price: {self.price}')
    try:
        print(f'{self.rating["general"]}')
    except:
        pass
```

This method prints the product's base data and rating.

```python
def set_all_characteristics_params(self, all_characteristics: dict):
    # Sets all characteristics parameters for a product
    new = {}
    for key in list(all_characteristics.keys()):
        new[key] = self.characteristics.get(key)

    self.all_characteristics = new
```

This method sets all characteristics parameters for a product, replacing the current values.

```python
def set_all_rate(self, all_rate: dict):
    # Sets all-rating for a product
    new = {}
    for key in list(all_rate.keys()):
        new[key] = self.rating.get(key)

    print(new)
    self.all_rate = new
```

This method sets all-rating values for a product, replacing the current values.

```python
def to_dict(self):
    # Converts the product's data to dictionary
    info_dict = {
        "name": self.name,
        "link": self.link,
        "price": self.price,
        "image": self.image,
        "characteristics": self.characteristics,
        "rating": self.rating,
        "all_characteristics": self.all_characteristics,
        "all_rate": self.all_rate
    }

    return info_dict
```

This method converts the product's data into a dictionary containing the product's information.

### `DataHandler`

Represents a data handler object that fetches product's base data, characteristics, and rating.

```python
def __init__(self, classes_data: dict, others_data: dict) -> None:
    # Initializes a new instance of the DataHandler class
    self.classes_data = classes_data
    self.others_data = others_data
```

This method initializes a new `DataHandler` instance with provided `classes_data` and `others_data` dictionaries.

```python
def get_base_data(self) -> Product:
    # Retrieves product's base data based on the given class dictionary
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
```

This method fetches the product's base data using the provided class dictionary and returns it.

```python
def get_characteristics(self, product: Product) -> Product:
    # Retrieves product's characteristics based on the given other data dictionary
    params = self.others_data["/[document]/p-view__specs/p-specs/p-specs__groups-list/p-specs__group/tbody/tr/p-specs__cell"]
    param_dict = {}
    parser = until.Parser()
    for index in range(len(params) - 1):
        if index % 2 == 0:
            param_dict[parser.get_normal_text(params[index].text)] = params[index + 1].text

    product.set_characteristics(characteristics=param_dict)
    return product
```

This method fetches the product's characteristics using the provided other data dictionary and updates the `product` instance.

```python
def get_rate(self, product: Product) -> Product:
    # Retrieves product's rating from the given class dictionary.
    try:
        general_rating = self.classes_data["/[document]/product-estimate/average-estimate/average-estimate__rating"][0].text
        general_rating = general_rating[11:]

        more_ratings = self.classes_data.get("/[document]/product-estimate/product-estimate__center/detail-estimate/detail-estimate-list/detail-estimate-list__item")
        if more_ratings:
            all_rating = {
                "general": float(general_rating)
            }
            for el in more_ratings:
                HB_class = HandlerBlock(str(el))
                classes, others = HB_class.Handler()
                name_rate = classes["/[document]/detail-estimate-list__item/detail-estimate-list__label"][0].text
                value_rate = classes["/[document]/detail-estimate-list__item/detail-estimate-list__value/detail-estimate-list__rating"][0].text

                all_rating[name_rate] = float(value_rate)
        else:
            all_rating = {}

        product.set_rating(all_rating)
        return product
    except:
        product.set_rating(rating=None)
        return product
```

This method retrieves the product's rating using the provided class dictionary and updates the `product` instance.
# handler_order.py

## Overview

The `handler_order.py` file contains a class named `HandlerOrder` that manages sorting and processing products based on their given characteristics and ratings.

## Usage

```python
from handler_order import HandlerOrder

products = [Product characteristics and rating, ...]
handler = HandlerOrder(products)

# Sort products based on their ratings
handler.sort_orders()

# Get columns for characteristics
handler.get_colums()

# Set all products characteristics parameters
handler.get_all_characteristics()

# Get columns for ratings
handler.get_colums_rate()

# Set all products rating parameters
handler.get_all_rate()
```

### Methods

* `HandlerOrder__init__(self, products) -> None`
  - Takes in a list of products containing their characteristics and ratings.
  - Initializes the `HandlerOrder` object.

* `sort_orders(self) -> None`
  - Sorts the list of products based on their general rating score in ascending order.

* `get_colums(self) -> None`
  - Creates a dictionary called `colums` that will hold the unique characteristics of the products.

* `get_all_characteristics(self) -> None`
  - Sets all product's characteristics parameters to the columns of characteristics created in the `get_colums` method.

* `get_colums_rate(self) -> None`
  - Creates a dictionary called `colums_rate` that will hold the unique ratings of the products.

* `get_all_rate(self) -> None`
  - Sets all product's ratings params to the columns of ratings created in the `get_colums_rate` method.

This documentation is an addition to the full documentation of the module. For further information, please refer to the full documentation.
# HTML Handler Documentation

This markdown file provides a documentation for the `html_handler.py` file. Here, the focus is on explaining the usage and describing the methods within the file.

## Usage

To use the `html_handler.py` file, first ensure it is correctly imported into your Python project. This file can be used for extracting classes, elements, and without-class elements to form paths based on the HTML structure.

Here is an example of how to use the `HandlerBlock` class in your project:

```python
from html_handler import HandlerBlock

# Define a sample HTML block
sample_html = '''
<html>
  <head>
    <div>
      <p> paragraphs </p>
    </div>
  </head>
  <body>
    <table class="t1">
      <tr>
        <td class="a"> td1_a </td>
      </tr>
    </table>
    <div>
      <div class="b">
        <p> paragraphs_inside_b </p>
      </div>
    </div>
  </body>
</html>
'''

# Create an instance of HandlerBlock, passing the HTML block
handler_block = HandlerBlock(sample_html)

# Call the Handler method to get the data
class_data, element_data = handler_block.Handler()

# Process the data
print("Class data:", class_data)
print("Element without class data:", element_data)
```

## Methods

### HandlerBlock

The `HandlerBlock` class contains 3 methods: `__init__`, `Handler`, and 2 helper methods `handler_classes`, and `handler_element_without_classes`.

#### Constructor: `__init__(self, block_code: str)`

- This constructor takes the HTML block as input and initializes the `block_code` attribute.

#### Method: `Handler(self) -> tuple[dict, dict]`

- Returns a tuple containing two dictionaries: `class_data` and `element_data`.
- This method calls `handler_classes` and `handler_element_without_classes` internal methods to process the HTML block and extract classes, elements, and without-class elements from the structure.

#### Method: `handler_classes(self) -> dict`

- Searches for classes within the HTML block.
- It returns a dictionary representing the classes and their associated paths.

#### Method: `handler_element_without_classes(self) -> dict`

- Searches for elements (with and without classes) within the HTML block.
- It returns a dictionary representing the elements and their associated paths.

#### Method: `get_item_path(self, finder: until.Finder, item, element_type:str) -> str`

- Constructs the correct path for an item with respect to its parent elements and the given element type (class or none).
- This method is a common helper to both `handler_classes` and `handler_element_without_classes`.
# until.py

This module provides a parser and a finder class, which can be used to extract information from HTML documents.

## Parser Class

The `Parser` class is used for parsing strings and returning the necessary information.

### Constructor

```python
__init__(self)
```
The constructor initializes a new instance of the `Parser` class. It does not require any arguments.

### Methods

```python
from_str_to_int(self, start: str, flag: tuple) -> float
```
This method converts a string input `start` to an integer value while excluding the characters in the `flag` tuple.

```python
get_normal_text(self, text: str) -> str
```
The method `get_normal_text` extracts the desired text from the input string `text`, taking into account specific conditions, and returns the extracted text. In this case, it removes the first 17 characters and the substring after the newline `\n`.

## Finder Class

The `Finder` class is used to extract and find elements from HTML documents.

### Constructor

```python
__init__(self, html_code: str)
```
The constructor initializes a new instance of the `Finder` class and takes an HTML document as input in the form of a string.

### Methods

```python
find_classes(self, type_item, class_name: str) -> list
```
The `find_classes` method returns a list of elements from the given HTML document's `type_item` and with the specified class `class_name`.

```python
find_without_class(self) -> list
```
The method `find_without_class` returns a list of elements from the given HTML document's without the specification of a class.
,,
# Allo Search Documentation

## Usage

The script provided here is meant to interact with the Allo.ua search functionality and retrieve detailed information about the products obtained for a certain search query. This write-up explains how to use the script in a Google-style documentation approach.

### Importing Required Libraries

```python
import requests
import handlers.until as until
from bs4 import BautifuelSoup
import sys
from handlers.handler_data import Product, DataHendler
import config
from handlers.html_handler import HandlerBlock
from handlers.handler_order import HendlerOrder
sys.stdout.reconfigure(encoding='utf-8')
```

### Main Classes

#### Req_part

- **Description**: Handles search requests, fetching HTML content and extracting specific elements from the content using the provided search query prompt.
- **Methods**:
	- `__init__(self, url: str)`: Initializes the Req_part object with the search URL.
	- `get_html_code(self, prompt: str) -> str`: Returns the fetched HTML code for the given search prompt.
	- `get_element(self, element_type: str, element_class: str, html_code: str) -> list`: Finds and extracts elements with specified type and class from the provided HTML code.

#### HandlerCode

- **Description**: Builds search requests, applies filters, and handles blocks to obtain detailed product information and orders from search results.
- **Methods**:
	- `__init_(sel_f, url, find_items: str, prompt: str)`: Initializes the HandlerCode object with the search URL, target search elements, and the search prompt.
	- `make_req(self, url: str, find_items: str, prompt: str) -> list`: Constructs and sends a search request and retrieves the result elements.
	- `hendler_blocks(self, blocks: list)`: Processes multiple blocks of search results for obtaining detailed product data.
	- `get_characteristics(self, html_code: str, RP_class: Req_part, product: Product) -> Product`: Extracts product specifications from the raw search result.
	- `get_all_order(self, max_page: int = 3)`: Retrieves all search order pages with the specified maximum number of pages.
	- `add_filter(self, filter:str, value: any)`: Adds a filter to the search query by specifying key-value pair from the provided Config parameters.
	- `apply_param(self)`: Applies filters and updates the URL accordingly.

#### Get_orders

- **Description**: Retrieves products, orders them, and prepares them for further custom processing based on the search prompt provided.
- **Methods**:
	- `Get_orders(prompt: str)`: Main function to retrieve relevant information from the search prompt.

### How to Use

To use this script, follow the steps provided in the example:

```python
def Get_orders(prompt: str):
    url = "https://allo.ua/ru/catalogsearch/result/index"
    prompt = prompt

    find_items = "product-card"
    HC_class = HandlerCode(url=url, prompt=prompt, find_items=find_items)
    
    # Apply filters (optional)
    # HC_class.add_filter(filter="price from", value=100)
    # HC_class.add_filter(filter="price to", value=1800)

    HC_class.apply_param()

    products = HC_class.get_all_order(max_page=1)

    HO = HendlerOrder(products=products)
    HO.sort_orders()

    HO.get_colums()
    HO.get_all_characteristics()
    HO.get_colums_rate()
    HO.get_all_rate()

    return HO.products
```

1. Import required libraries and classes.
2. Initialize the `HandlerCode` object with the appropriate configuration.
3. Optional: Apply filters by calling the `add_filter` method.
4. Call `apply_param` to apply filters to the URL.
5. Call the `get_all_order` method for retrieving the results.
6. Create an instance of `HendlerOrder` and process the product list as needed (sorting, retrieving characteristics, and fetching rate values).

Extend the functionality and steps if needed based on the specific application requirements.
# index.html

This file represents the HTML template for a web application that displays product orders based on a user inputted prompt. Here is a detailed explanation of all the methods present in this file:

## add_colums(colums)
- Description: This function creates additional table columns in the specified table element `.products .products_table`.
- Parameters: `colums` (an object containing keys and values to be added as table column headers).
- Usage: `add_colums(data["orders"][0]["all_characteristics"])` creates additional columns with characteristic keys as headers.

## add_product(product)
- Description: This function populates the created columns with data from the `product` object.
- Parameters: `product` (an object containing product data).
- Usage: `add_product(data["orders"][i])` populates each product data in the result array `data["orders"]`.

## clear_data()
- Description: This function removes previously added data (characteristics and rates) from the table element.
- Usage: `clear_data()` clears the table data before displaying new results.

## add_rate_colums(colums)
- Description: This function creates additional table columns with rate values.
- Parameters: `colums` (an object containing keys and rate values for the new columns).
- Usage: `add_rate_colums(data["orders"][0]["all_rate"])` creates additional columns with rate keys as headers.

## get_orders(prompt)
- Description: Sends a request to a specified URL path with provided prompt, retrieves the response and processes it.
- Parameters: `prompt` (a user inputted value).
- Usage: `get_orders(prompt)` retrieves product data based on user prompt and processes the response.

## make_req()
- Description: Clears existing data, gets the user prompt value, and calls `get_orders()` method to retrieve and display product orders.
- Usage: `make_req()` initiates the process of displaying product orders based on the user input prompt. This includes clearing existing data, getting the prompt input, and fetching orders data.

Furthermore, CSS styles are provided for various parts of the application, including header, input field, buttons, table visibility, and more. These styles help in creating a better user interface.

Remember to fill up remaining gaps and expand on this documentation while adhering to Google Styles. Non-essential sections, such as "Additional wishes", are not included in this sample documentation.
# visual.py Documentation

This documentation outlines the usage and methods of the `visual.py` file.

## Usage

To use this file, you need to have a basic understanding of Python and its packages, such as Flask.

1. Ensure that `flask` is installed on your system, if not, you can install it by running the following command in your terminal:

```bash
pip install Flask
```

2. Open the `visual.py` file in your preferred text editor or integrated development environment (IDE).

3. You can run the Flask application using the following command in your terminal:

```bash
python visual.py
```

4. Access the application locally at `http://127.0.0.1:8000/` (assuming the default port number `8000`).

## Methods:

- `Visual`: A class for initializing the Flask application and starting the server on a desired port.
- `__init__(self, port: int = 800) -> None`: Initializes the Visual class with a specified port number. The port number is set to `800` by default.
- `start_app(self)`: Starts the Flask application using `app.run('0.0.0.0', port=self.port)`.
- `render_template()`: Renders the `index.html` template at the root URL.


`/get_orders` EndPoint:

- Method: GET
- Description: Retrieves the products based on the given prompt.
- Parameters: "prompt" (a query parameter)
- Returns: A JSON object containing a message and a list of products as dictionaries.
- Note: The `Get_orders` method from the `main` module is called and the prompt parameter is passed to it.

## Full Documentation

For full documentation, please refer to the main project's documentation or contact the project maintainer.
