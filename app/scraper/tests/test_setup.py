from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

  def setUp(self):
    self.run_task_url = reverse('zaim:run_task')
    self.list_tasks_url = reverse('zaim:list_tasks')

    return super().setUp()

  def tearDown(self):
    return super().tearDown()
