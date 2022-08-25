import os

BIG_TITLE_FILENAME = "title.txt"
BIG_TITLE_PATH = os.path.join(os.path.dirname(__file__), BIG_TITLE_FILENAME)
with open(BIG_TITLE_PATH, 'r') as f:
    BIG_TITLE = f.read()

TITLE = "Password Manager with PSI"

WELCOME_MSG = "Welcome to Password Manager with PSI.\n"

NOT_MATCHING_PASSWORD_MSG = "Passwords don't match. Please enter passwords again."

SELECT_OPTS_MSG = "Please select an option:\n"

LOGIN_OPTS_MSG = SELECT_OPTS_MSG + "\t1. Sign-up\n" \
                                   "\t2. Sign-in\n" \
                                   "\t3. Quit\n"

MAIN_OPTS_MSG = SELECT_OPTS_MSG + "\t1. Add login details\n" \
                                  "\t2. Edit login details\n" \
                                  "\t3. Delete login details\n" \
                                  "\t4. Retrieve login details\n" \
                                  "\t5. Check login details leakage\n" \
                                  "\t6. Retrieve all login sites\n" \
                                  "\t7. Log-out\n" \
                                  "\t8. Quit\n"

SITE_MSG = "Site: "
USERNAME_MSG = "Username: "
PASSWORD_MSG = "Password: "
REPEAT_PASSWORD_MSG = "Repeat-Password: "

LEAKAGE_MSG = "Your passwords for the following login sites are leaked!"

RETRIEVED_INFO_MSG = "Retrieved information:"

PASSWORD_COPY_MSG = "Password copied to clipboard."

DELETE_COMPLETED_MSG = " is deleted successfully from your saved login details."

GOODBYE_MSG = "Goodbye!"

INVALID_INPUT_MSG = "Invalid input"

ERROR_PREFIX = "Error: "

PRESS_ENTER_MSG = "Press ENTER to continue."
