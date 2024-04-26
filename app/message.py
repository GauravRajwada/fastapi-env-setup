from pydantic import BaseModel

class InvoiceDetails(BaseModel):
    itemName: str
    qty: int
    price: float
    amount: float

class BillingSundary(BaseModel):
    billingSundryName: str
    amount: float


class CreateInvoice(BaseModel):
    # id: str
    date: str
    invoiceNumber: int
    customerName: str
    billingAddress: str
    shippingAddress: str
    gstic: str
    totalAmount: float
    invoiceDetails: list[InvoiceDetails]
    billingSundry: list[BillingSundary]


