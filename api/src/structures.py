
# ---------------------structure configurations for data extraction----------------------
inventory_monthly_config = {
    "structures": [
        {
            "structure_type": "text line",
            "starts_with": "Stock Report",
            "next_starts_with": "Category",
            "name": "title",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "table",
            "starts_with": "Category",
            "next_starts_with": "",    # starting text of next item (empty means no next item)
            "name": "Inventory Table",
            "columns": 5,
            "headers": ["Category", "Product", "Units Sold", "Units in Stock", "Unit Price"],
            "fields": [
                {"name": "Category", "type": "string", "remove": ""},
                {"name": "Product", "type": "string", "remove": ""},
                {"name": "Units Sold", "type": "integer", "remove": ""},
                {"name": "Units in Stock", "type": "integer", "remove": ""},
                {"name": "Unit Price", "type": "float", "remove": ""}
            ],
        }
    ]
}

inventory_monthly_category_config = {
    "structures": [
        {
            "structure_type": "text line",
            "starts_with": "Stock Report",
            "next_starts_with": "Category :",
            "name": "title",
            "type": "string",
            "remove": "",
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Category :",
            "next_starts_with": "id category",
            "name": "category",
            "type": "string",
            "remove": "Category :",
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "id category :",
            "next_starts_with": "Product",
            "name": "id category",
            "type": "integer",
            "remove": "id category :",
            "ignore": False
        },
        {
            "structure_type": "table",
            "starts_with": "Product",
            "next_starts_with": "",    # starting text of next item (empty means no next item)
            "name": "Inventory Table for Category",
            "columns": 4,
            "headers": ["Product", "Units Sold", "Units in Stock", "Unit Price"],
            "fields": [
                {"name": "Product", "type": "string", "remove": ""},
                {"name": "Units Sold", "type": "integer", "remove": ""},
                {"name": "Units in Stock", "type": "integer", "remove": ""},
                {"name": "Unit Price", "type": "float", "remove": ""}
            ],
        }
    ]
}

invoice_config = {
    "structures": [
        {
            "structure_type": "text line",
            "starts_with": "Order ID",
            "next_starts_with": "Customer ID",
            "name": "order id",
            "type": "integer",
            "remove": "Order ID:",
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Customer ID",
            "next_starts_with": "Order Date",
            "name": "customer id",
            "type": "string",
            "remove": "Customer ID:",
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Order Date",
            "next_starts_with": "Customer Details:",
            "name": "order date",
            "type": "string",
            "remove": "Order Date:",
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Customer Details:",
            "next_starts_with": "Contact Name:",
            "name": "customer details heading",
            "type": "string",
            "remove": "",
            "ignore": True
        },
        {
            "structure_type": "key-value table",
            "starts_with": "Contact Name:",
            "next_starts_with": "Product Details:",    # starting text of next item (empty means no next item)
            "name": "Customer Details",
            "num_of_keys": 7,
            "keys": [
                {"name": "Contact Name", "type": "string", "remove": ""},
                {"name": "Address", "type": "string", "remove": ""},
                {"name": "City", "type": "string", "remove": ""},
                {"name": "Postal Code", "type": "integer", "remove": ""},
                {"name": "Country", "type": "string", "remove": ""},
                {"name": "Phone", "type": "string", "remove": ""},
                {"name": "Fax", "type": "string", "remove": ""}
            ],
        },
        {
            "structure_type": "text line",
            "starts_with": "Product Details:",
            "next_starts_with": "Product ID",
            "name": "product details heading",
            "type": "string",
            "remove": "",
            "ignore": True
        },
        {
            "structure_type": "table",
            "starts_with": "Product ID",
            "next_starts_with": "TotalPrice",    # starting text of next item (empty means no next item)
            "name": "Product Details Table",
            "columns": 4,
            "headers": ["Product ID", "Product Name", "Quantity", "Unit Price"],
            "fields": [
                {"name": "Product ID", "type": "integer", "remove": ""},
                {"name": "Product Name", "type": "string", "remove": ""},
                {"name": "Quantity", "type": "integer", "remove": ""},
                {"name": "Unit Price", "type": "float", "remove": ""}
            ],
        },
        {
            "structure_type": "table_summary",
            "starts_with": "TotalPrice",
            "next_starts_with": "Page 1",    # starting text of next item (empty means no next item)
            "name": "Products Total Price",
            "type": "float",
            "remove": "",
        },
        {
            "structure_type": "text line",
            "starts_with": "Page 1",
            "next_starts_with": "",
            "name": "page number",
            "type": "string",
            "remove": "",
            "ignore": True
        },
    ]
}

purchase_orders_config = {
    "structures": [
        {
            "structure_type": "text line",
            "starts_with": "Purchase Orders",
            "next_starts_with": "Order ID",
            "name": "title",
            "type": "string",
            "remove": "",
            "ignore": False
        },
        {
            "structure_type": "table",
            "starts_with": "Order ID",
            "next_starts_with": "Products",    # starting text of next item (empty means no next item)
            "name": "Orders Table",
            "columns": 3,
            "headers": ["Order ID", "Order Date", "Customer Name"],
            "fields": [
                {"name": "Order ID", "type": "integer", "remove": ""},
                {"name": "Order Date", "type": "string", "remove": ""},
                {"name": "Customer Name", "type": "string", "remove": ""},
            ],
        },
        {
            "structure_type": "text line",
            "starts_with": "Products",
            "next_starts_with": "Product ID:",
            "name": "products heading",
            "type": "string",
            "remove": "",
            "ignore": True
        },
        {
            "structure_type": "table",
            "starts_with": "Product ID:",
            "next_starts_with": "Page 1",    # starting text of next item (empty means no next item)
            "name": "Products Table",
            "columns": 4,
            "headers": ["Product ID:", "Product:", "Quantity:", "Unit Price:"],
            "fields": [
                {"name": "Product ID:", "type": "integer", "remove": ""},
                {"name": "Product:", "type": "string", "remove": ""},
                {"name": "Quantity:", "type": "integer", "remove": ""},
                {"name": "Unit Price:", "type": "float", "remove": ""}
            ],
        },
        {
            "structure_type": "text line",
            "starts_with": "Page 1",
            "next_starts_with": "",
            "name": "page number",
            "type": "string",
            "remove": "",
            "ignore": True
        },
    ]
}

shipping_orders_config = {
    "structures": [
        {
            "structure_type": "text line",
            "starts_with": "Order ID:",
            "next_starts_with": "Shipping Details:",
            "name": "Order ID",
            "type": "string",
            "remove": "Order ID:", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Shipping Details:",
            "next_starts_with": "Customer Details:",
            "name": "Shipping Details",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Customer Details:",
            "next_starts_with": "Employee Details:",
            "name": "Customer Details",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Employee Details:",
            "next_starts_with": "Shipper Details:",
            "name": "Employee Details",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Shipper Details:",
            "next_starts_with": "Order Details:",
            "name": "Shipper Details",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Order Details:",
            "next_starts_with": "Products:",
            "name": "Order Details",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Products:",
            "next_starts_with": "Total Price:",
            "name": "Products",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
        {
            "structure_type": "text line",
            "starts_with": "Total Price:",
            "next_starts_with": "",
            "name": "Total Price",
            "type": "string",
            "remove": "", # text to remove from the line
            "ignore": False
        },
    ]
}
# ---------------------------------------------------------------------------------------
