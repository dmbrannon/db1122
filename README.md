# Local Setup
You must install FastAPI and its dependencies to use this project.
```
pip install "fastapi[all]"
```
You can run the development server with the following: `uvicorn main:app --reload`
You can now view the app by visiting `http://localhost:8000/`. 
You can view the interactive documentation by going to `http://localhost:8000/docs`.

## Questions
- In Tests, LADL doesn't exist; can we just return "Tool Doesn't Exist?"
- Used strings to represent dates because of the desired format; would ask Client if we could use more standard date format of YYYY-MM-DD?
- Assumed Holiday pricing took precedence (If a Holiday falls on a weekday and we don't charge for holidays but we DO charge for weekdays, do we want to charge for that day...?)