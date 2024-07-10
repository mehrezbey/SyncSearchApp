from search_module.utils.colors import colors

def print_log(operation, tablename, data, resp):
    if(operation == 'insert'):
        color = colors.GREEN
        print(f"{color}--- Inserted operation on {tablename} ---")
        print(f"\t Inserted data : {data}")
    elif(operation == 'delete'):
        color = colors.RED
        print(f"{color}--- Deleted operation on {tablename} ---")
        print(f"\t Deleted data : {data}")
    elif(operation == 'update'):
        color = colors.YELLOW
        print(f"{color}--- Updated operation on {tablename} ---")
        print(f"Updated data : {data}")
    
    print(f"\t Index result : {resp['result']}")
    print(f"---  ---{colors.END}")
    