from werkzeug.security import check_password_hash


class Auth_Handler:
    def __init__(self, db, auth) -> None:
        self.auth = auth
        @self.auth.verify_password
        def verify_password(username, password):
            if username in db["properties"]["users"] and \
                    check_password_hash(db["properties"]["users"].get(username), password):
                return username
            