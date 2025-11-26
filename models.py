from sqlalchemy import Column, Integer, String, Date, Float
from db import Base


class JournalData(Base):
    __tablename__ = "journal_data"

    _id = Column(String, primary_key=True)
    Journal_Name = Column(String)
    Special_Issue_Name = Column(String)
    Journal_Website = Column(String)
    Special_Issue_keywords = Column(String)
    Submission_Url = Column(String)
    Journal_Username = Column(String)
    Journal_Password = Column(String)
    Journal_Login_Status = Column(String)
    Slots_Availble = Column(String)
    ISSN_No = Column(String)
    Index = Column(String)
    SI_Open = Column(String)
    Managing_Guest_Editor = Column(String)
    Journal_Short_Name = Column(String)
    IF = Column(String)              # if impact factor is float, change to Float
    Publisher = Column(String)
    Login_Received = Column(String)
    Anna_University_A1_A2_Both = Column(String)
    Login_Received_Date = Column(Date)  # change to Date if needed
    Deadline = Column(Date)             # change to Date if needed
    Editorial_Manager_Submission_System = Column(String)
    JCR_Ranking = Column(String)
    UAE_Ranking = Column(String)
    LetPub = Column(String)
    SCIMAGO_Ranking = Column(String)
    Special_Issue_Supplement_Issue_regular_issue = Column(String)
    APC_Fee = Column(String, nullable=True)
    SI_Received_Person = Column(String)
    Assigned_To = Column(String)
    SI_Status_Updated_Date = Column(Date)
    Login_Status_Last_Updated_Date = Column(Date)
    Deadline_Last_Updated_Date = Column(Date)
    Updated_Date = Column(Date)
    No_of_used = Column(Integer)
    WO_Slots = Column(Integer)
    No_of_Paper_Processed = Column(Integer)
    Date_of_Editorial_Sent = Column(Date)
    Remarks = Column(String)
    Smooth_Average_Very_tough = Column(String)
    Editorial_Sent = Column(String)


class AssosiateData(Base):
    __tablename__ = "Assosiate_data"

    _id = Column(String, primary_key=True, index=True)

    Journal_Name = Column(String)
    Journal_Website = Column(String)
    Special_Issue_keywords = Column(String)

    Submission_Url = Column(String)
    Journal_Username = Column(String)
    Journal_Password = Column(String)
    Journal_Login_Status = Column(String)

    Index = Column(String)
    Assigned_To = Column(String)
    Remarks = Column(String)
    Editor_Name = Column(String)

    APC = Column(String) 