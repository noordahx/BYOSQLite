import unittest
import subprocess 

class DatabaseTest(unittest.TestCase):
    def run_script(self, commands):
        input_str = '\n'.join(commands) + '\n'
        process = subprocess.Popen(
                "./db", 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
        )
        stdout_data, _ = process.communicate(input=input_str.encode())

        output_lines = stdout_data.decode().splitlines()
        return output_lines
        

    def test_inserts_and_retrieves_row(self):
        result = self.run_script([
            "insert 1 user1 person1@example.com",
            "select",
            ".exit",
        ])
        expected_result = [
                "db > Executed.",
                "db > (1, user1, person1@example.com)",
                "Executed.",
                "db > ",
        ]
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()

