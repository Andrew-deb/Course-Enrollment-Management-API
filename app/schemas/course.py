from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    code: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    