import sys
import time

class Blockchain:
    def __init__(self):
        self.owner = None
        self.unique_id = 1
        self.manufacturers = {}
        self.products = {}

    def only_owner(self, address):
        if address != self.owner:
            raise PermissionError("Only the owner can perform this action")

    def create_manufacturer(self, name, address):
        self.only_owner(msg.sender)
        self.manufacturers[address] = {
            "exists": True,
            "name": name,
            "_address": address,
            "products": {},  # Track products created by this manufacturer
        }

    def addproduct(self, p, sender_address):
        '''if sender_address not in self.manufacturers or not self.manufacturers[sender_address]["exists"]:
            raise ValueError("You are not a Manufacturer!")'''
        
        product = p
        product["exists"]: True
        product["owner"]: sender_address
        product["timestamp"]: time.time()
        product["isAuthentic"]: True
        
        self.products[self.unique_id] = product
        '''self.manufacturers[sender_address]["products"][self.unique_id] = True

        # Emit an event (print for simplicity)
        print(f"ProductAdded: uniqueId={self.unique_id}, timestamp={product['timestamp']}, "
              f"productName={name}, productId={product_id}, "
              f"retail_price={retail_price}, discounted_price={discounted_price}, "
              f"brand={brand}, is_authentic=True, manufacturer={sender_address}")
'''
        self.unique_id += 1

    def getProduct(self, uniqueid):
        return {
            "exists": True,
            "productid": 123,
            "uniqueid": 1,
            "productname": "Iphone",
            "retailprice": 1500,
            "discountedprice": 1000,
            "brand": "Apple",
            "manufacturer": "add",
            "timestamp": "123",
            "isAuthentic": True,
        }
#self.products.get(uniqueid, {})
#return self.products.get(unique_id, {}).get("isAuthentic", False)
