from sqlalchemy import Column, String, UUID, DateTime, Time, ForeignKey, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class OldLocation(Base):
    __tablename__ = 't_mst_tmp_lokasi'
    id = Column(String, primary_key=True)
    nama_tmp_lokasi = Column(String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class OldWorship(Base):
    __tablename__ = 't_mst_jenis_staff'
    id = Column(String, primary_key=True)
    nama_jenis_staff = Column(String)
    masuk = Column(DateTime)
    keluar = Column(DateTime)
    created_date = Column(DateTime)
    last_update = Column(DateTime)
    id_tmp_lokasi = Column(String, ForeignKey('t_mst_tmp_lokasi.id'))
    location = relationship(OldLocation, backref='oldworship')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# ========================== NEW MODELS ==========================

class NewLocation(Base):
    __tablename__ = 'master_location'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class NewWorship(Base):
    __tablename__ = 'management_managementofworship'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    type = Column(Integer)
    status = Column(Boolean)
    qrcode = Column(String)
    location_id = Column(UUID(as_uuid=True), ForeignKey('master_location.id'), nullable=True)
    pendeta_id = Column(UUID(as_uuid=True), ForeignKey('master_master.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class NewMaster(Base):
    __tablename__ = 'master_master'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    full_name = Column(String)
    gender = Column(Integer)
    address = Column(String)
    personal_identity = Column(String)
    blood_type = Column(Integer)
    marital_status = Column(Integer)
    profile_photo = Column(String)
    location_id = Column(UUID(as_uuid=True), ForeignKey('master_location.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('auth_user.id'))
    phone_number = Column(String)
    nonstructural_id = Column(UUID(as_uuid=True), ForeignKey('structural_nonstructural.id'))
    date_of_birth = Column(DateTime)
    date_of_death = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}