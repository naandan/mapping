
class Gender:
    MAN = 1, "Man"
    WOMAN = 2, "Woman"

class BloodType:
    A_POSITIVE = 1, 'A+'
    B_POSITIVE = 2, 'B+'
    AB_POSITIVE = 3, 'AB+'
    O_POSITIVE = 4, 'O+'
    A_NEGATIVE = 5, 'A-'
    B_NEGATIVE = 6, 'B-'
    AB_NEGATIVE = 7, 'AB-'
    O_NEGATIVE = 8, 'O-'

class MaritalStatus:
    SINGLE = 1, 'Single'
    MARRIED = 2, 'Married'
    DIVORCED = 3, 'Divorced'
    WIDOWED = 4, 'Widowed'

class FamilyStatus:
    GRANDFATHHER = 1, 'Grandfather'
    GRANDMOTHER = 2, 'Grandmother'
    FATHER = 3, 'Father'
    MOTHER = 4, 'Mother'
    CHILD = 5, 'Child'
    STEPCHILD = 6, 'Step Child'
    ADOPTEDCHILD = 7, 'Adopted Child'
    STEPMOTHER = 8, 'Step Mother'
    STEPFATHER = 9, 'Step Father'
    # Todo: Add family status
    HUSBAND = 10, 'Husband'
    WIFE = 11, 'Wife'
    BROTHER = 12, 'Brother'
    SISTER = 13, 'Sister'
    RELATIVES = 14, 'Relatives'
    SIBLING = 15, 'Sibling'

class BaptisStatus:
    BAPTISM_CILD = 1, 'Baptis Child'
    BAPTISM_ADULT = 2, 'Baptism Adult'

class AgamaStatus:
    ISLAM = 1, 'Islam'
    KRISTEN = 2, 'Kristen'
    KATHOLIK = 3, 'Katholik'
    HINDU = 4, 'Hindu'
    BUDHA = 5, 'Budha'
    KONGHUCU = 6, 'Konghucu'

class TypeOfWorship:
    ONLINE = 1, 'Online'
    OFFLINE = 2, 'Offline'
    HYBRID = 3, 'Hybrid'

class SourcePresence:
    FINGERPRINT = 1, 'Fingerprint'
    QR_CODE = 2, 'QR Code'
    RFID = 3, 'RFID'