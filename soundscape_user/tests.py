# from django.test import TestCase
from django.test import TestCase
from soundscape_user.models import SoundFileUser, SoundDescriptor


class SoundFileUserModelTest(TestCase):

    def setUp(self):
        self.sound_descriptor = SoundDescriptor.objects.create(descriptor="Bird Song")
        self.sound_file_user = SoundFileUser.objects.create(
            user_name="Test User",
            sound_descriptor=self.sound_descriptor.descriptor,
            s3_file_name="bird_song.mp3",
            latitude=40.7128,
            longitude=-74.0060,
        )

    def test_sound_file_user_creation(self):
        """Test that a SoundFileUser instance is created correctly"""
        sound_file_user = self.sound_file_user
        self.assertIsInstance(sound_file_user, SoundFileUser)
        self.assertEqual(sound_file_user.user_name, "Test User")
        self.assertEqual(sound_file_user.sound_descriptor, "Bird Song")
        self.assertEqual(sound_file_user.s3_file_name, "bird_song.mp3")
        self.assertAlmostEqual(sound_file_user.latitude, 40.7128)
        self.assertAlmostEqual(sound_file_user.longitude, -74.0060)
        self.assertIsNotNone(sound_file_user.created_at)

    def test_sound_file_user_str_representation(self):
        """Test the string representation of SoundFileUser"""
        self.assertEqual(str(self.sound_file_user), "Test User - bird_song.mp3")


class SoundDescriptorModelTest(TestCase):

    def setUp(self):
        self.sound_descriptor = SoundDescriptor.objects.create(descriptor="Rain")

    def test_sound_descriptor_creation(self):
        """Test that a SoundDescriptor instance is created correctly"""
        sound_descriptor = self.sound_descriptor
        self.assertIsInstance(sound_descriptor, SoundDescriptor)
        self.assertEqual(sound_descriptor.descriptor, "Rain")
        self.assertIsNotNone(sound_descriptor.created_at)

    def test_sound_descriptor_str_representation(self):
        """Test the string representation of SoundDescriptor"""
        self.assertEqual(str(self.sound_descriptor), "Rain")
