from fastapi import FastAPI

from app.api.v1.user import user_router
from app.api.v1.course import course_router
from app.api.v1.enrollment import enrollment_router


app = FastAPI()

app.include_router(user_router)
app.include_router(course_router)
app.include_router(enrollment_router)
