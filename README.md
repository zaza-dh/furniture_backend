# Some basic doc for setting up the API:
Setting up env (tested with python3.6)
________________________________________________________________________________

To create a virtual environment: `make venv`

To activate the virtual environment: `source venv36/bin/activate`

To install the package locally: `make install`

To run `make run`

To test the API: 

1- Upload inventory file: `curl -X POST http://localhost:8000/uploadfile/inventory -F file=@inventory.json`

2- Upload products file: `curl -X POST http://localhost:8000/uploadfile/products -F file=@products.json`

3- Get list of available products: `curl -X GET http://localhost:8000/available_products`

4- Sell product 1 (available): `curl -X PUT http://localhost:8000/sell_product/1`

5- Sell product 2 (Available): `curl -X PUT http://localhost:8000/sell_product/2`

6- Sell product 1 again (Out of stockl): `curl -X PUT http://localhost:8000/sell_product/1`

8- Sell product 3 (Does not exist): `curl -X PUT http://localhost:8000/sell_product/3`