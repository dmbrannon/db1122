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
<img width="868" alt="image" src="https://user-images.githubusercontent.com/52638822/202776290-7d39173a-d4af-44ab-b33a-a10df7d6e613.png">

## Case 3
<img width="857" alt="image" src="https://user-images.githubusercontent.com/52638822/202776596-053e3b7f-6964-43c8-b0ba-36b44814950a.png">

## Case 4
<img width="859" alt="image" src="https://user-images.githubusercontent.com/52638822/202776951-9811b73d-5948-498a-b3dc-e310b678ea6b.png">

## Case 5
<img width="859" alt="image" src="https://user-images.githubusercontent.com/52638822/202777356-f920761a-08b8-43b3-a40d-d7342adce906.png">

## Case 6
<img width="860" alt="image" src="https://user-images.githubusercontent.com/52638822/202778300-6eaf5f77-1559-4223-a2a3-82d61f9bf05d.png">


# Questions
- In Tests, LADL doesn't exist; can we just return "Tool Doesn't Exist?"
- Used strings to represent dates because of the desired format; would ask Client if we could use more standard date format of YYYY-MM-DD?
- Assumed Holiday pricing took precedence (If a Holiday falls on a weekday and we don't charge for holidays but we DO charge for weekdays, do we want to charge for that day...?)
