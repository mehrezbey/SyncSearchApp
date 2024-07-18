from search_module.utils.colors import colors
import sys

def print_log(operation, tablename, data, resp):
    color = colors.END
    if(operation == 'insert'):
        color = colors.GREEN
        print(f"{color}--- Inserted operation on {tablename} ---")
        sys.stdout.flush()
        print(f"{color}\t Inserted data : {data}")
        sys.stdout.flush()

    elif(operation == 'delete'):
        color = colors.RED
        print(f"{color}--- Deleted operation on {tablename} ---")
        sys.stdout.flush()

        print(f"{color}\t Deleted data : {data}")
        sys.stdout.flush()

    elif(operation == 'update'):
        color = colors.YELLOW
        print(f"{color}--- Updated operation on {tablename} ---")
        sys.stdout.flush()

        print(f"{color}Updated data : {data}")
        sys.stdout.flush()

    
    print(f"{color}\t Index result : {resp['result']}")
    sys.stdout.flush()
    print(f"---  ---{colors.END}")
    sys.stdout.flush()

    