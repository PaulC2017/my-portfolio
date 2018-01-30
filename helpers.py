def check_user_name(un):
    
   if un == "":
     return False
   elif un.count(" ") != 0:
     return False
   elif len(un) < 3 or len(un) > 20:
     return False

def check_pass_word(pw ):
    
   if pw == "":
     return False
   elif pw.count(" ") != 0:
     return False
   elif len(pw) < 3 or len(pw) > 20:
     return False
    
def verify_pass_word(vpw,pw):  
    if pw == vpw:
      return True
    else:
       return False

def verify_email(em):
    if em.count(" ") != 0 or em.count("@") != 1 or em.count(".") != 1:
      return False
    elif len(em) < 3 or len(em) > 20:
      return False
    
     
