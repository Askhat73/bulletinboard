from django.contrib.auth.mixins import UserPassesTestMixin


class UserTypeIsAdvertiserMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.is_advertiser
        return False


class UserTypeIsModeratorMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.is_moderator
        return False


class UserTypeIsAdminMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.is_admin
        return False
