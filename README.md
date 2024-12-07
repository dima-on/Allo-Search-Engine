# Allo Search Engine Overview

The Allo search engine is a tool designed to search and display information about products from the Allo.ua website. It uses Python to scrape data from various pages and retrieve relevant product details such as name, price, image, ratings, and other characteristics. The primary goal of this code is to collect and present a comprehensive list of products that meet certain search parameters.

# Features

- A simple and user-friendly web interface that allows users to quickly enter a search prompt and receive results.
- Extraction of product details, including name, price, image, ratings, and characteristics.
- Sorting and categorizing of product information for enhanced search results.
- Seamless integration with Allo.ua website, scraping relevant data accurately and efficiently.
- Customizable search parameters based on filters such as price range, brand, and page number.

# Structure

The codebase consists of multiple components with well-defined responsibilities:

- `Req_part`: Handles HTTP requests and obtains HTML responses from the Allo.ua website.
- `HandlerCode`: Manages the extraction and processing of relevant data from HTML responses.
- `main`: Main script where the functions `GetOrders()`, `ReqPart`, and `HandlerCode` are initiated to form the final response that is returned to the user.
- `DataHandler`: Processes data and extracts essential information such as name, price, ratings, and characteristics from the retrieved products.
- `HendlerOrder`: Sorts and organizes the assembled product data, displaying the final results in an ordered fashion.
- `HTMLHandler`: Parses and extracts data from HTML content efficiently.
- `Until`: Provides helpful classes for parsing and finding elements within the HTML code.
- `Visual`: Initializes the web server using the Flask framework, allowing users to interact with the search engine through a simple web interface.

# Usage

To use the Allo search engine, follow these steps:

1. Install the required dependencies:
   - Python 3.6+ (to run the code, install Python through official Python website)
   - Flask (visit "https://flask.palletsprojects.com" to install Flask)
   - BeautifulSoup4 and requests (to scrape data)


2. Run the script from the terminal or command prompt by executing the python command followed by the path to the `visual.py` file:

```python
python visual.py
```

3. Open a web browser and navigate to the created server address (default port 800) to reach the Allo search engine's web interface. Type the desired search prompt and click on the "Get orders" button to retrieve and display the results.

Note: Since the code interacts with the Allo.ua website, ensure that the website's terms and conditions and local legal restrictions regarding web scraping are taken into account.
# config.py

This file contains a Python dictionary called `REQ_PARAMS`, which holds parameter names and their respective query string placeholders for building API requests.

## REQ_PARAMS

A dictionary that maps parameter names to their corresponding query string placeholders.

- `"price from"`: A string representing the starting price of an item. The placeholder for the API query is `"price_from-"`.
- `"price to"`: A string representing the ending price of an item. The placeholder for the API query is `"price_to-"`.
- `"proizvoditel"`: A string representing the manufacturer of an item. The placeholder for the API query is `"proizvoditel-"`.
- `"page"`: A string representing the page number for pagination. The placeholder for the API query is `"p-"`.

### Example

To use this file, first import it into your code:

```python
from config import REQ_PARAMS
```

You can then use the `REQ_PARAMS` dictionary to construct API requests by replacing the question marks `?` with the necessary query parameter names, and inserting the corresponding placeholders for dynamic values.

For example, to build a URL for an API request that includes starting price, ending price, manufacturer, and page number, you would do the following:

```python
base_url = "http://example.com/api/items?"
url_params = "?".join([
    f"{param}={REQ_PARAMS[param]}{value}"
    for param, value in [
        ("price_from", "100"),
        ("price_to", "500"),
        ("proizvoditel", "Brand X"),
        ("p", "2"),
    ]
])

full_api_url = base_url + url_params
```

This will generate a URL like the following:

```
http://example.com/api/items/?price_from=100&price_to=500&proizvoditel=Brand%20X&p=2
```

By using this file, your code will benefit from a clean and consistent way to handle API request parameters for an allo search application.
# Data Handler

This Markdown file provides documentation for the `DataHandler` class, focusing on its usage and methods. It is an additional documentation, not the full version.

## Introduction

