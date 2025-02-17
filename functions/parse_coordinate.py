def parse_coordinates(input_string):
    import re
    
    numbers = re.findall(r'-?\d+', input_string)
    
    if len(numbers) >= 2:
        return (int(numbers[0]), int(numbers[1]))
    
    return None  
