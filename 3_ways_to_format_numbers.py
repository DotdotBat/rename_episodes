def format_with_leading_zeros_zfill(number:int|float, leading_digits_count:int)->str:
    if isinstance(number, float) and number.is_integer():
        number = int(number)
    num_str = str(number)
    parts = num_str.split('.')
    whole_part = parts[0]
    padded_whole = whole_part.zfill(leading_digits_count)
    if len(parts) == 2:  # If there was a decimal part
        return f"{padded_whole}.{parts[1]}"
    else:
        return padded_whole
    
def format_with_leading_zeros_format(number:int|float, leading_digits_count:int)->str:
    if isinstance(number, float) and number.is_integer():
        number = int(number)
    num_str = str(number)
    parts = num_str.split('.')
    whole_part = parts[0]
    padded_whole = '{:0{width}d}'.format(whole_part, width=leading_digits_count)
    if len(parts) == 2:  # If there was a decimal part
        return f"{padded_whole}.{parts[1]}"
    else:
        return padded_whole

def format_with_leading_zeros(number:int|float, leading_digits_count:int)->str:
    if isinstance(number, float) and number.is_integer():
        number = int(number)
    num_str = str(number)
    parts = num_str.split('.')
    whole_part = parts[0]
    padded_whole = f'{whole_part:0{leading_digits_count}d}'
    if len(parts) == 2:  # If there was a decimal part
        return f"{padded_whole}.{parts[1]}"
    else:
        return padded_whole