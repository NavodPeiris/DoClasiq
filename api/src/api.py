from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import shutil
from PIL import Image
import fitz
import io
from transformers import LayoutLMv2Processor, LayoutLMv2ForSequenceClassification
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn.functional as F
from utils import extract_info

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# getting cached models from /models folder in docker container
processor = LayoutLMv2Processor.from_pretrained("./models/layoutlmv2-base/")
model = LayoutLMv2ForSequenceClassification.from_pretrained("./models/layoutlmv2-classifier/")

label2id = {"inventory_monthly": 0, "inventory_monthly_category": 1, "invoices": 2, "purchase_orders": 3, "shipping_orders": 4}
id2label = {v: k for k, v in label2id.items()}


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


# Route to serve the web page
@app.post("/api/classify")
def list_files(file: UploadFile = File(...)):   
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        if file.content_type.lower() != "application/pdf":
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF files are allowed.")

        raw_text = ""

        with fitz.open(file_location) as doc:
            for page in doc:
                raw_text += page.get_text()
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            del pix  # Free pixmap memory

        with Image.open(io.BytesIO(img_bytes)) as img:
            image = img.convert("RGB").copy()

        encoding = processor(image, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
        outputs = model(**encoding)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)

        # get entropy of softmax output
        entropy = -torch.sum(probs * torch.log(probs + 1e-12), dim=1).item()

        print("entropy: ", entropy)

        predicted_class_id = logits.argmax(dim=1).item()
        classified_output = model.config.id2label[predicted_class_id]

        # if entropy value is lower than threshold, model is more confident about the classified class
        # threshold entropy was decided through testing
        if entropy < 0.15:
            print(f"Predicted class: {classified_output}")
            extracted_data = extract_info(raw_text, classified_output)
        else:
            # unknown documents give high entropy
            classified_output = "unknown"
            extracted_data = []
            print(f"Predicted class: {classified_output}")

        # release memory
        del image, encoding, outputs, logits, probs, raw_text, file
        torch.cuda.empty_cache()

        return {"classified_output": classified_output, "extracted_data": extracted_data}

    finally:
        if os.path.exists(file_location):
            os.remove(file_location)