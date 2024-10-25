import unittest
from inventory_management import Database, Product, Supplier, Sale

class TestInventoryManagement(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the database connection before any tests run."""
        cls.db = Database()

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after all tests run."""
        cls.db.close()

    def test_add_product(self):
        """Test adding a product to the database."""
        product = Product(self.db, "Test Product", "Test Category", 19.99, 50)
        product.add_product()
        
        # Check if the product was added
        self.db.cursor.execute("SELECT name FROM products WHERE name = %s", ("Test Product",))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Test Product")

    def test_add_supplier(self):
        """Test adding a supplier to the database."""
        supplier = Supplier(self.db, "Test Supplier", "test@supplier.com")
        supplier.add_supplier()
        
        # Check if the supplier was added
        self.db.cursor.execute("SELECT name FROM suppliers WHERE name = %s", ("Test Supplier",))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Test Supplier")

    def test_record_sale(self):
        """Test recording a sale."""
        # First, add a product to record a sale against
        product = Product(self.db, "Sale Product", "Sale Category", 29.99, 100)
        product.add_product()
        
        # Record the sale
        sale = Sale(self.db, product_id=1, quantity=2)  # Assuming the product ID is 1
        sale.record_sale()
        
        # Check if the sale was recorded
        self.db.cursor.execute("SELECT quantity FROM sales WHERE product_id = %s", (1,))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 2)

if __name__ == "__main__":
    unittest.main()
