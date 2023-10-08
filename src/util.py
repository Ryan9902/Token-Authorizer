import base64


def get_addr(token :str) ->str: # This is to get the user id from the token instead of making another request to the api
    token_parts = token.split(".")
    user_id = base64.urlsafe_b64decode(token_parts[0] + "==").decode("utf-8")
    return user_id

