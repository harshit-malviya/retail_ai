from products.models import Product
from billing.models import Sale

def process_return(return_obj):
    item = return_obj.item
    product = return_obj.product
    quantity = return_obj.quantity
    refund_amount = return_obj.refund_amount

    # Update product stock (assuming product has a stock field)
    product.stock_quantity += quantity
    product.save()

    # Update sale item quantity
    item.quantity -= quantity
    item.save()

    # Update sale total amount
    sale = return_obj.sale
    sale.total_amount -= refund_amount
    sale.save()

    # Update customer total spent
    customer = sale.customer
    customer.total_spent -= refund_amount
    if customer.total_spent < 0:
        customer.total_spent = 0  # Avoid negative values
    customer.save()