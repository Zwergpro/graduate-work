from app.models.base import db


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.Integer)
    town_id = db.Column(db.Integer)
    gender = db.Column(db.SmallInteger)
    experience = db.Column(db.SmallInteger)
    science = db.Column(db.SmallInteger)
    category = db.Column(db.SmallInteger)
    position = db.Column(db.SmallInteger)
    rating = db.Column(db.Numeric)
    stars = db.Column(db.Numeric)
    official_rating = db.Column(db.Numeric)
    rates = db.Column(db.Integer)
    drugrates = db.Column(db.SmallInteger)
    answers = db.Column(db.SmallInteger)
    extrainfo = db.Column(db.Integer)
    bio = db.Column(db.Integer)
    hobby = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    appointment_count = db.Column(db.Integer)
    has_owner = db.Column(db.SmallInteger)
    lpu_pro = db.Column(db.SmallInteger)
    min_price = db.Column(db.Integer)
    min_price_go = db.Column(db.Integer)
    min_price_online = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    friendliness = db.Column(db.Numeric)
    osmotr = db.Column(db.Numeric)
    efficiency = db.Column(db.Numeric)
    informativity = db.Column(db.Numeric)
    recommend = db.Column(db.Numeric)
    spec_in_title = db.Column(db.Integer)
    rate_count = db.Column(db.Integer)
    pos = db.Column(db.Integer)
    net = db.Column(db.Integer)
    neg = db.Column(db.Integer)
    wp_count = db.Column(db.Integer)
    min_price_2 = db.Column(db.Integer)
    min_discount = db.Column(db.Integer)
    age_min = db.Column(db.SmallInteger)
    age_max = db.Column(db.SmallInteger)
    avatar = db.Column(db.Integer)
    spec_count = db.Column(db.Integer)
    ed_count = db.Column(db.Integer)
    course_count = db.Column(db.Integer)
    honor_count = db.Column(db.Integer)
    job_count = db.Column(db.Integer)

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
