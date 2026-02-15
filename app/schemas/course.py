from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    code: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    title: str = None
    code: str = None

class Course(CourseBase):
    id: int
    