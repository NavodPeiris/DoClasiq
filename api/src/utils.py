from structures import inventory_monthly_config, inventory_monthly_category_config, invoice_config, purchase_orders_config, shipping_orders_config

def extract_info(raw_text, classified_output):
    """
    raw_text: str  

    this function returns extracted data as a list of dictionaries

    raw text example:  
        Stock Report for 2016-07  
        Category  
        Product  
        Units Sold  
        Units in Stock  
        Unit Price  
        Beverages  
        Chang  
        105  
        17  
        19  
        Beverages  
        Chartreuse verte  
        48  
        69  
        18  

    normal text lines and text lists are processed as text lines  
    tables are processed in following way:  

        - headers are skipped ex:Category, Product, Units Sold, Units in Stock, Unit Price 
        - each sequence of text lines equal to number of columns, are processed together as a record  
          ex:  
            Beverages  
            Chang  
            105  
            17  
            19  

        - these are processed as a single record as they appear in single line in the table  
    """

    #print(raw_text)

    # Split into lines and skip the header
    data_lines = raw_text.strip().split("\n")

    # Process lines into structured records
    records = []

    # for inventory_monthly class docs: to hold inventory records
    inv_mon_records = {
        "name": "Inventory Table",
        "records": []
    }

    # for inventory_monthly_category class docs: to hold inventory records
    inv_mon_cat_records = {
        "name": "Inventory Table for Category",
        "records": []
    }

    # for invoice class docs: to hold customer details
    invoice_customer_details = {
        "name": "Customer Details",
        "records": []
    }

    # for invoice class docs: to hold total price
    invoice_total_price_details = {
        "name": "Total Price",
        "records": {
            "Total Price": None
        }
    }

    # for invoice class docs: to hold product details
    invoice_product_details = {
        "name": "Product Details Table",
        "records": []
    }

    # for purchase_orders class docs: to hold purchase details
    purchase_orders_records = {
        "name": "Orders Table",
        "records": []
    }

    # for purchase_orders class docs: to hold product details
    purchase_orders_products_records = {
        "name": "Products Table",
        "records": []
    }

    # for shipping_orders class docs: to hold shipping details
    shipping_details_records = {
        "name": "Shipping Details",
        "records": {
            "Ship Name": None,
            "Ship Address": None,
            "Ship City": None,
            "Ship Region": None,
            "Ship Postal Code": None,
            "Ship Country": None,
        }
    }

    # for shipping_orders class docs: to hold customer details
    customer_details_records = {
        "name": "Customer Details",
        "records": {
            "Customer ID": None,
            "Customer Name": None,
        }
    }

    # for shipping_orders class docs: to hold employee details
    employee_details_records = {
        "name": "Employee Details",
        "records": {
            "Employee Name": None,
        }
    }

    # for shipping_orders class docs: to hold shipper details
    shipper_details_records = {
        "name": "Shipper Details",
        "records": {
            "Shipper ID": None,
            "Shipper Name": None
        }
    }

    # for shipping_orders class docs: to hold order details
    order_details_records = {
        "name": "Order Details",
        "records": {
            "Order Date": None,
            "Shipped Date": None
        }
    }

    # for shipping_orders class docs: to hold products details
    products_details_records = {
        "name": "Products",
        "fields": [
            {"name": "Product", "type": "string", "remove": "Product:"},
            {"name": "Quantity", "type": "integer", "remove": "Quantity:"},
            {"name": "Unit Price", "type": "float", "remove": "Unit Price:"},
            {"name": "Total", "type": "float", "remove": "Total:"}
        ],
        "records": []
    }

    # for shipping_orders class docs: to hold total price
    total_price_records = {
        "name": "Total Price",
        "records": {
            "Total Price": None,
        }
    }
    
    config_map = {
        "inventory_monthly": inventory_monthly_config,
        "inventory_monthly_category": inventory_monthly_category_config,
        "invoices": invoice_config,
        "purchase_orders": purchase_orders_config,
        "shipping_orders": shipping_orders_config,
    }

    config = config_map.get(classified_output)
    if not config:
        return []

    structures = config["structures"]

    current_structure_idx = 0
    idx = 0
    total_lines = len(data_lines)
    
    while(idx < total_lines):
        if current_structure_idx < len(structures):
            print(f"Processing line: {data_lines[idx].strip()} with type: {structures[current_structure_idx]['structure_type']} and curent structure index: {current_structure_idx}")

            if structures[current_structure_idx]["structure_type"] == "text line":
                if not structures[current_structure_idx]["ignore"]:
                    if structures[current_structure_idx]["next_starts_with"] != "" and data_lines[idx].strip().startswith(structures[current_structure_idx]["next_starts_with"]):
                        current_structure_idx += 1 # go to next structure
                        continue

                    if data_lines[idx].strip().startswith(structures[current_structure_idx]["starts_with"]):
                        if structures[current_structure_idx]["remove"] != "":
                            # remove the specified text from the line
                            txt_line = data_lines[idx].strip().replace(structures[current_structure_idx]["remove"], "").strip()
                        else:
                            txt_line =  data_lines[idx].strip()

                        try:
                            if structures[current_structure_idx]["type"] == "integer":
                                txt_line = int(txt_line)
                            elif structures[current_structure_idx]["type"] == "float":
                                txt_line = float(txt_line)
                        except ValueError:
                            pass

                        if classified_output == "shipping_orders":
                            shipping_details_fields = list(shipping_details_records["records"].keys())
                            customer_details_fields = list(customer_details_records["records"].keys())
                            employee_details_fields = list(employee_details_records["records"].keys())
                            shipper_details_fields = list(shipper_details_records["records"].keys())
                            order_details_fields = list(order_details_records["records"].keys())
                            product_details_fields = [field["name"] for field in products_details_records["fields"]]
                            
                            while True:
                                idx += 1

                                for field in shipping_details_fields:
                                    if data_lines[idx].strip().startswith(field + ":"):
                                        shipping_details_records["records"][f"{field}"] = data_lines[idx].strip().replace(field + ":", "").strip()
                                    if field == shipping_details_fields[-1]:
                                        # if last item, break
                                        break

                                for field in customer_details_fields:
                                    if data_lines[idx].strip().startswith(field + ":"):
                                        customer_details_records["records"][f"{field}"] = data_lines[idx].strip().replace(field + ":", "").strip()
                                    if field == customer_details_fields[-1]:
                                        # if last item, break
                                        break
                                
                                for field in employee_details_fields:
                                    if data_lines[idx].strip().startswith(field + ":"):
                                        employee_details_records["records"][f"{field}"] = data_lines[idx].strip().replace(field + ":", "").strip()
                                    if field == employee_details_fields[-1]:
                                        # if last item, break
                                        break
                                
                                for field in shipper_details_fields:
                                    if data_lines[idx].strip().startswith(field + ":"):
                                        shipper_details_records["records"][f"{field}"] = data_lines[idx].strip().replace(field + ":", "").strip()
                                    if field == shipper_details_fields[-1]:
                                        # if last item, break
                                        break
                                
                                for field in order_details_fields:
                                    if data_lines[idx].strip().startswith(field + ":"):
                                        order_details_records["records"][f"{field}"] = data_lines[idx].strip().replace(field + ":", "").strip()
                                    if field == order_details_fields[-1]:
                                        # if last item, break
                                        break

                                if data_lines[idx].strip().startswith(total_price_records["name"] + ":"):
                                    txt_line = data_lines[idx].strip().replace(total_price_records["name"] + ":", "").strip()
                                    try:
                                        txt_line = float(txt_line)
                                    except ValueError:
                                        pass
                                    total_price_records["records"]["Total Price"] = txt_line
                                    break

                                if data_lines[idx].strip().startswith(product_details_fields[0] + ":"):
                                    product_record = {field: None for field in product_details_fields}
                                    
                                    for i in range(len(product_details_fields)):
                                        if idx >= total_lines:
                                            break
                                        if data_lines[idx].strip().startswith(product_details_fields[i] + ":"):
                                            if products_details_records["fields"][i]["remove"] != "":
                                                txt_line = data_lines[idx].replace(products_details_records["fields"][i]["remove"], "").strip()
                                            else:
                                                txt_line = data_lines[idx].strip()


                                            # Extract relevant fields
                                            if products_details_records["fields"][i]["type"] == "string":
                                                product_record[products_details_records["fields"][i]["name"]] = txt_line
                                            elif products_details_records["fields"][i]["type"] == "integer":
                                                product_record[products_details_records["fields"][i]["name"]] = int(txt_line)
                                            elif products_details_records["fields"][i]["type"] == "float":
                                                product_record[products_details_records["fields"][i]["name"]] = float(txt_line)
                                        idx += 1
                                    products_details_records["records"].append(product_record)
                                    continue
                        else:
                            records.append({
                                f"{structures[current_structure_idx]['name']}": txt_line
                            })
                        current_structure_idx += 1 # go to next structure
                else:
                    # if ignored, no need to process this structure
                    current_structure_idx += 1 # go to next structure
                idx += 1

            elif structures[current_structure_idx]["structure_type"] == "table":
                # skip the header line of table
                if not data_lines[idx].strip() in structures[current_structure_idx]["headers"]:
                    # check if current line belongs to next structure
                    if structures[current_structure_idx]["next_starts_with"] != "" and data_lines[idx].strip().startswith(structures[current_structure_idx]["next_starts_with"]):
                        current_structure_idx += 1 # go to next structure
                        continue

                    if data_lines[idx].strip() == "":
                        # empty line after table means move to next structure
                        current_structure_idx += 1 # go to next structure
                        continue
                    
                    fields = structures[current_structure_idx]["fields"]

                    # Initialize field defaults
                    table_record = {field["name"]: None for field in fields}
                    
                    for i in range((structures[current_structure_idx]["columns"])):
                        if idx >= total_lines:
                            break

                        if fields[i]["remove"] != "":
                            txt_line = data_lines[idx].replace(fields[i]["remove"], "").strip()
                        else:
                            txt_line = data_lines[idx].strip()

                        # Extract relevant fields
                        try:
                            if fields[i]["type"] == "string":
                                table_record[fields[i]["name"]] = txt_line
                            elif fields[i]["type"] == "integer":
                                table_record[fields[i]["name"]] = int(txt_line)
                            elif fields[i]["type"] == "float":
                                table_record[fields[i]["name"]] = float(txt_line)
                            else:
                                # fallback to string if type is wrong
                                table_record[fields[i]["name"]] = txt_line
                        except ValueError:
                            # fallback to string if conversion fails
                            table_record[fields[i]["name"]] = txt_line

                        idx += 1
                    
                    if classified_output == "inventory_monthly":
                        if structures[current_structure_idx]["name"] == inv_mon_records["name"]:
                            # add to inventory table records
                            inv_mon_records["records"].append(table_record)
                        else:
                            # add to records
                            records.append(table_record)
                    elif classified_output == "inventory_monthly_category":
                        if structures[current_structure_idx]["name"] == inv_mon_cat_records["name"]:
                            # add to inventory table records
                            inv_mon_cat_records["records"].append(table_record)
                        else:
                            # add to records
                            records.append(table_record)
                    elif classified_output == "invoices":
                        if structures[current_structure_idx]["name"] == invoice_product_details["name"]:
                            # add to invoice products table records
                            invoice_product_details["records"].append(table_record)
                        else:
                            # add to records
                            records.append(table_record)
                    elif classified_output == "purchase_orders":
                        if structures[current_structure_idx]["name"] == purchase_orders_records["name"]:
                            # add to purchase orders table records
                            purchase_orders_records["records"].append(table_record)
                        elif structures[current_structure_idx]["name"] == purchase_orders_products_records["name"]:
                            # add to purchase orders products table records
                            purchase_orders_products_records["records"].append(table_record)
                        else:
                            # add to records
                            records.append(table_record)

                    elif classified_output == "shipping_orders":
                        # for now shipping_orders type docs don't have tables
                        pass
                    else:
                        # add to records
                        records.append(table_record)
                    
                else:
                    idx += 1

            elif structures[current_structure_idx]["structure_type"] == "key-value table":
                # check if current line belongs to next structure
                if structures[current_structure_idx]["next_starts_with"] != "" and data_lines[idx].strip().startswith(structures[current_structure_idx]["next_starts_with"]):
                    current_structure_idx += 1 # go to next structure
                    continue

                if data_lines[idx].strip() == "":
                    # empty line after table means move to next structure
                    current_structure_idx += 1 # go to next structure
                    continue
                
                keys = structures[current_structure_idx]["keys"]

                # Initialize field defaults
                table_record = {key["name"]: None for key in keys}
                
                for i in range((structures[current_structure_idx]["num_of_keys"])):
                    if idx >= total_lines:
                        break
                    
                    if keys[i]["remove"] != "":
                        # next item after key is the value
                        txt_line = data_lines[idx+1].replace(keys[i]["remove"], "").strip()
                    else:
                        txt_line = data_lines[idx+1].strip()

                    # Extract relevant 
                    try:
                        if keys[i]["type"] == "string":
                            table_record[keys[i]["name"]] = txt_line
                        elif keys[i]["type"] == "integer":
                            table_record[keys[i]["name"]] = int(txt_line)
                        elif keys[i]["type"] == "float":
                            table_record[keys[i]["name"]] = float(txt_line)
                        else:
                            # fallback to string if type is wrong
                            table_record[fields[i]["name"]] = txt_line
                    except ValueError:
                        # fallback to string if conversion fails
                        table_record[keys[i]["name"]] = txt_line

                    # go to next key
                    idx += 2
                
                if classified_output == "invoices":
                    if structures[current_structure_idx]["name"] == invoice_customer_details["name"]:
                        # add to invoice products table records
                        invoice_customer_details["records"].append(table_record)
                    else:
                        # add to records
                        records.append(table_record)
                else:
                    records.append(table_record)

            elif structures[current_structure_idx]["structure_type"] == "table_summary":
                if data_lines[idx].strip().startswith(structures[current_structure_idx]["starts_with"]):
                    # next to summary name cell, we have the value
                    txt_line = data_lines[idx+1].strip()

                    try:
                        if structures[current_structure_idx]["type"] == "integer":
                            txt_line = int(txt_line)
                        elif structures[current_structure_idx]["type"] == "float":
                            txt_line = float(txt_line)
                    except ValueError:
                        pass

                    if classified_output == "invoices":
                        invoice_total_price_details["records"]["Total Price"] = txt_line

                    current_structure_idx += 1 # go to next structure
                    idx += 2
                else:
                    # if not starting with summary name, just skip this line
                    idx += 1
            else:
                idx += 1

        else:
            # progress through last lines
            idx += 1
    
    # append the predefined objects to output that hold some data specific to a document structure
    if classified_output == "inventory_monthly":
        records.append(inv_mon_records)
    if classified_output == "inventory_monthly_category":
        records.append(inv_mon_cat_records)
    if classified_output == "invoices":
        records.append(invoice_customer_details)
        records.append(invoice_product_details)
        records.append(invoice_total_price_details)
    if classified_output == "purchase_orders":
        records.append(purchase_orders_records)
        records.append(purchase_orders_products_records)
    if classified_output == "shipping_orders":
        records.append(shipping_details_records)
        records.append(customer_details_records)
        records.append(employee_details_records)
        records.append(shipper_details_records)
        records.append(order_details_records)
        records.append({
            # leave out fields as not needed in output
            "name": products_details_records["name"],
            "records": products_details_records["records"]
        })
        records.append(total_price_records)

    print(records[:5])

    return records