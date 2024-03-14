from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from PIL import Image
import tempfile
import uuid
import os

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser' + str(uuid.uuid4()), password='12345')
        self.profile = self.user.profile
        self.profile.bio = "This is a test bio."
        self.profile.save()

    def test_profile_creation(self):
        self.assertEqual(self.user.profile.bio, "This is a test bio.")
        self.assertTrue(isinstance(self.user.profile, Profile))

    def test_profile_str(self):
        expected_username = f'{self.user.username} Profile'
        self.assertEqual(str(self.profile), expected_username)

def test_avatar_resizing(self):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
        image = Image.new('RGB', (500, 500), 'white')
        image.save(tmp, format='JPEG')
        tmp.seek(0)
        tmp_file = open(tmp.name, 'rb')

        self.profile.avatar.save('temp_image.jpg', tmp_file)

    self.profile.save()
    resized_image = Image.open(self.profile.avatar.path)

    self.assertLessEqual(resized_image.width, 300)
    self.assertLessEqual(resized_image.height, 300)

    resized_image.close()
    os.remove(self.profile.avatar.path)
    tmp_file.close()

