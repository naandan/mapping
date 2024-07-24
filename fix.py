import pyodbc
import psycopg
from functools import wraps
from datetime import datetime
import pandas as pd
from uuid import uuid4
from const import *
from utils import *
import pandas as pd
import random
import requests
from datetime import datetime

def get_db_connection():
    sql_server_host = '127.0.0.1,1433'
    sql_server_db = 'eHC'
    sql_server_user = 'sa'
    sql_server_pass = 'Admin#1234'

    sql_server_conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+sql_server_host+';DATABASE='+sql_server_db+';UID='+sql_server_user+';PWD='+sql_server_pass+';TrustServerCertificate=yes;')

    postgres_host = '127.0.0.1'
    postgres_db = 'gkim'
    postgres_user = 'root'
    postgres_pass = 'password'

    postgres_conn = psycopg.connect(f"host='{postgres_host}' dbname='{postgres_db}' user='{postgres_user}' password='{postgres_pass}'")

    return sql_server_conn, postgres_conn

def use_db_connection(func):
    @wraps(func)
    def with_connection(*args, **kwargs):
        sql_server_conn, postgres_conn = get_db_connection()
        try:
            result = func(sql_server_conn, postgres_conn, *args, **kwargs)
        finally:
            sql_server_conn.close()
            postgres_conn.close()
        return result
    return with_connection

def to_df(data, columns, to_dict=False):
    data = formatted(data)
    df = pd.DataFrame(data, columns=columns)
    if to_dict:
        df = df.to_dict(orient='records')[0]
    return df

@use_db_connection
def insert_location(sql_server_conn, postgres_conn, *args, **kwargs):
    sql_server_cursor = sql_server_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    def save(res):
        index = res.name
        postgres_cursor.execute(
            """
            INSERT INTO master_location
            (id, name, created_at, updated_at) 
            VALUES (%s, %s, %s, %s)
            """,
            (uuid4(), res['lokasi'], datetime.now(), datetime.now())
        )
        postgres_conn.commit()
        print(f"{index+1}. {res['lokasi']}")

    locations = sql_server_cursor.execute("SELECT nama_tmp_lokasi AS lokasi FROM t_mst_tmp_lokasi").fetchall()
    column_names = [desc[0] for desc in sql_server_cursor.description]
    locations_df = to_df(locations, column_names)
    locations_df.apply(save, axis=1)

