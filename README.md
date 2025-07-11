## DoClasiq

A document classifier with ability to both classify and extract structured information from company documents

Dataset used: [Company Documents Dataset](https://www.kaggle.com/datasets/navodpeiris/company-documents-dataset)

Fully trained model is available on Hugging Face. no need to run training. just follow section 2 to run the app.

model link: [navodPeiris/layoutlmv2-document-classifier](https://huggingface.co/navodPeiris/layoutlmv2-document-classifier)

### 1. Run Training (Optional)

#### Run training:
Run this notebook on kaggle (use P100 gpu not T4x2): [finetune_doclasiq_model](https://www.kaggle.com/code/navodpeiris/finetune-doclasiq-model)

#### Visualize training details(loss, accuracy etc):
```
pip install tensorboard
cd train
tensorboard --logdir logs
```

### 2. Run the app
```
docker-compose up -d .
```

This will download the prebuilt images and start the UI and APIs.

### 3. How to use the app

Use test documents in test_docs folder to test  

![how to use app](doclasiq_use.gif)

### 4. Performance

Model Performance:

![model_performance](tensorboard_view.png)

Model has acheived **0.0008 evaluation loss** and **1.0 evaluation accuracy**

### 5. design choices

#### why streamlit for UI?

Streamlit is easy to use and integrate well with any python workload related to ML

#### why use FastAPI with Uvicorn and Gunicorn 

FastAPI is high-performance framework for API development and widely used.  
Gunicorn handles multiple worker processes, restarts.  
Uvicorn enables FastAPI’s async features as it is an async web server.  

```
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8001", "api:app"]
```

This command plugs Uvicorn into Gunicorn as a worker and here it spawns 4 workers to handle requests parallely. This is great for scalability.

#### why Docker?

It makes running this solution easy and seamless. works perfectly across platforms.

### 6. How document classification work


### 7. How data extraction works

