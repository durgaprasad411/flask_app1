class User:
    users = []
    next_id = 1

    def __init__(self, name, mobile, resume):
        self.id = User.next_id
        self.name = name
        self.mobile = mobile
        self.resume = resume
        User.next_id += 1
        User.users.append(self)

    @classmethod
    def get_all_users(cls):
        return [{"id": user.id, "name": user.name, "mobile": user.mobile, "resume": user.resume} for user in cls.users]

    @classmethod
    def update_user(cls, user_id, name, mobile, resume):
        for user in cls.users:
            if user.id == user_id:
                user.name = name
                user.mobile = mobile
                user.resume = resume
                return user
        return None

    @classmethod
    def delete_user(cls, user_id):
        global users
        users = [user for user in cls.users if user.id != user_id]
        return any(user.id == user_id for user in cls.users)
