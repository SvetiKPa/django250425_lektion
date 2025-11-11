from enum import StrEnum


class Role(StrEnum):  # Енам класс. Похоже как мы делали список с кортежами, только мощнее(можно создвать свои настройки, методы и прочее)
    lib_member = "Lib Member"
    admin = "Admin"
    moderator = "Moderator"
    guest = "Guest"

    @classmethod
    def choices(cls):  # choices параметр в поле требует список с кортежами, поэтому этот метод будет нам его формировать.
        return [(attr.name, attr.value) for attr in cls]


class Gender(StrEnum):
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
