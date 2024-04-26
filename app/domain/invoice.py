import uuid
from fastapi.exceptions import HTTPException

# Store the invoices
invoices = {}
invoice_details = {}
invoice_sundry = {}

def check_invoice_exist(id):
    return id in invoices

def validate_invoice_item(item):
    if item['qty'] * item['price'] != item['amount'] or item['qty'] < 1 or item['price'] < 1 or item['amount'] < 1:
        raise HTTPException(503, detail=f"Invalid item details for {item['itemName']}")

def validate_billing_sundry(sundry):
    if not sundry['amount']:
        raise HTTPException(503, detail=f"Sundry amount cannot be 0 for {sundry['billingSundryName']}")

def validate_invoice(kwargs):
    invoiceDetails = kwargs.get('invoiceDetails', [])
    billingSundry = kwargs.get('billingSundry', [])
    invoice_details_amount = sum(item['amount'] for item in invoiceDetails)
    sundry_amount = sum(sundry['amount'] for sundry in billingSundry)
    total_amount = kwargs.get('totalAmount', 0)

    if total_amount != invoice_details_amount + sundry_amount:
        raise HTTPException(503, detail="Total amount does not match with item and sundry amounts")

def create_invoice(**kwargs):
    invoice_id = str(uuid.uuid4().hex)
    validate_invoice(kwargs)

    invoiceDetails = kwargs.pop("invoiceDetails", [])
    billingSundry = kwargs.pop("billingSundry", [])

    for item in invoiceDetails:
        item["id"] = invoice_id
        validate_invoice_item(item)

    for sundry in billingSundry:
        sundry["id"] = invoice_id
        validate_billing_sundry(sundry)

    kwargs['id'] = invoice_id
    invoices[invoice_id] = kwargs

    invoice_details[invoice_id] = invoiceDetails
    invoice_sundry[invoice_id] = billingSundry

    return kwargs

def get_invoice_by_id(id):
    if not check_invoice_exist(id):
        raise HTTPException(503, detail=f"No invoice exists with id: {id}")

    result = invoices[id]
    result['invoiceDetails'] = invoice_details.get(id, [])
    result['billingSundry'] = invoice_sundry.get(id, [])
    return result

def delete_invoice_by_id(id):
    if not check_invoice_exist(id):
        raise HTTPException(503, detail=f"No invoice exists with id: {id}")
    
    del invoices[id]
    del invoice_details[id]
    del invoice_sundry[id]

    return 'Deleted'

def update_invoice_by_id(**kwargs):
    invoice_id = kwargs.pop("id")
    if not check_invoice_exist(invoice_id):
        raise HTTPException(503, detail=f"No invoice exists with id: {invoice_id}")
    
    validate_invoice(kwargs)

    invoiceDetails = kwargs.pop("invoiceDetails", [])
    billingSundry = kwargs.pop("billingSundry", [])

    for item in invoiceDetails:
        item["id"] = invoice_id
        validate_invoice_item(item)

    for sundry in billingSundry:
        sundry["id"] = invoice_id
        validate_billing_sundry(sundry)

    invoices[invoice_id] = kwargs
    invoice_details[invoice_id] = invoiceDetails
    invoice_sundry[invoice_id] = billingSundry

    return kwargs
