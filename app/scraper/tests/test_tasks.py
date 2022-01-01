from app.scraper import tasks, zaim
from django.test import TestCase
from django.conf import settings
import tempfile

class TestTasks(TestCase):

  def test_scrape_succeed(self):
    result = tasks.scrape(settings.ZAIM_USER, settings.ZAIM_PASSWORD, "2021", "11")
    self.assertTrue(type(result) is dict)

  def test_scrape_fail(self):
    with self.assertRaises(zaim.ZaimCrawlerException):
      tasks.scrape("wrong_user@gmail.com", "wrong_password", "2021", "11")

  def test_upload_file_succeed(self):
    outfile_path = "upload_test.txt"
    with tempfile.NamedTemporaryFile(mode="w") as temp:
      temp.write("Testing upload to Google Drive.")
      temp.flush()
      file_id = tasks.upload_file(temp.name, 'text/plain', outfile_path, ['1zfImy-dUKtcNJM0Rpg0iM7LwV2_az-Vi'])
    self.assertTrue(type(file_id) is str)