@use_db_connection
def insert_worship(sql_server_conn, postgres_conn, *args, **kwargs):
    sql_server_cursor = sql_server_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    def save(res):
        index = res.name
        location_id = postgres_cursor.execute(f"SELECT id FROM master_location WHERE name = '{res['nama_tmp_lokasi']}'").fetchone()
        location_id = location_id[0] if location_id else None
        postgres_cursor.execute(
            f"""
            INSERT INTO management_managementofworship
            (id, name, start_time, end_time, type, status, qrcode, created_at, updated_at, location_id, pendeta_id, day_worship)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (uuid4(), res['nama_jenis_staff'], res['masuk'], res['keluar'], TypeOfWorship.OFFLINE[0], True, None, get_datetime_type(res['created_date']), get_datetime_type(res['last_update']), location_id, None, 7)
        )
        postgres_conn.commit()
        print(f"{index+1}. {res['nama_jenis_staff']}")

    worship = sql_server_cursor.execute(
            """
            SELECT
                t_mst_jenis_staff.nama_jenis_staff,
                t_mst_jenis_staff.masuk,
                t_mst_jenis_staff.keluar,
                t_mst_jenis_staff.created_date,
                t_mst_jenis_staff.last_update,
                t_mst_tmp_lokasi.nama_tmp_lokasi
            FROM
                t_mst_jenis_staff
            LEFT JOIN
                t_mst_tmp_lokasi ON t_mst_tmp_lokasi.id = t_mst_jenis_staff.id_tmp_lokasi
            
            """
        ).fetchall()
    column_names = [desc[0] for desc in sql_server_cursor.description]
    worship_df = to_df(worship, column_names)
    worship_df.apply(save, axis=1)

@use_db_connection
def insert_master(sql_server_conn, postgres_conn, *args, **kwargs):
    sql_server_cursor = sql_server_conn.cursor()
    postgres_cursor = postgres_conn.cursor()  

    counter = 1

    insertedId = []
    insertedNIK = []
    insertedNoReg = []
    insertedPhone = []

    def save_master(res, counter):
        print(counter, res['nama_depan'])

        if str(res['no_ktp']) in insertedNIK or res['no_ktp'] is None:
            res['no_ktp'] = f"rand-{counter}-ktp"
        insertedNIK.append(res['no_ktp'])

        res['id_golongan_darah'] = 0 if res['id_golongan_darah'] is None else res['id_golongan_darah']
        res['id_marital_status'] = 0 if res['id_marital_status'] is None else res['id_marital_status']
        res['email'] = f"rand-{counter}@gmail.com" if res['email'] is None else res['email']
        res['alamat'] = f"rand-{counter}-alamat" if res['alamat'] is None else res['alamat']

        res['no_reg'] = cleaned_string(res['no_reg'])
        if res['no_reg'] in insertedNoReg or res['no_reg'] is None:
            res['no_reg'] = f"rand-{counter}"
        insertedNoReg.append(res['no_reg'])

        if res['no_hp1'] is not None and res['no_hp1'] in insertedPhone:
            res['no_hp1'] = None
        insertedPhone.append(res['no_hp1'])

        res['password'] = generate_password(res['tgl_lahir'])
        res['tgl_lahir'] = get_datetime_type(res['tgl_lahir'], True)
        res['tgl_kematian'] = get_datetime_type(res['tgl_kematian'], True)

        location_id = postgres_cursor.execute(f"SELECT id FROM master_location WHERE name = '{res['lokasi']}'").fetchone()[0] if res['lokasi'] is not None else 'bb9488cf-7620-4901-a743-e041d313986f'
        postgres_cursor.execute(
            """
            INSERT INTO auth_user
            (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (res['password'], None, False, str(res['no_reg']), res['nama_depan'], res['nama_belakang'], res['email'], False, True, datetime.now())
        )

        user_id = postgres_cursor.execute("SELECT id FROM auth_user WHERE username = '" + res['no_reg'] + "'").fetchone()[0]
        postgres_cursor.execute(
            """
            INSERT INTO master_master
            (id, full_name, gender, address, personal_identity, blood_type, marital_status, profile_photo, created_at, updated_at, location_id, user_id, phone_number, date_of_birth, date_of_death)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,    
            (str(uuid4()), f"{res['nama_depan']} {res['nama_belakang']}", get_gender(res['id_gender']), get_existing(res['alamat']), cleaned_string(res['no_ktp']), get_blood_type(res['id_golongan_darah']), get_marital_status(res['id_marital_status']), None, get_datetime_type(res['created_date']), datetime.now(), location_id, user_id, res['no_hp1'], res['tgl_lahir'], res['tgl_kematian'])
        )
        postgres_conn.commit()

    def pre_save(employee, counter):
        res = sql_server_cursor.execute(
            f"""
            SELECT 
                t_mst_karyawan.id,
                t_mst_karyawan.no_reg,
                t_mst_karyawan.nama_depan,
                t_mst_karyawan.nama_belakang,
                t_mst_karyawan.tgl_lahir,
                t_mst_karyawan.id_gender,
                t_mst_karyawan.no_ktp,
                t_mst_karyawan.id_golongan_darah,
                t_mst_karyawan.id_marital_status,
                t_mst_karyawan.created_date,
                t_mst_karyawan.tgl_kematian,
                t_mst_pr_alamat.alamat,
                t_mst_pr_alamat.email,
                t_mst_pr_alamat.no_hp1,
                t_mst_tmp_lokasi.nama_tmp_lokasi AS lokasi
            FROM 
                t_mst_karyawan
            LEFT JOIN 
                t_mst_pr_alamat ON t_mst_pr_alamat.id_employee = t_mst_karyawan.id
            LEFT JOIN
                t_mst_tmp_lokasi ON t_mst_tmp_lokasi.id = t_mst_karyawan.id_tmp_lokasi
            WHERE 
                t_mst_karyawan.id = '{employee['id']}'
            """
        ).fetchall()
        if res:
            column_names = [desc[0] for desc in sql_server_cursor.description]
            res = to_df(res, column_names, to_dict=True)
        else:
            res = requests.post(url=f"http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetPersonalData?id={employee['no_reg']}").json()[0]
        save_master(res, counter)

    employees = requests.post(url='http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetKaryawan').json()['data']
    for employee in employees:
        pre_save(employee, counter)
        counter += 1

@use_db_connection
def insert_congregation(sql_server_conn, postgres_conn, *args, **kwargs):
    sql_server_cursor = sql_server_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    insertedMaster = []
    insertedNoReg = []

    def save(res, counter):
        res['nama_alias'] = f"rand-{counter}" if res['nama_alias'] is None else res['nama_alias']
        
        res['no_reg'] = cleaned_string(res['no_reg'])
        res['no_reg'] = f"rand-{counter}" if res['no_reg'] is None or res['no_reg'] in insertedNoReg else res['no_reg']
        insertedNoReg.append(res['no_reg'])

        if 'nama_jenis_staff' in res:
            worship_id = postgres_cursor.execute(f"SELECT id FROM management_managementofworship WHERE name = '{res['nama_jenis_staff']}'").fetchone()
            worship_id = worship_id[0] if worship_id else None
        
        if len(insertedMaster) == 0:
            masteruser_id = postgres_cursor.execute("SELECT id FROM master_master WHERE full_name = '" + f"{res['nama_depan']} {res['nama_belakang']}" + "'").fetchone()[0]
        else:
            placeholders = ", ".join(["%s"] * len(insertedMaster))
            masteruser_id = postgres_cursor.execute("SELECT id FROM master_master WHERE full_name = '" + f"{res['nama_depan']} {res['nama_belakang']}" + "' AND id NOT IN (" + placeholders + ")", insertedMaster).fetchone()[0]

        congregation_id = str(uuid4())
        postgres_cursor.execute(    
            """
            INSERT INTO master_congregation
            (id, member_number, alias_name, chinese_name, is_congregation, worship_id, created_at, updated_at, masteruser_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (congregation_id, res['no_reg'], res['nama_alias'], res['nama_mandarin'], True, worship_id, get_datetime_type(res['created_date']), datetime.now(), masteruser_id)
        )

        if res['tgl_baptis']:
            postgres_cursor.execute(
                """
                INSERT INTO master_baptism
                (id, baptism_date, status, created_at, updated_at, congregation_id, masteruser_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), get_datetime_type(res['tgl_baptis'], True), 2, get_datetime_type(res['created_date']), datetime.now(), None, masteruser_id)
            )
        if res['tgl_masuk']:
            postgres_cursor.execute(
                """
                INSERT INTO master_baptism
                (id, baptism_date, status, created_at, updated_at, congregation_id, masteruser_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), get_datetime_type(res['tgl_masuk'], True), 3, get_datetime_type(res['created_date']), datetime.now(), None, masteruser_id)
            )
        if res['tgl_keluar']:
            postgres_cursor.execute(
                """
                INSERT INTO master_baptism
                (id, baptism_date, status, created_at, updated_at, congregation_id, masteruser_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), get_datetime_type(res['tgl_keluar'], True), 4, get_datetime_type(res['created_date']), datetime.now(), None, masteruser_id)
            )
        if res['tgl_sidi']:
            postgres_cursor.execute(
                """
                INSERT INTO master_baptism
                (id, baptism_date, status, created_at, updated_at, congregation_id, masteruser_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), get_datetime_type(res['tgl_sidi'], True), 5, get_datetime_type(res['created_date']), datetime.now(), None, masteruser_id)
            )
        insertedMaster.append(masteruser_id)
        postgres_conn.commit()

    employees = requests.post(url="http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetKaryawan").json()['data']
    for counter, employee in enumerate(employees):
        print(counter+1, employee['nama'])
        res = sql_server_cursor.execute(
            f"""
            SELECT 
                t_mst_karyawan.id,
                t_mst_karyawan.nama_depan,
                t_mst_karyawan.nama_belakang,
                t_mst_karyawan.no_reg,
                t_mst_karyawan.nama_alias,
                t_mst_karyawan.nama_mandarin,
                t_mst_karyawan.tgl_baptis,
                t_mst_karyawan.created_date,
                t_mst_karyawan.tgl_masuk,
                t_mst_karyawan.tgl_keluar,
                t_mst_karyawan.tgl_sidi,
                t_mst_jenis_staff.nama_jenis_staff
            FROM
                t_mst_karyawan
            LEFT JOIN
                t_mst_jenis_staff ON t_mst_jenis_staff.id = t_mst_karyawan.id_jenis_staff
            WHERE
                t_mst_karyawan.id = '{employee['id']}'
            """
        ).fetchall()
        if res:
            column_names = [desc[0] for desc in sql_server_cursor.description]
            res = to_df(res, column_names, to_dict=True)
        else:
            res = requests.post(url=f"http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetPersonalData?id={employee['no_reg']}").json()[0]
        save(res, counter)
        counter += 1

