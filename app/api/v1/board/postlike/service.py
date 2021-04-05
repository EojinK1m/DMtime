

class PostlikeService():
    
    def get_postlike_by_user_id(self, user_id):
        pass

    def abort_404_if_not_exist_postlike_by_user(self, user_id):
        pass

    def abort_409_if_postlike_by_user_already_exist(self, user_id):
        pass

    def create_postlike(self, user_id):
        pass


class PostdislikeService():

    def get_postdislike_by_user_id(self, user_id):
        pass

    def abort_404_if_not_exist_postdislike_by_user(self, user_id):
        pass
    
    def abort_409_if_postdislike_by_user_already_exist(self, user_id):
        pass

    def create_postdislike(self, user_id):
        pass
