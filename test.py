import os
def is_admin():
    return os.geteuid == 0

print(is_admin)