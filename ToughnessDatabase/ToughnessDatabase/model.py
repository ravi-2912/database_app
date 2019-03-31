import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# configuration
Base = declarative_base()
#DBURI = "postgresql://ravi_:ravi_@localhost:5432/sportsitems"
DBURI = "sqlite:///sportsitems.db?check_same_thread=False"

# main function
def main():
    engine = create_engine(DBURI)
    Base.metadata.create_all(engine)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    prj_name = Column(String(250), nullable=False)
    prj_no = Column(String(32), index=True, unique=True)
    region_prj_no = Column(String(32), index=True, unique=True)
    owner = Column(String(250))
    operator = Column(String(250))
    country = Column(String(80))
    state = Column(String(80))
    city = Column(String(80))

class Pipeine(Base):
    __tablename__ = "pipelines"
    id = Column(Integer, primary_key=True)
    pipe_name = Column(String(250))
# Database crud operation class
class CRUD:
    def __init__(self):
        engine = create_engine(DBURI, echo=True)
        Base.metadata.bind = engine
        DBsession = sessionmaker(bind=engine)
        self.session = DBsession()

    def new_prj(self, project):
        newprj = Project(project.name, project.no, project.region_no,
                         project.owner, project.operator,
                         project.country, project.state, project.city)
        self.session.add(newprj)
        self.session.commit()
        project = self.session.query(Project)\
                    .order_by(Project.id.desc())\
                    .first()
        return project.id

    def get_prj(self, name="", no="", reg_no="",
                owner="", operator="", country="", 
                st="", city="", all_items=True):
        querry_obj = self.session.query(Project)
        f_obj = ""
        if name:
            f_obj = querry_obj.filter_by(prj_name=name)
        if no:
            f_obj = querry_obj.filter_by(prj_no=no)
        if reg_no:
            f_obj = querry_obj.filter_by(region_prj_no=reg_no)

        # TODO: add other criteria to filter_by

        if all_items:
            return f_obj.all()
        else: return f_obj.first()
        



