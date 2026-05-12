from fastapi import FastAPI, Query
from rag_queue.client.rq_client import queue
from rag_queue.queues.worker import process_query
app = FastAPI()


@app.get("/")
def root():
    return {"status":"server is up and running "}
@app.post("/chat")
def chat(
        query: str =Query(...,description="The query to process")
):
   job = queue.enqueue(process_query, query)
   
   return {"status":"queued", "job_id": job.id}
@app.get("/result")
def get_result(
        job_id: str = Query(..., description="The ID of the job to retrieve results for")
):
    job = queue.fetch_job(job_id)
    result=job.return_value()

    return{"result": result} 
