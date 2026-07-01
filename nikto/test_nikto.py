import subprocess
import unittest
import logging
import shutil

logging.basicConfig(filename='test_nikto.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TestNiktoOutput(unittest.TestCase):
    def setUp(self):
        # Проверяем доступность nikto перед запуском теста
        self.nikto_path = shutil.which('nikto')
        if not self.nikto_path:
            self.skipTest("Nikto не установлен. Для установки выполните: "
                          "'sudo apt install nikto' или скачайте с https://github.com/sullo/nikto")

    def test_nikto_output(self):
        try:
            result = subprocess.run(
                [self.nikto_path, '-h', 'https://test-stand.gb.ru/', '-ssl', '-Tuning', '4'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                timeout=120  # Добавляем таймаут на случай зависания
            )

            output = result.stdout + result.stderr
            logging.info("Nikto Output:\n%s", output)

            self.assertIn("0 error(s)", output,
                          "В выводе nikto обнаружены ошибки. Полный вывод:\n" + output[:1000] + "...")
            logging.info("Тест пройден: ошибки не обнаружены")

        except subprocess.TimeoutExpired:
            error_msg = "Nikto выполнение превысило таймаут"
            logging.error(error_msg)
            self.fail(error_msg)
        except subprocess.CalledProcessError as e:
            error_msg = f"Ошибка выполнения nikto (код {e.returncode}):\n{e.stderr}"
            logging.error(error_msg)
            self.fail(error_msg)
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            logging.exception(error_msg)
            self.fail(error_msg)


if __name__ == '__main__':
    unittest.main()