from connection import use_session
from models import *
from datetime import datetime
from uuid import uuid4
from typing import List

@use_session
def insert_locations(mssql_session, postgres_session):
    locations: List[OldLocation] = mssql_session.query(OldLocation).all()
    for location in locations:
        new=NewLocation(id=uuid4(), name=location.nama_tmp_lokasi, created_at=datetime.now(), updated_at=datetime.now())
        postgres_session.add(new)
        postgres_session.commit()

@use_session
def insert_worship(mssql_session, postgres_session):
    worship: List[OldWorship] = mssql_session.query(OldWorship).all()
    for worship in worship:
        location_id = postgres_session.query(NewLocation).filter(NewLocation.name == worship.location.nama_tmp_lokasi).first().id
        new=NewWorship(
            id=uuid4(),
            name=worship.nama_jenis_staff,
            start_time=worship.masuk,
            end_time=worship.keluar,
            type=1,
            status=True,
            location_id=location_id,
            pendeta_id=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        postgres_session.add(new)
        postgres_session.commit()
    
# insert_locations()
# insert_worship()


@use_session
def get_master(mssql_session, postgres_session):
    masters = postgres_session.query(NewMaster).all()
    for master in masters:
        print(master.to_dict())
get_master()