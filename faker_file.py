from faker import Faker
import random

fake = Faker()

#start = 7


#with open("fake_customers.sql", "w") as f:
#    for i in range(5):
#        current_id = start + i
#        customer_name = (fake.name())
#        number = (fake.numerify("55#-####"))
#        address = (fake.street_address())
#        f.write((f"INSERT INTO customers (customer_id, customer_name, tel_no, address) VALUES ({current_id}, '{customer_name}', '{number}', '{address}');\n"))

# Orders
start_order_id = 8

with open("fake_orders.sql", "w") as f:
    for i in range(15):
        order_id = start_order_id + i
        customer_id = random.randint(7, 11)
        order_date = fake.date_between(start_date="-30d", end_date="today")
        is_delivery = random.choice([True, False])
        f.write(f"INSERT INTO orders (order_id, customer_id, order_date, is_delivery) VALUES ({order_id}, {customer_id}, '{order_date}', {is_delivery});\n")