
import json
from typing import List

from ikea_backend.database import SessionLocal, engine
from ikea_backend import model

# Dependency
def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


def from_byte_to_json(file):
    data = ''
    for line in file.readlines():
        data = data + str(line, 'utf-8')
    return json.loads(data)


def get_product_availability(product_id: int):
    product_components_amounts = get_product_components_and_amounts(product_id)
    required_articles_ids = list(product_components_amounts.keys())
    articles_in_stock = get_articles_amount_in_stock(required_articles_ids)
    product_availability = calculate_quantity_of_available_product(
        articles_in_stock, product_components_amounts)
    return product_availability


def get_all_products_availabilities():
    db = get_db()
    db_products = db.query(model.Products).all()
    products_available_quantities = []
    for product in db_products:
        product_available_quantitiy = {}
        product_available_quantitiy["name"] = product.name
        product_available_quantitiy["id"] = product.id
        product_available_quantitiy["availability"] = get_product_availability(
            product.id)
        products_available_quantities.append(product_available_quantitiy)
    db.close()
    return products_available_quantities


def product_components_are_available(product: model.Products, available_components: List):
    for article in product['contain_articles']:
        if int(article['art_id']) not in available_components:
            return False
    return True


def add_product_components_to_database(product_id: int, components: List):
    db = get_db()
    for article in components:
        db_article = model.ProductComponents(
            prod_id=product_id,
            art_id=article['art_id'],
            amount=article['amount_of']
        )

        db.add(db_article)
    db.commit()
    db.close()



def write_products_to_database(products: json):
    db = get_db()
    all_articles = db.query(model.Articles).all()
    articles_ids = [art.id for art in all_articles]

    for product in products:
        product_name = product["name"]
        db_product = model.Products(
            name=product_name,
            price=0.0
        )

        all_articles_available = product_components_are_available(
            product, articles_ids)

        if not all_articles_available:
            return {"error": f"Not all of the product '{product_name}' components are available."}

        db.add(db_product)
        db.commit()

        product_id = db.query(model.Products.id).filter(
            model.Products.name == product["name"])
        add_product_components_to_database(
            product_id, product['contain_articles'])
    db.close()



def write_inventory_to_database(inventory_items: json):
    db = get_db()
    for item in inventory_items:
        inventory_item = model.Articles(
            id=item['art_id'],
            name=item['name'],
            stock=item['stock']
        )
        db.add(inventory_item)
        db.commit()
    db.close()


def get_product_components_and_amounts(product_id: int):
    """
    Return a Dictionary mapping product components' IDs to their respective amounts
    """
    db = get_db()
    db_product_components = db.query(model.ProductComponents).filter(
        model.ProductComponents.prod_id == product_id).all()
    product_components_amounts = {
        p.art_id: p.amount for p in db_product_components}
    db.close()
    return product_components_amounts


def get_articles_amount_in_stock(article_ids: List):
    db = get_db()
    articles_in_stock = db.query(model.Articles).filter(
        model.Articles.id.in_(article_ids)).all()

    available_articles = {p.id: p.stock for p in articles_in_stock}
    db.close()
    return available_articles


def calculate_quantity_of_available_product(articles_in_stock: dict, product_components_amounts: dict):
    possible_product_per_article = []
    required_articles_ids = list(product_components_amounts.keys())
    for article_id in required_articles_ids:
        possible_product_per_article.append(
            int(articles_in_stock[article_id] / product_components_amounts[article_id]))
    if possible_product_per_article:
        return min(possible_product_per_article)
    return 0


def does_product_exist(prod_id: int):
    db = get_db()
    product = db.query(model.Products).filter(
        model.Products.id == prod_id).all()
    db.close()
    if product:
        return True
    return False


def get_product_componenet(prod_id: int):
    db = get_db()
    product_compenent = db.query(model.ProductComponents).filter(
        model.ProductComponents.prod_id == prod_id).all()
    db.close()
    return product_compenent


def update_inventory(product_compenent: List):
    db = get_db()
    for component in product_compenent:
        article = db.query(model.Articles).filter(
            model.Articles.id == component.art_id).one()
        article.stock = article.stock - component.amount
        db.commit()
    db.close()
