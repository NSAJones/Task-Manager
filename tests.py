import unittest
import db

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = db.Database()

    def test_login(self):
        """Test user login"""
        
        username,password="foo","bar"
        
        # Create user
        user_created = self.db.create_user(username,password)
        self.assertTrue(user_created,"User not created")

        # Login user
        sessionID = self.db.validate_user(username,password)
        test_user = self.db.sessionID(sessionID)

        self.assertEqual(username,test_user,"Incorrect sessionID")

        # False session id
        false_user = self.db.sessionID("abdc")
        self.assertIsNone(false_user)

    def test_tasks(self):
        """Test task creation"""
        username,password="foo","bar"

        # Create user + login
        self.db.create_user(username,password)
        sessionID = self.db.validate_user(username,password)

        # Create task
        listID = self.db.create_todolist(sessionID)

        # Check creation of task
        tasks = self.db.get_todolists(username)
        self.assertTrue((tasks[0][1] == "cool task"))

        # Update task
        task_dict = {
            "name":"cool task",
            "task_list":[{"name":"first task",
                          "description":"this is the 1st task"}]
        }
        self.db.update_task(listID,task_dict)

        # Check update happened
        response_list = self.db.get_todolist(listID)
        
        
        self.assertEqual(response_list["todolist"][1],"cool task")
        self.assertEqual(response_list["tasks"][0][2],"first task")


if __name__ == "__main__":
    unittest.main()