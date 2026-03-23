from rapidfuzz import fuzz

def match_details(field1, field2, field3, field4, field5, ocr_text):
    """
    Placeholder matching function for the old KYC route.
    Using rapidfuzz since it's in your requirements.txt.
    """
    ocr_lower = ocr_text.lower() if ocr_text else ""
    
    return {
        "match_1": fuzz.partial_ratio(field1.lower(), ocr_lower) if field1 else 0,
        "match_2": fuzz.partial_ratio(field2.lower(), ocr_lower) if field2 else 0,
        "match_3": fuzz.partial_ratio(field3.lower(), ocr_lower) if field3 else 0,
        "match_4": fuzz.partial_ratio(field4.lower(), ocr_lower) if field4 else 0,
        "match_5": fuzz.partial_ratio(field5.lower(), ocr_lower) if field5 else 0,
    }
