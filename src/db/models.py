from sqlalchemy import Column, Integer, SmallInteger, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Appointment(BaseModel):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    doctor_id = Column(Integer)
    dt_created = Column(DateTime)

    def __repr__(self):
        return f'<Appt(user={self.user_id}, doctor={self.doctor_id})>'


class DoctorTown(BaseModel):
    __tablename__ = 'doctors_towns'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    town_id = Column(Integer)
    spec_id = Column(Integer)
    wp_spec_id = Column(Integer)
    rating = Column(Numeric)

    def __repr__(self):
        return f'<DoctorTown(doctor={self.doctor_id})>'


class DoctorSpec(BaseModel):
    __tablename__ = 'doctor_spec'

    id = Column(Integer, primary_key=True)
    spec_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'<Doctor_Spec(doctor={self.id}, spec={self.spec_id})>'


class Doctor(BaseModel):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    spec_id = Column(Integer)
    town_id = Column(Integer)
    gender = Column(SmallInteger)
    experience = Column(SmallInteger)
    science = Column(SmallInteger)
    category = Column(SmallInteger)
    position = Column(SmallInteger)
    rating = Column(Numeric)
    stars = Column(Numeric)
    official_rating = Column(Numeric)
    rates = Column(Integer)
    drugrates = Column(SmallInteger)
    answers = Column(SmallInteger)
    extrainfo = Column(Integer)
    bio = Column(Integer)
    hobby = Column(Integer)
    comments = Column(Integer)
    appointment_count = Column(Integer)
    has_owner = Column(SmallInteger)
    lpu_pro = Column(SmallInteger)
    min_price = Column(Integer)
    min_price_go = Column(Integer)
    min_price_online = Column(Integer)
    hits = Column(Integer)
    friendliness = Column(Numeric)
    osmotr = Column(Numeric)
    efficiency = Column(Numeric)
    informativity = Column(Numeric)
    recommend = Column(Numeric)
    spec_in_title = Column(Integer)
    rate_count = Column(Integer)
    pos = Column(Integer)
    net = Column(Integer)
    neg = Column(Integer)
    wp_count = Column(Integer)
    min_price_2 = Column(Integer)
    min_discount = Column(Integer)
    age_min = Column(SmallInteger)
    age_max = Column(SmallInteger)
    avatar = Column(Integer)
    spec_count = Column(Integer)
    ed_count = Column(Integer)
    course_count = Column(Integer)
    honor_count = Column(Integer)
    job_count = Column(Integer)

    _fields = (
        'id',
        'spec_id',
        'town_id',
        'gender',
        'experience',
        'science',
        'category',
        'position',
        'rating',
        'stars',
        'official_rating',
        'rates',
        'drugrates',
        'answers',
        'extrainfo',
        'bio',
        'hobby',
        'comments',
        'appointment_count',
        'has_owner',
        'lpu_pro',
        'min_price',
        'min_price_go',
        'min_price_online',
        'hits',
        'friendliness',
        'osmotr',
        'efficiency',
        'informativity',
        'recommend',
        'spec_in_title',
        'rate_count',
        'pos',
        'net',
        'neg',
        'wp_count',
        'min_price_2',
        'min_discount',
        'age_min',
        'age_max',
        'avatar',
        'spec_count',
        'ed_count',
        'course_count',
        'honor_count',
        'job_count',
    )

    def __repr__(self):
        return f'<Doctor(id={self.id})>'

    def __iter__(self):
        for item in self._fields:
            yield getattr(self, item)
