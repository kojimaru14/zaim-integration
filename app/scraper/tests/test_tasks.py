from app.scraper import tasks
from django.test import TestCase
from django.conf import settings
import os

class TestTasks(TestCase):

  def test_add_task(self):
    result = tasks.add(6,4)
    self.assertEqual(result, 10)

  def test_scrape_succeed(self):
    result = tasks.scrape_and_upload(settings.ZAIM_USER, settings.ZAIM_PASSWORD, "2021", "11")
    self.assertEqual(result, 1)

  def test_scrape_fail(self):
    result = tasks.scrape_and_upload("wrong_user@gmail.com", "wrong_password", "2021", "11")
    self.assertEqual(result, 0)

  def test_upload_file_succeed(self):
    test_file = os.path.join(settings.BASE_DIR, "README.md")
    result = tasks.upload_file(test_file, 'text/plain', "README.md", ['1zfImy-dUKtcNJM0Rpg0iM7LwV2_az-Vi'])
    self.assertEqual(result, True)