from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Authenticate using en e-mail address.
    """
    def authenticate(self, request, username = None, password=None):
        try:
            # Find the user by email instead of username
            user = User.objects.get(email= username)
            if user.check_password(password):
                return user
            return None # Return None if password is incorrect
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None # Return None if user is not found or multiple users exist
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk= user_id) # Retrieve user by ID
        except User.DoesNotExist:
            return None # Return None if user ID is not found
        

        