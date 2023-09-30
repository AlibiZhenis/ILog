import unittest
from Ilog import ILog
import os


class LogComponentTests(unittest.TestCase):
    TEST_LOG_DIRECTORY = "TestLogs"
    NUM_LOG_MESSAGES = 10000

    def setUp(self):
        # Delete the test log directory if it exists
        self.test_log_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.TEST_LOG_DIRECTORY)
        if os.path.exists(self.test_log_directory):
            for file in os.listdir(self.test_log_directory):
                file_path = os.path.join(self.test_log_directory, file)
                os.remove(file_path)
            os.rmdir(self.test_log_directory)

    def test_stop_with_wait_for_completion_true(self):
        # Arrange
        log_component = ILog(log_directory=self.TEST_LOG_DIRECTORY)
        log_message = "Test"

        # Act
        for _ in range(self.NUM_LOG_MESSAGES):
            log_component.write(log_message)
        log_component.stop(wait_for_completion=True)

        # Assert
        log_files = os.listdir(self.TEST_LOG_DIRECTORY)
        self.assertEqual(len(log_files), 1)
        log_file_path = os.path.join(self.TEST_LOG_DIRECTORY, log_files[0])
        with open(log_file_path, "r+") as file:
            log_content = file.read()
            self.assertEqual(len(log_content), len(log_message) * self.NUM_LOG_MESSAGES)
        open(log_file_path, 'w').close()

    def test_stop_with_wait_for_completion_false(self):
        # Arrange
        log_component = ILog(log_directory=self.TEST_LOG_DIRECTORY)
        log_message = "Test"

        # Act
        for _ in range(self.NUM_LOG_MESSAGES):
            log_component.write(log_message)
        log_component.stop(wait_for_completion=False)

        # Assert
        log_files = os.listdir(self.test_log_directory)
        self.assertEqual(len(log_files), 1)
        log_file_path = os.path.join(self.TEST_LOG_DIRECTORY, log_files[0])
        with open(log_file_path, "r") as file:
            log_content = file.read()
            self.assertNotEqual(len(log_content), len(log_message) * self.NUM_LOG_MESSAGES)
        open(log_file_path, 'w').close()


if __name__ == "__main__":
    unittest.main()
