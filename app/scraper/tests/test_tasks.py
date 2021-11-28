from app.scraper import tasks
from django.test import TestCase
from django.conf import settings

class TestTasks(TestCase):

  def test_add_task(self):
    result = tasks.add(6,4)
    self.assertEqual(result, 10)

  def test_scrape_succeed(self):
    print(settings.ZAIM_USER, settings.ZAIM_PASSWORD)
    result = tasks.scrape_and_upload(settings.ZAIM_USER, settings.ZAIM_PASSWORD, "2021", "08")
    self.assertEqual(result, 1)

  def test_scrape_fail(self):
    result = tasks.scrape_and_upload("wrong_user@gmail.com", "wrong_password", "2021", "11")
    self.assertEqual(result, 0)