The `DataHandler` class is a utility class designed to extract data from webpages. It utilizes the `Product` class to handle data storage. The class takes two dictionaries (`classes_data` and `others_data`) as initialization parameters and offers methods to get the base data, characteristics, and ratings of a product.

## Usage

To use the `DataHandler`, you must create an instance of it and supply the required dictionaries.

```python
from handler_data import DataHandler

classes_data = {
    "/[document]/product-card/product-card__content/product-card__title": [...],
    "/[document]/product-card/product-card__content/product-card__buy-box/v-pb/v-pb__cur/sum": [...],
    "/[document]/product-card/product-card__pictures/product-card__img/image-carousel/image-carousel__container/image-carousel__slides/is-active/gallery__img": [...],
    "/[document]/product-estimate/average-estimate/average-estimate__rating": [...],
    "/[document]/product-estimate/product-estimate__center/detail-estimate/detail-estimate-list/detail-estimate-list__item": [...]
}

others_data = {
    "/[document]/p-view__specs/p-specs/p-specs__groups-list/p-specs__group/tbody/tr/p-specs__cell": [...]
}

data_handler = DataHandler(classes_data, others_data)
```

Once you have created an instance of `DataHandler`, you can use its methods:

## Methods

### `get_base_data()` → `Product`

This method extracts the base data for a product from `classes_data` and returns a `Product` instance with the extracted data.

```python
product = data_handler.get_base_data()
```

### `get_characteristics(product: Product)` → `Product`

This method receives a `Product` instance with base data, accesses other data from `others_data`, and extracts the characteristics (parameters) of the product. It updates the instance's `characteristics` attribute and returns the modified `Product` instance.

```python
characteristics_product = data_handler.get_characteristics(product)
```

### `get_rate(product: Product)` → `Product`

This method receives a `Product` instance with base data and accesses classes_data. It retrieves the product's rating and updates the instance's `rating` attribute. A rated `Product` instance is returned.

```python
rated_product = data_handler.get_rate(product)
```

In case there is an error retrieving the rating, the method will set the rating to `None` and return the product object.
# handler_order.py

This module contains a class `HandlerOrder` to handle sorting and displaying characteristics and ratings of products.

## Class: `HandlerOrder`

This class accepts a list of `Product` objects and provides methods to sort the products by rating, and set up columns for displaying the characteristics and ratings.

### Methods

#### `__init__(self, products)`

Initializes the `HandlerOrder` object with a list of products.

#### `sort_orders(self)`

Sorts the product list in descending order based on the "general" rating.

#### `get_columns(self)`

Generates dictionaries of empty strings with keys as product characteristics and stores it in `colums`.

#### `get_all_characteristics(self)`

Sets all product characteristics to the columns defined in `get_columns(self)`.

#### `get_columns_rate(self)`

Generates dictionaries of empty strings with keys as product ratings and stores it in `colums_rate`.

#### `get_all_rate(self)`

Sets all product ratings to the columns defined in `get_columns_rate(self)`.
# Html Handler Module

This module, `html_handler.py`, provides a `HandlerBlock` class that parses an input string containing HTML code and extracts class names and elements without class names.

## Usage

To use the `HandlerBlock` class, perform the following steps:

1. Import the `HandlerBlock` class from the `html_handler.py` module:

```python
from html_handler import HandlerBlock
```

2. Create an instance of the `HandlerBlock` class by passing an HTML code string to its constructor:

```python
html_code = '''
  <div>
    <button class="btn btn-primary">Primary</button>
    <p class="text-danger">Danger</p>
  </div>
'''

handler = HandlerBlock(html_code)
```

3. Obtain the results containing the extracted class names and elements without class names using the `Handler()` method of the `HandlerBlock` instance:

```python
class_data, element_data = handler.Handler()
```

4. Use the returned `class_data` and `element_data` dictionaries to access the extracted information:

- `class_data`: a dictionary where keys represent the element path in the form of `/class1/class2/element` and values are lists of corresponding class names.
- `element_data`: a dictionary where keys represent the element path in the form of `//element` and values are lists of corresponding elements without class names.

## Methods

### `__init__(self, block_code: str) -> None`

