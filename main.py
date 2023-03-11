import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
import mysql.connector


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        # connect to the database
        self.db = mysql.connector.connect(
            host='utmlogins.cxi3a3hhwnkb.us-west-2.rds.amazonaws.com',
            user='UTMxyz9856',
            password='A7nHQhUuurDs-T2!',
            database='UTMLogins'
        )
        self.cursor = self.db.cursor()

        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.create_button = QPushButton("Create Account")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.create_button)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        # Connect login button to log in function
        self.login_button.clicked.connect(self.login)

        # Connect create button to creat account function
        self.create_button.clicked.connect(self.create)

    def login(self):
        # Here you can check if the login credentials are correct
        # and close the dialog if they are.
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"""This is the Login Information: 
        Username: {username}
        Password: {password} \n
        """)

        # Query database for matching users
        query = f"SELECT * FROM Logins where usernames = '{username}' AND password = '{password}'"
        self.cursor.execute(query)
        user = self.cursor.fetchone()

        if user:
            print(f"Logged in as {username}")
            self.accept()
        else:
            print("Invalid username or password")

    def create(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f""" This is the information that will be created 
        Username: {username}
        Password: {password} \n 
        """)

        # add information to the DB
        sql = "INSERT INTO Logins (usernames, password) VALUES (%s, %s)"
        val = (username, password)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("YOUR ACCOUNT HAS BEEN SAVED")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        print("Login successful!")
    else:
        print("Login canceled.")
