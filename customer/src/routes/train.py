from fastapi import APIRouter

train_router = APIRouter(
    tags=["train"]
)

class TrainManager():
    def __init__(self):
        self.status = "False"

    def checking(self):
        return self.status

    def use_gpu(self):
        self.status = "True"
        return self.status
    
    def done_gpu(self):
        self.status = "False"
        return self.status

train_manager = TrainManager()
