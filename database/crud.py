from database.engine import SessionLocal
from database.models import Product

def create_product(product_data):
    """
    Adds a new product record to the database.

    Args:
        product_data (dict): A dictionary containing the product's attributes.
                             Keys should match the Product model's columns.

    Returns:
        dict: A dictionary confirming the action.
    """
    db = SessionLocal()
    try:
        # Create a new Product object from the input data
        new_product = Product(**product_data)

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        print(f"Successfully added product: {new_product.name}")
        return {"status": "success", "product_id": new_product.id}
    except Exception as e:
        print(f"Error creating product: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
