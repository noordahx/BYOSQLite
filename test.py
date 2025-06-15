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

    def test_prints_error_message_when_table_is_full(self):
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1401)]
        script.append(".exit")
        result = self.run_script(script)
        self.assertEqual(result[-2], 'db > Error: Table full.')

    def test_allows_inserting_strings_that_are_the_maximum_length(self):
        long_username = "a"*32
        long_email = "a"*255
        script = [
                f"insert 1 {long_username} {long_email}",
                "select",
                ".exit",
        ]
        result = self.run_script(script)
        self.assertEqual(result, [
            "db > Executed.",
            f"db > (1, {long_username}, {long_email})",
            "Executed.",
            "db > "
        ])

    def test_prints_error_message_if_strings_are_too_long(self):
        long_username = "a"*33
        long_email = "a"*256
        script = [
                f"insert 1 {long_username} {long_email}",
                "select",
                ".exit",
        ]
        result = self.run_script(script)
        self.assertEqual(result, [
            "db > String is too long.",
            "db > Executed.",
            "db > "
        ])

    def test_prints_an_error_message_if_id_is_negative(self):
        script = [
                "insert -1 nurda nurda@nurda.com",
                "select",
                ".exit"
        ]
        result = self.run_script(script)
        self.assertEqual(result, [
            "db > ID must be positive.",
            "db > Executed.",
            "db > ",
        ])

if __name__ == "__main__":
    unittest.main()

