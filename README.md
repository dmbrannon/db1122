# Local Setup
You must install FastAPI and its dependencies to use this project.
```
pip install "fastapi[all]"
```
You can run the development server with the following: `uvicorn main:app --reload`
You can now view the app by visiting `http://localhost:8000/`. 
You can view the interactive documentation by going to `http://localhost:8000/docs`.

# Test Case Results
## Add Tool
<img width="849" alt="image" src="https://user-images.githubusercontent.com/52638822/202774478-74f48f6f-b940-4609-ba76-38094f9fc3dc.png">

## Update Daily Charge
<img width="862" alt="image" src="https://user-images.githubusercontent.com/52638822/202775785-570579b1-f671-4a65-afbc-d25440ab48c3.png">

## Case 1
<img width="850" alt="image" src="https://user-images.githubusercontent.com/52638822/202774170-4504e0f6-098e-465d-b293-f2df64a50031.png">

## Case 2

## Case 3

## Case 4

## Case 5

# Questions
- In Tests, LADL doesn't exist; can we just return "Tool Doesn't Exist?"
- Used strings to represent dates because of the desired format; would ask Client if we could use more standard date format of YYYY-MM-DD?
- Assumed Holiday pricing took precedence (If a Holiday falls on a weekday and we don't charge for holidays but we DO charge for weekdays, do we want to charge for that day...?)
