from .test_setup import TestSetUp

class TestViews(TestSetUp):

  def test_user_cannot_run_task(self):
    res = self.client.get(self.run_task_url)
    self.assertEqual(res.status_code, 401)

  # def test_user_can_run_task(self):
  #   res = self.client.get(self.run_task_url)
  #   self.assertEqual(res.status_code, 200)