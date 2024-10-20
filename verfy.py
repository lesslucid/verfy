import re

def validate_trade_list(trade_list, username):
    errors = []
    valid_pattern = re.compile(rf'\({re.escape(username)}\) (\d{{8}}-[A-Z0-9]+|\$\d+|%[A-Z]+): (.+)')
    item_id_pattern = re.compile(r'^\d{8}-[A-Z0-9]{1,5}$')
    money_pattern = re.compile(r'^\$\d+$')
    group_pattern = re.compile(r'^%[A-Z]+$')
    
    for line_number, line in enumerate(trade_list.split('\n'), 1):
        line = line.strip()
        if not line:
            continue
        
        match = valid_pattern.match(line)
        if not match:
            errors.append(f"Line {line_number}: Invalid format. Expected '({username}) ITEM_ID: WANTS_LIST'")
            continue
        
        item_id, wants = match.groups()
        
        # Validate item ID (now includes money and group patterns)
        if not (item_id_pattern.match(item_id) or money_pattern.match(item_id) or group_pattern.match(item_id)):
            errors.append(f"Line {line_number}: Invalid item ID format: {item_id}. Expected format: '12345678-ABCDE', '12345678-A1B2C', '$XX', or '%GROUPID'")
        
        # Validate wants
        wants_items = wants.split()
        if not wants_items:
            errors.append(f"Line {line_number}: No valid items in wants list. Each item should be in format '12345678-ABCDE', '12345678-A1B2C', '$XX', or '%GROUPID'")
        
        for want in wants_items:
            if not (item_id_pattern.match(want) or money_pattern.match(want) or group_pattern.match(want)):
                errors.append(f"Line {line_number}: Invalid want item: {want}. Expected format: '12345678-ABCDE', '12345678-A1B2C', '$XX', or '%GROUPID'")
    
    return errors

# Example usage
username = input("Enter your username: ")
print("Enter your trade list (paste and press Enter twice when done):")
trade_list_lines = []
while True:
    line = input()
    if line:
        trade_list_lines.append(line)
    else:
        break
trade_list = "\n".join(trade_list_lines)

errors = validate_trade_list(trade_list, username)
if errors:
    print("\nErrors found:")
    for error in errors:
        print(error)
else:
    print("\nNo errors found in the trade list.")

