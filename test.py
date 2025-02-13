import re

def nice_autorize(email, password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_pattern, email) is None:
        return(False)
    
    if re.match(password_pattern, password) is None:
        return(True, False)
    
    return(True)

print(nice_autorize('gromlbv@gmail.com', 'lbvDima17'))