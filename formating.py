def check_mess(mess):
    if "напомни" in mess.text.lower():
        return True
    else:
        return False