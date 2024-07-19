import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.products.router import products_router, categories_router
from dotenv import load_dotenv

from src.users.router import users_router

app = FastAPI()

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(users_router)

origins = [
    f"http://{os.getenv('HOST')}:{int(os.getenv('PORT'))}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv('HOST'), port=8001)