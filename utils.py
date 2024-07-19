from const import *
from datetime import datetime
import os

def get_gender(gender):
    if gender == 'GENDER001':
        return Gender.MAN[0]
    elif gender == 'GENDER002':
        return Gender.WOMAN[0]
    elif gender == 'GENDER003':
        return 3

def get_fullname(first_name, last_name):
    return first_name + ' ' + last_name if last_name is not None or last_name != '-' else ''

def get_blood_type(blood_type):
    if blood_type == '17M110001':
        return BloodType.A_POSITIVE[0]
    elif blood_type == '17M110002':
        return BloodType.AB_POSITIVE[0] 
    elif blood_type == '17M110003':
        return BloodType.B_POSITIVE[0]
    elif blood_type == '17M110004':
        return BloodType.O_POSITIVE[0]
    else:
        return 0

def get_marital_status(marital_status):
    if marital_status == 'MARITAL01':
        return MaritalStatus.MARRIED[0]
    elif marital_status == 'MARITAL02':
        return MaritalStatus.SINGLE[0]
    elif marital_status == 'MARITAL03':
        return MaritalStatus.WINDOWWINDOWER[0]
    else:
        return 0

def get_identity_number(identity_number):
    try:
        identity_number = int(identity_number)
    except:
        identity_number = 0

    return identity_number

def get_religion(religion):
    if religion == 'AGAMA0001':
        return AgamaStatus.KRISTEN[0]
    elif religion == 'AGAMA0002':
        return AgamaStatus.KATHOLIK[0]
    elif religion == 'AGAMA0003':
        return AgamaStatus.BUDHA[0]
    elif religion == 'AGAMA0004':
        return AgamaStatus.HINDU[0]
    elif religion == 'AGAMA0005':
        return AgamaStatus.KONGHUCU[0]
    elif religion == 'AGAMA0006':
        return AgamaStatus.ISLAM[0]
    else:
        return 0
    
def get_int_type(int_type):
    try:
        int_type = int(int_type)
    except:
        int_type = None

    return int_type

date_format = "%Y-%m-%d %H:%M:%S"

def get_datetime_type(datetime_type, none=False):
    try:
        return datetime.combine(datetime_type, datetime.min.time())
    except:
        if datetime_type is None:
            if none:
                return None
            else:
                return datetime.now()
        else:
            try:
                return datetime.strptime(datetime_type, date_format)
            except:
                timestamp_s = int(int(datetime_type.strip("/Date()"))) / 1000
                return datetime.fromtimestamp(timestamp_s)

def formatted(data):
    formatted_data = []
    for record in data:
        new_record = []
        for item in record:
            if isinstance(item, datetime):
                new_record.append(item.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                new_record.append(item)
        formatted_data.append(tuple(new_record))
    return formatted_data

def formatted_item(data):
    new_record = []
    for item in data:
        if isinstance(item, datetime):
            new_record.append(item.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            new_record.append(item)
    return tuple(new_record)

def cleaned_string(string):
    try:
        return string.replace(" ", "")
    except:
        return None

def get_existing(data):
    return data if data is not None else None

def get_family_status(family_status):
    if family_status == '17M130001':
        return FamilyStatus.FATHER[0]
    elif family_status == '17M130002':
        return FamilyStatus.MOTHER[0]
    elif family_status == '17M130003':
        return FamilyStatus.HUSBAND[0]
    elif family_status == '17M130004':
        return FamilyStatus.WIFE[0]
    elif family_status == '17M130005':
        return FamilyStatus.CHILD[0]
    elif family_status == '17M130006':
        return FamilyStatus.SISTER[0]
    elif family_status == '17M130007':
        return FamilyStatus.BROTHER[0]
    elif family_status == '17M130008':
        return FamilyStatus.RELATIVES[0]
    else:
        return 0

def generate_password(password_raw=None):
    if password_raw is not None:
        if password_raw.startswith("/Date"):
            password_raw = password_raw.strip("/Date()").replace(" ", "")
            return datetime.fromtimestamp(int(password_raw) / 1000).strftime("%d%m%Y")
        return datetime.strptime(password_raw, date_format).strftime("%d%m%Y")
    else:
        return "p455word"