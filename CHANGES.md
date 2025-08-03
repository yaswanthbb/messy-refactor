## 🔧 What I Fixed and Why

- **It had SQL queries written as a string** — I changed them to use `?` parameters to avoid SQL injection.
- **Passwords were saved as plain text** — I used `Werkzeug.security` to hash the passwords before saving.
- **All the code was in one file (`app.py`)** — I moved the code into multiple files like `routes.py`, `models.py`, and `utils.py` to make it cleaner and easier to understand.
- **It didn’t check if required fields were missing** — I added checks for `name`, `email`, and `password` in the input data.
- **Error messages were just plain strings** — I returned proper JSON messages with correct HTTP status codes like 200, 400, and 404.
- **Everything was returned as text** — I changed it to return data as JSON so it’s easier to use with frontend.
- **There were no tests** — I added basic tests using `pytest` to make sure key endpoints like `/users` and `/login` work correctly.

## 🤖 AI Used For : 

- I dont know much about How to write test cases so I toke help from ChatGpt to write test cases.
- I learnt how to improve quality, security, and maintainability from ChatGpt.