- `block_code`: the HTML code string to be parsed.

Creates an instance of the `HandlerBlock` class that can be used to extract class names and elements without class names from the provided HTML code.

### `Handler(self) -> tuple[dict, dict]`

Returns a tuple containing two dictionaries: `class_data` and `element_data`.

- `class_data`: a dictionary representing the extracted class names along with their paths.
- `element_data`: a dictionary representing the extracted elements without class names along with their paths.

### `handler_classes(self) -> dict`

Parses the HTML code and finds all class names within the code, organizing them into a dictionary.

### `handler_element_without_classes(self) -> dict`

Parses the HTML code and finds all elements without class names within the code, organizing them into a dictionary.

### `get_item_path(self, finder: until.Finder, item, element_type:str) -> str`

Calculates the element's path based on its class or the type of element, with the input being a nested format.

- `finder`: a `until.Finder` instance used for HTML code parsing.
- `item`: the current element in the hierarchy.
- `element_type`: specifies whether the element's path is based on a class or not. (`None` means the element's path is not based on a class.)

Returns the element's path in the form of `/class1/class2/element`, where elements without class names are represented by `//element`.
# until.py

## Usage

This file contains two classes: `Parser` and `Finder`. These classes are used to parse and find HTML elements in a given HTML code.

## Parser

### from_str_to_int

```
from_str_to_int(self, start: str, flag: tuple) -> float
```

Converts a string to a float value, skipping elements from the given tuple `flag`.

### get_normal_text

```
get_normal_text(self, text: str) -> str
```

Removes the specified parts of a string to extract the desired text.

## Finder

### __init__

```
__init__(self, html_code: str) -> None
```

Initializes a new `Finder` object with the given HTML code.

### find_classes

```
find_classes(self, type_item, class_name) -> list
```

Finds HTML elements based on the provided `type_item` and optional `class_name`.

### find_without_class

```
find_without_class(self) -> list
```

Finds all HTML elements without specifying any class name.

## Example usage

```python
# Import the required classes.
from bs4 import BeautifulSoup
from until import Parser, Finder

# Initialize the Parser and Finder classes.
parser = Parser()
finder = Finder('<html_code_here>')

# Example of using the from_str_to_int method.
start_str = "1k2n4"
flag_tuple = ('k', 'n')
result = parser.from_str_to_int(start_str, flag_tuple)
print(result)  # Output: 142

# Example of using the get_normal_text method.
text = "normal text\nwith multiple\nlines"
normal_text = parser.get_normal_text(text)
print(normal_text)  # Output: normal text with multiple lines

# Example of using the find_classes method.
html_code = '<html_code_here>'
finder = Finder(html_code)
elements = finder.find_classes('div', 'specific_class')
for el in elements:
    print(el)

# Example of using the find_without_class method.
finder = Finder(html_code)
elements = finder.find_without_class()
for el in elements:
    print(el)
```

This example demonstrates how to use the methods in the `Parser` and `Finder` classes to find information from an HTML document. You can integrate these methods into your own code as needed.
# main.py Documentation

This documentation describes the usage of `main.py` which interacts with the Allo.ua search functionality to fetch and process product information using Python.

## Classes and Methods Overview

* `Req_part`: A class responsible for making request to the Allo.ua search.
  - `get_html_code(self, prompt: str) -> str`: Fetches the HTML code for the given search prompt.
  - `get_element(self, element_type: str, element_class: str, html_code: str) -> list`: Finds element by type and class within HTML code.
* `HandlerCode`: A class for handling code blocks and extracting product data.
  - `make_req(self, url: str, find_items: str, prompt: str) -> list`: Makes a request to the given URL and returns a list of elements.
  - `hendler_blocks(self, blocks: list)`: Processes the blocks and extracts product data, including characteristics and rates.
  - `get_characteristics(self, html_code: str, RP_class: Req_part, product: Product) -> Product`: Processes the product's characteristics.
  - `get_all_order(self, max_page: int = 3)`: Fetches all orders up to the specified number of pages.
  - `add_filter(self, filter: str, value: any)`: Adds filter parameters to the URL.
  - `apply_param(self)`: Applies the filter parameters to the URL.