@use_db_connection
def insert_family(sql_server_conn, postgres_conn, *args, **kwargs):
    sql_server_cursor = sql_server_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    def save(res):
        master = postgres_cursor.execute(f"SELECT id FROM master_master WHERE full_name = '{res['nama_depan']} {res['nama_belakang']}'").fetchone()
        if master:
            master = master[0]

            family = sql_server_cursor.execute(f"SELECT nama_keluarga, id_dt_pr_hubungan_keluarga FROM t_mst_pr_keluarga WHERE id_employee = '{res['id']}'").fetchall()
            if family:
                column_names = [desc[0] for desc in sql_server_cursor.description]
                family = to_df(family, column_names)
                for _, row in family.iterrows():
                    family_id = postgres_cursor.execute(f"SELECT id FROM master_master WHERE full_name = '{row['nama_keluarga']}'").fetchone()
                    if family_id:
                        postgres_cursor.execute(
                            """
                            INSERT INTO master_family
                            (id, status, created_at, updated_at, masteruser_id, family_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (str(uuid4()), get_family_status(row['id_dt_pr_hubungan_keluarga']), datetime.now(), datetime.now(), master, family_id[0])
                        )
                        postgres_conn.commit()
    
    def pre_save(res):
        master = sql_server_cursor.execute(f"SELECT id, nama_depan, nama_belakang FROM t_mst_karyawan WHERE id = '{res['id']}'").fetchone()
        if master:
            master = {
                'id': master[0],
                'nama_depan': master[1],
                'nama_belakang': master[2]
            }
        else:
            master = requests.post(url=f"http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetPersonalData?id={res['no_reg']}").json()[0]
        save(master)
    
    employees = requests.post(url='http://gw.gkimkaimtong.org:8888/HR/Services/WebService.asmx/GetKaryawan').json()['data']
    for counter, employee in enumerate(employees):
        print(counter+1, employee['nama'])
        pre_save(employee)
        
# insert_location()
# insert_worship()
# insert_master()
# insert_congregation()
# insert_family()