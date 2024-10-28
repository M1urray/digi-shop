import random
from faker import Faker
from app.extensions import db
from app.model import Category, SubCategory, Brand, Product, Customer, Address, Order, OrderItem, Tag, Specification
from app import create_app  # Assuming you have a create_app function to initialize your app

# Initialize Faker
fake = Faker()

# Initialize Flask app and application context
app = create_app()
app.app_context().push()

# Function to generate test data
def generate_test_data():
    try:
        # Generate categories and subcategories
        categories = []
        for _ in range(5):  # 5 categories
            category = Category(name=fake.word().capitalize())
            db.session.add(category)
            categories.append(category)
        db.session.commit()

        subcategories = []
        for category in categories:
            for _ in range(3):  # 3 subcategories per category
                subcategory = SubCategory(name=fake.word().capitalize(), category_id=category.id)
                db.session.add(subcategory)
                subcategories.append(subcategory)
        db.session.commit()

        # Generate brands
        brands = []
        for _ in range(5):  # 5 brands
            brand = Brand(name=fake.company())
            db.session.add(brand)
            brands.append(brand)
        db.session.commit()

        # Generate tags
        tags = []
        for _ in range(10):  # 10 tags
            tag = Tag(name=fake.word().lower(), description=fake.sentence())
            db.session.add(tag)
            tags.append(tag)
        db.session.commit()

        # Generate products
        products = []
        for subcategory in subcategories:
            for _ in range(10):  # 10 products per subcategory
                product = Product(
                    name=fake.word().capitalize(),
                    price=round(random.uniform(10, 500), 2),
                    brand_id=random.choice(brands).id,
                    rating=random.randint(1, 5),
                    discount=f"{random.randint(5, 30)}%",
                    image=fake.image_url(),
                    is_hot_deal=random.choice([True, False]),
                    category_id=subcategory.category_id,
                    subcategory_id=subcategory.id
                )
                db.session.add(product)
                products.append(product)
        db.session.commit()

        # Assign tags to products
        for product in products:
            product_tags = random.sample(tags, k=random.randint(1, 3))  # Assign 1 to 3 random tags
            for tag in product_tags:
                product.tags.append(tag)
        db.session.commit()

        # Generate specifications for products
        for product in products:
            for _ in range(random.randint(1, 5)):  # 1 to 5 specifications per product
                specification = Specification(
                    specification_name=fake.word().capitalize(),
                    specification_value=fake.sentence(nb_words=3),
                    product_id=product.id
                )
                db.session.add(specification)
        db.session.commit()

        # Generate customers
        customers = []
        for _ in range(10):  # 10 customers
            customer = Customer(
                fname=fake.first_name(),
                lname=fake.last_name(),
                company_name=fake.company(),
                email=fake.email(),
                phone=fake.phone_number()
            )
            db.session.add(customer)
            customers.append(customer)
        db.session.commit()

        # Generate addresses
        addresses = []
        for customer in customers:
            for _ in range(2):  # 2 addresses per customer
                address = Address(
                    street=fake.street_address(),
                    town=fake.city(),
                    postal_code=fake.postcode(),
                    country=fake.country(),
                    customer_id=customer.id
                )
                db.session.add(address)
                addresses.append(address)
        db.session.commit()

        # Generate orders and order items
        for customer in customers:
            for _ in range(3):  # 3 orders per customer
                address = random.choice(addresses)
                order = Order(
                    customer_id=customer.id,
                    address_id=address.id,
                    notes=fake.sentence()
                )
                db.session.add(order)
                db.session.commit()  # Commit the order to generate an order ID

                # Generate order items for each order
                for _ in range(4):  # 4 items per order
                    product = random.choice(products)
                    order_item = OrderItem(
                        product_id=product.id,
                        order_id=order.id,
                        quantity=random.randint(1, 5)
                    )
                    db.session.add(order_item)
                db.session.commit()  # Commit order items for this order

    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        print(f"An error occurred: {e}")


with app.app_context():
    print("Generating test data...")
    generate_test_data()
    print("Test data generation complete!")
