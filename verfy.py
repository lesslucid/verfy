import re

def validate_trade_list(trade_list, username):
    errors = []
    valid_pattern = re.compile(rf'\({re.escape(username)}\) (\d{{8}}-[A-Z]+|\$\d+|%[A-Z]+): (.+)')
    item_pattern = re.compile(r'(\d{8}-[A-Z]+|\$\d+|%[A-Z]+)')
    
    for line_number, line in enumerate(trade_list.split('\n'), 1):
        line = line.strip()
        if not line:
            continue
        
        match = valid_pattern.match(line)
        if not match:
            errors.append(f"Line {line_number}: Invalid format. Expected '({username}) ITEM_ID: WANTS_LIST'")
            continue
        
        item_id, wants = match.groups()
        
        # Validate item ID
        if not re.match(r'\d{8}-[A-Z]+|\$\d+|%[A-Z]+', item_id):
            errors.append(f"Line {line_number}: Invalid item ID format: {item_id}. Expected format: '12345678-ABCDE' or '$XX' or '%GROUPID'")
        
        # Validate wants
        wants_items = item_pattern.findall(wants)
        if not wants_items:
            errors.append(f"Line {line_number}: No valid items in wants list. Each item should be in format '12345678-ABCDE', '$XX', or '%GROUPID'")
        
        for want in wants_items:
            if not (re.match(r'\d{8}-[A-Z]+', want) or 
                    re.match(r'\$\d+', want) or 
                    re.match(r'%[A-Z]+', want)):
                errors.append(f"Line {line_number}: Invalid want item: {want}. Expected format: '12345678-ABCDE' or '$XX' or '%GROUPID'")
    
    return errors

# Example usage
username = input("Enter your username: ")
trade_list = input("Enter your trade list (paste and press Enter twice when done):\n")

errors = validate_trade_list(trade_list, username)
if errors:
    print("\nErrors found:")
    for error in errors:
        print(error)
else:
    print("\nNo errors found in the trade list.")
