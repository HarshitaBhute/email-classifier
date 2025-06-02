from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from masking import mask_email

app = FastAPI()

model = joblib.load("email_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class EmailBody(BaseModel):
    input_email_body: str

@app.post("/classify")
def classify_email(request: EmailBody):
    email = request.input_email_body
    masked_email, entities = mask_email(email)
    email_vec = vectorizer.transform([masked_email])
    prediction = model.predict(email_vec)[0]
    
    return {
        "input_email_body": email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": prediction
    }
