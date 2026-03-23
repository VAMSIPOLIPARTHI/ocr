import re

def extract_fields(text):
    data = {"name": None, "amount": None, "date": None, "id": None}
    
    # Name: Look for "Name" or "Customer" followed by text
    name_match = re.search(r"(?:name|customer|vendor)[:\-]?\s*([a-zA-Z ]{3,30})", text, re.I)
    if name_match: data["name"] = name_match.group(1).strip()
    
    # Amount: Handle symbols, commas, and decimals. Capture only the numeric part.
    amount_match = re.search(r"(?:amt|amount|total|sum)[:\-]?\s*(?:₹|\$|USD|INR)?\s*([\d,]+\.?\d*)", text, re.I)
    if amount_match: 
        raw_amt = amount_match.group(1).replace(",", "")
        data["amount"] = raw_amt
    
    # Date: Support DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    date_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}-\d{2}-\d{2})", text)
    if date_match: data["date"] = date_match.group(1)
    
    # ID: Look for Invoice, ID, No, or Ref followed by alphanumeric. Require colon or space.
    id_match = re.search(r"\b(?:id|invoice|no|number|ref|bill)[:\- ]\s*([A-Z0-9\-]{4,20})", text, re.I)
    if id_match: data["id"] = id_match.group(1).strip()
    
    return data




