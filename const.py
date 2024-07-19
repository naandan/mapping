class Gender:
    MAN = 1, "Laki-laki"
    WOMAN = 2, "Perempuan"


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
    SINGLE = 1, 'Belum Menikah'
    MARRIED = 2, 'Menikah'
    WINDOWWINDOWER = 3, 'Janda/Duda'

class FamilyStatus:
    FATHER = 1, 'Ayah',
    MOTHER = 2, 'Ibu'
    HUSBAND = 3, 'Suami'
    WIFE = 4, 'Istri'
    CHILD = 5, 'Anak'
    BROTHER = 6, 'Kakak'
    SISTER = 7, 'Adik'
    RELATIVES = 8, 'Kerabat'

class BaptisStatus:
    BAPTISM_CILD = 1, 'Anak'
    BAPTISM_ADULT = 2, 'Dewasa'
    BAPTISM_ATESTASI_MASUK = 3, 'Atestasi Masuk'
    BAPTISM_ATESTASI_KELUAR = 4, 'Atestasi Keluar'
    BAPTISM_SIDI = 5, 'Sidi'

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

class Role:
    CONGREGATION = 1, 'Congregation'
    SERVANTOFGOD = 2, 'Servant Of God'
    EMPLOYEE = 3, 'Employee'