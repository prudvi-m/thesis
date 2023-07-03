import random
from django.test import TestCase
from .models import File_Results


class ZipfileModelUnitTestCase(TestCase):
    def setUp(self):
        self.zipfile = File_Results.objects.create(
            id_number=random.randint(10000, 99999),
            user_name='Bob',
            db_name='Smith',
            email='bob.smith@test.com',
            is_build_succeeded='Computer Science',
            dotnet_version=3.92
        )

    def test_student_model(self):
        data = self.zipfile
        self.assertIsInstance(data, File_Results)
