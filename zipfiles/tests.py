import random
from django.test import TestCase
from .models import Zipfile


class ZipfileModelUnitTestCase(TestCase):
    def setUp(self):
        self.zipfile = Zipfile.objects.create(
            id_number=random.randint(10000, 99999),
            user_name='Bob',
            db_name='Smith',
            email='bob.smith@test.com',
            is_build_succeeded='Computer Science',
            gpa=3.92
        )

    def test_student_model(self):
        data = self.zipfile
        self.assertIsInstance(data, Zipfile)
