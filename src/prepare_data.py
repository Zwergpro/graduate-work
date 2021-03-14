from src.vectors import UserVector, DoctorVector


if __name__ == '__main__':
    print('create doctor vector')
    doctor_vectors = DoctorVector()
    doctor_vectors.create()
    doctor_vectors.save()

    print('create user vector')
    user_vectors = UserVector()
    user_vectors.create()
    user_vectors.save()
