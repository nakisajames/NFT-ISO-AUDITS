
def make_imap_connection(imap_host, username, password):
    import imaplib
    from datetime import datetime
    api_response = {"error": True, "error_msg": "Imap server is unreachable"}
    t1 = datetime.now()
    try:
        # connect to host using SSL
        imap = imaplib.IMAP4_SSL(imap_host)
        # login to server
        imap.login(username, password)
        # when it get here its ok
        api_response["error"] = False
        api_response["error_msg"] = "Imap server is online"
    except Exception as x:
        api_response["error"] = True
        if str(x).lower().__contains__("login") or str(x).lower().__contains__("credentials"):
            api_response["error_msg"] = "ImapServer Online but User Login Failed error:" + str(x)
        else:
            api_response["error_msg"] = "Imap server is unreachable error:" + str(x)
    t2 = datetime.today()
    api_response["microseconds_elapsed"] = (t2 - t1).microseconds
    return api_response

