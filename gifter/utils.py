

def user_display(user):
    if user.first_name or user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.email
