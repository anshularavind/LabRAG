# LabRAG

AI platform that acts as a basic biology/biotech laboratory assistant that allows users to ask questions about a particular lab procedure and modify lab procedures based on available equipment. All sources are thoughtfully cited, with the author and the university/laboratory that created the base protocol, making LabRAG a project that maintains the highest standard of ethical and responsible AI. 

To run:

Install all necessary requirements
```
pip install -r requirements.txt
```
Set up environment variables.

Create a new folder called db in the backend.

Then run these commands (to start the backend)
```
cd backend
cd src
uvicorn main:app --reload
```

Then, to get the frontend running
```
cd frontend
npm start
```
