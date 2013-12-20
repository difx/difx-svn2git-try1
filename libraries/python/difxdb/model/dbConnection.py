# -*- coding: utf-8 -*-
#===========================================================================
# SVN properties (DO NOT CHANGE)
#
# $Id$
# $HeadURL$
# $LastChangedRevision$
# $Author$
# $LastChangedDate$
#
#============================================================================
__author__="Helge Rottmann"

from sqlalchemy import *
from sqlalchemy.orm import *
from difxdb.model.model import *

class Schema(object):
    """Describes the schema and mappers used by  SQLAlchemy """
    
    def __init__(self, connection):
        
        connStr = connection.getConnectionString()
        self.engine__ = create_engine(connStr, echo=connection.echo) 
        self.connection__ = self.engine__.connect()
    
        self.metadata__ = MetaData(self.engine__)
     
        
        self.loadSchema()
        self.createMappers()
    

    def _get_session(self):
        return scoped_session(sessionmaker(bind=self.engine__))
    session = property(_get_session)
    

    def loadSchema(self):
        
        self.experimentTable = Table("Experiment", self.metadata__, autoload=True)
        self.experimentStatusTable = Table("ExperimentStatus", self.metadata__, autoload=True)
        self.experimentTypeTable = Table("ExperimentType", self.metadata__, autoload=True)
        self.slotTable = Table("Slot", self.metadata__, autoload=True)
        self.moduleTable = Table("Module", self.metadata__, autoload=True)
        self.jobTable = Table("Job", self.metadata__, autoload=True)
        self.jobStatusTable = Table("JobStatus", self.metadata__, autoload=True)
        self.passTable = Table("Pass", self.metadata__, autoload=True)
        self.passTypeTable = Table("PassType", self.metadata__, autoload=True)
        self.versionHistoryTable = Table("VersionHistory", self.metadata__, autoload=True)
        self.userTable = Table("User", self.metadata__, autoload=True)
        
        #association table for many-to-many Experiment/Module relation 
        self.experimentModuleTable = Table('ExperimentAndModule', self.metadata__, autoload=True)
        self.experimentAndTypeTable = Table('ExperimentAndType', self.metadata__, autoload=True)
  
        

        
    def createSchema(self):

        #self.slotTable = Table('Slot', self.metadata__,
        #    Column('id', Integer, primary_key=True),
        #    Column('location', String(20)))

        #self.metadata__.create_all(self.engine__)
        pass

    def createMappers(self):
        
        clear_mappers()
        mapper(Queue, self.jobTable, properties={'Pass':relation(Pass, uselist=False),'status':relation(JobStatus, uselist=False)})
        mapper(Job, self.jobTable, properties={'status':relation(JobStatus, uselist=False)})
        mapper(JobStatus, self.jobStatusTable)
        
        mapper(Pass, self.passTable, properties={'experiment':relation(Experiment, uselist=False), 'type':relation(PassType, uselist=False)})
        mapper(PassType, self.passTypeTable)
        mapper(ExperimentStatus, self.experimentStatusTable)
       # mapper(Experiment, self.experimentTable,properties={'status':relation(ExperimentStatus, uselist = False)})
        mapper(Experiment, self.experimentTable,properties={'status':relation(ExperimentStatus, uselist=False), \
            'user':relation(User, primaryjoin=self.experimentTable.c.userID==self.userTable.c.id, uselist = False), \
            'releasedByUser':relation(User, primaryjoin=self.experimentTable.c.releasedByUserID==self.userTable.c.id, uselist = False), \
            'types':relation(ExperimentType, secondary=self.experimentAndTypeTable, primaryjoin=self.experimentAndTypeTable.c.experimentID==self.experimentTable.c.id, secondaryjoin=self.experimentAndTypeTable.c.experimentTypeID==self.experimentTypeTable.c.id, foreign_keys = [self.experimentAndTypeTable.c.experimentID, self.experimentAndTypeTable.c.experimentTypeID])}) 
	mapper(Module, self.moduleTable, properties={'experiments': relation(Experiment, secondary=self.experimentModuleTable, primaryjoin=self.experimentModuleTable.c.moduleID==self.moduleTable.c.id, secondaryjoin=self.experimentModuleTable.c.experimentID==self.experimentTable.c.id, foreign_keys = [self.experimentModuleTable.c.experimentID, self.experimentModuleTable.c.moduleID], backref=backref('modules'))}) 
	mapper(Slot, self.slotTable,properties={'module': relation(Module, uselist = False, backref=backref('slot', uselist=False))})
        mapper(VersionHistory, self.versionHistoryTable)
        mapper(User, self.userTable)
        mapper(ExperimentType, self.experimentTypeTable)

class Connection(object):
    
    def __init__(self, difxdbConfig = None):
        
        self.type = ""
        self.server = ""
        self.port = ""
        self.user = ""
        self.password = ""
        self.database = ""
        
        # if a configuration object was passed
        # use it to fill the connection parameters
        if difxdbConfig is not None:
            self.type = difxdbConfig.get("Database", "type")
            self.server = difxdbConfig.get("Database", "server")
            self.port = difxdbConfig.get("Database", "port")
            self.user = difxdbConfig.get("Database", "user")
            self.password = difxdbConfig.get("Database", "password")
            self.database = difxdbConfig.get("Database", "database")
        
        self.echo = False
        
    def getConnectionString(self):
        
        try:
            self._validate()
        except:
            raise
            return("")
        
        str = self.type + "://" + self.user + ":" + self.password + "@" + self.server + ":" + self.port + "/" + self.database
        
        return(str)
    
    def _validate(self):
        
        if self.type == "":
            raise  ConnectionParamError("Database type has not been specified")
        if self.server == "":
            raise  ConnectionParamError("Database server has not been specified")
        if self.port == "":
            raise  ConnectionParamError("Database port has not been specified")
        if self.user == "":
            raise  ConnectionParamError("Database user has not been specified")
        if self.password == "":
            raise  ConnectionParamError("Database password has not been specified")
        if self.database == "":
            raise  ConnectionParamError("Database has not been specified")
       

        
class ConnectionParamError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
