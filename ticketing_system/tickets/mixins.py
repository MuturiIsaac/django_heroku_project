from django.contrib.auth.mixins import UserPassesTestMixin

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.profile.is_staff

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_staff