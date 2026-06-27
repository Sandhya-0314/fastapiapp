
from sqlalchemy import Column,Integer,String,Enum,ForeignKey,relationship
from models.company import Company
from database import Base,engine,SessionalLocal

#Base = declarative_base()

class Job(Base):
    __tablename__="jobs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String)
    Salary=Column(Integer)
    company_id=Column(Integer,Foreign_key=True("companies:id"))
    company=relationship("Company",back_populates="jobs")
