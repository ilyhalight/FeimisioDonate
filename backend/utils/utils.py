def sort_dict(data: dict):
    sorted_tuple = sorted(data.items(), key=lambda x: x[0]) 
    return dict(sorted_tuple)