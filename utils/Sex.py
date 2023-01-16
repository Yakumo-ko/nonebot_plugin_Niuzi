from enum import IntEnum, unique 

@unique
class Sex(IntEnum):
    FEMALE = 0
    MALE = 1

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