* `Get_orders`: A function that retrieves, processes, and returns the Allo.ua search results based on given prompt.
  - `url`: The base URL for the Allo.ua search functionality.
  - `prompt`: The search prompt for the desired products.
  - `find_items`: A string denoting the class name for the items to find on the page.
  - `HC_class`: HandlerCode class instance for handling code blocks and extracting product data.

## Usage

To use the `main.py` module, import the required class and function, and call the `Get_orders()` function with the desired prompt. Here's an example:

```python
from main import Get_orders

prompt = "laptop"
products = Get_orders(prompt)

for product in products:
    print(product)
```

This will fetch Allo.ua search results for the "laptop" prompt and print the associated product information.

You may also modify the default behavior by overriding the parameters such as `find_items` or by adding custom filters through the `add_filter()` and `apply_param()` methods of the `HandlerCode` class. These custom filters can include parameters like price range, delivery options, or specific categories.

Note: Ensure that the necessary dependencies are installed (`requests`, `beautifulsoup`, `sys`, `config`, `handlers` package) before running this code.
# Allo_Search/templates/index.html

This file is responsible for displaying the user interface and handling user interactions for the Allo_Search application. It utilizes JavaScript, HTML, and CSS to render the product information based on the user's input prompt.

## Usage

Before diving into the methods, make sure the following preconditions are met:

1. Load the `index.html` file in a web browser or any HTML rendering environment.
2. Ensure the `url` variable is set to the correct base URL in the `<script>` section at the beginning of the file.

### Methods

- `add_colums(colums)`: This method creates and appends new table columns (`<tr>` elements) with the specified headers from the `colums` object. It uses the keys of the `colums` object as the column headers.
- `add_product(product)`: This method iterates over each row in the table, creates `<th>` elements, and populates them with the respective product information. It takes a `product` object as input.
- `clear_data()`: This method clears the existing data in the table, removing specific elements with the classes `.characteristics:not(root)` and `.rate:not(root)`.
- `add_rate_colums(colums)`: This method creates and appends new table columns (`<tr>` elements) for rating information. It iterates over the keys of the `colums` object and uses them as column headers.
- `get_orders(prompt)`: This method sends a GET request to the server to fetch the order data based on the user's input `prompt`. Once the data is retrieved, it calls the `add_rate_colums()`, `add_colums()`, and `add_product()` methods to populate the table.
- `make_req()`: This method is triggered when the user clicks the "Get orders" button. It clears existing data in the table and retrieves new order information by calling the `get_orders()` method with the user's input prompt.

## Additional Remarks

Note that the provided documentation is only a reference for the highlighted methods and usage instructions. For complete documentation, please refer to additional sources or the original source code.
# visual.py

This file provides a Flask web application that allows users to interact with the `main` module and receive JSON data with the list of orders corresponding to a given prompt.

## Usage

1. Ensure that the `main` module is in the same directory or correctly imported at the beginning of this file.
2. Run the `visual.py` script.
3. The web server will start on `http://0.0.0.0:8000`.
4. Access the web page via the URL and use the endpoint `/get_orders` to retrieve the list of orders for a specific prompt.

### Method Descriptions

1. **`Visual(port: int = 800)`**: This class constructor initializes the `Visual` class and assigns a specified `port` number, with a default value of `800`.

2. **`start_app()`**: This method initiates the Flask web application.

3. **`render_template()`**: This route renders the `index.html` template, which serves as the main page of the web application.

4. **`get_orders()`**: This route receives a GET request with a query parameter named `prompt`. It calls the `Get_orders` function from the `main` module and converts the products in the returned list to a dictionary format, which is then sent as JSON data with the message "Получено значение!".

### Example Usage

Run `visual.py` and send a GET request to `http://0.0.0.0:8000/get_orders?prompt=<your_prompt>`. Replace `<your_prompt>` with the desired prompt. The function will return a JSON response with the list of orders for the given prompt.

**Note**: Make sure to adhere to the [Google Style](https://google.github.io/styleguide/pyguide.html) when using this file.

**Additional wishes**: None.

</markdown>
