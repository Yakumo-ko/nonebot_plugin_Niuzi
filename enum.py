from enum import IntEnum, unique 

@unique
class Sex(IntEnum):
    MALE = 0
    FEMALE = 1

    @classmethod
    def getMax(cls) -> int:
        res: int = cls.FEMALE.value
        for i in cls:
            res = max(res, i.value)

        return res

    @classmethod
    def getMin(cls) -> int:
        res: int = cls.FEMALE.value
        for i in cls:
            res = min(res, i.value)

        return res


@unique
class CDType(IntEnum):
    pk = 0
    doi = 1
