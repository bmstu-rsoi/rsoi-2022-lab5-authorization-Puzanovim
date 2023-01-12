import asyncio
import logging
import os
from asyncio import Task

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from gateway_system.auth.auth import authenticate_user, authenticated_users_db, create_access_token
from gateway_system.auth.schemas import Token
from gateway_system.exceptions import ServiceNotAvailableError
from gateway_system.queue_processor import QUEUE, queue_processor
from gateway_system.routers import router

from gateway_system import cancel_and_stop_task

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router, prefix='/api/v1', tags=['Gateway API'])

queue_task: Task


@app.post("/oauth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(authenticated_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health():
    return None


@app.on_event('startup')
async def startup_event() -> None:
    global queue_task
    queue_task = asyncio.create_task(queue_processor(QUEUE))
    logger.info('Queue processor is started')


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await cancel_and_stop_task(queue_task)
    logger.info('Queue processor is stopped')


@app.exception_handler(ServiceNotAvailableError)
async def not_available_exception_handler(request: Request, exc: ServiceNotAvailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={'message': 'Bonus Service unavailable'},
    )


if __name__ == "__main__":
    port = os.environ.get('PORT')
    if port is None:
        port = 8080

    uvicorn.run(app, host="0.0.0.0", port=int(port))
