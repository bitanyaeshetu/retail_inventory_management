import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

class Product:
    def __init__(self, db, name, category, price, stock_level):
        self.db = db
        self.name = name
        self.category = category
        self.price = price
        self.stock_level = stock_level

    def add_product(self):
        query = "INSERT INTO products (name, category, price, stock_level) VALUES (%s, %s, %s, %s)"
        self.db.cursor.execute(query, (self.name, self.category, self.price, self.stock_level))
        self.db.connection.commit()

    def update_stock(self, quantity):
        self.stock_level += quantity
        query = "UPDATE products SET stock_level = %s WHERE name = %s"
        self.db.cursor.execute(query, (self.stock_level, self.name))
        self.db.connection.commit()

class Sale:
    def __init__(self, db, product_id, quantity, discount=0):
        self.db = db
        self.product_id = product_id
        self.quantity = quantity
        self.discount = discount
        self.sale_date = datetime.now()
        self.revenue = 0

    def record_sale(self):
        self.db.cursor.execute("SELECT price FROM products WHERE id = %s", (self.product_id,))
        price = self.db.cursor.fetchone()[0]
        total_price = price * self.quantity
        discount_amount = (total_price * self.discount) / 100
        self.revenue = total_price - discount_amount
        
        query = "INSERT INTO sales (product_id, quantity, sale_date, revenue) VALUES (%s, %s, %s, %s)"
        self.db.cursor.execute(query, (self.product_id, self.quantity, self.sale_date, self.revenue))
        self.db.connection.commit()

def forecast_stock_demand(db, product_id, period=3):
    """Forecast future stock demand based on moving averages."""
    db.cursor.execute("""
        SELECT quantity FROM sales 
        WHERE product_id = %s 
        ORDER BY sale_date DESC LIMIT %s
    """, (product_id, period))
    
    sales_data = db.cursor.fetchall()
    if len(sales_data) < period:
        return "Not enough data to forecast."
    
    moving_average = sum(sale[0] for sale in sales_data) / period
    return moving_average

def check_low_stock_and_order(db, threshold=5):
    """Check stock levels and generate orders for suppliers if below threshold."""
    db.cursor.execute("SELECT id, name, stock_level FROM products WHERE stock_level < %s", (threshold,))
    low_stock_products = db.cursor.fetchall()
    
    for product in low_stock_products:
        product_id, product_name, stock_level = product
        print(f"Ordering more of {product_name}. Current stock: {stock_level}.")

# Example usage
if __name__ == "__main__":
    db = Database(host='localhost', user='your_username', password='your_password', database='your_database')

    # Example: Add a product
    new_product = Product(db, 'Sample Product', 'Electronics', 99.99, 10)
    new_product.add_product()

    # Example: Record a sale with a discount
    sale = Sale(db, product_id=1, quantity=2, discount=10)  # 10% discount
    sale.record_sale()

    # Forecast stock demand
    forecast = forecast_stock_demand(db, product_id=1, period=3)
    print(f"Forecasted demand: {forecast}")

    # Check for low stock and generate orders
    check_low_stock_and_order(db, threshold=5)

    # Close the database connection
    db.close()
