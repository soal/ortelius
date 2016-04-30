from datetime import datetime
import sqlalchemy
import jdcal


class HistoricalDate(object):
    """HistoricalDate"""

    __month = 0
    __day = 0

    @property
    def month(self):
        return '0' + str(self.__month) if self.__month < 10 else str(self.__month)

    @month.setter
    def month(self, value):
        self.__month = value

    @property
    def day(self):
        return '0' + str(self.__day) if self.__day < 10 else str(self.__day)

    @day.setter
    def day(self, value):
        self.__day = value

    def __init__(self, value):
        year = 0
        month = 0
        day = 0

        if isinstance(value, int):
            s_value = str(value)
            year = int(s_value[:-4])
            month = int(s_value[-4:-2])
            day = int(s_value[-2:])

        elif isinstance(value, str):
            arr_value = value.split('-')
            if len(arr_value) != 3:
                raise Exception('Date must be in format: "YYYY-MM-DD"')
            year = int(arr_value[0])
            month = int(arr_value[1])
            day = int(arr_value[2])

        elif isinstance(value, datetime):
            year = value.yars
            month = value.month
            day = value.day

        else:
            raise Exception('Argument should be int, string in format "YYYY-MM-DD" or datetime.datetime object')

        if year == 0:
            raise Exception("Year cannot be 0")

        if month <= 0 or month > 12:
            raise Exception("Month must be between 1 and 12")

        if day <= 0:
            raise Exception("Day cannot be 0")

        if month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
            raise Exception("This month has only 31 days")

        if month == 2 and jdcal.is_leap(year) and day > 29:
            raise Exception("This month has only 29 days")

        if month == 2 and not jdcal.is_leap(year) and day > 28:
            raise Exception("This month has only 28 days")

        if month in [4, 6, 9, 11] and day > 30:
            raise Exception("This month has only 30 days")

        self.year = year
        self.month = month
        self.day = day


    def __eq__(self, value):
        return self.year == value.year and self.month == value.month and self.day == value.day

    def __gt__(self, value):
        if not isinstance(value, HistoricalDate):
            raise Exception('Object to compare must be HistoricalDate instance')

        if self.year < value.year:
            return False
        elif self.year > value.year:
            return True
        else:
            if self.month < value.month:
                return False
            elif self.month > value.month:
                return True
            else:
                if self.day < value.day:
                    return False
                elif self.day > value.day:
                    return True


    def __ge__(self, value):
        if not isinstance(value, HistoricalDate):
            raise Exception('Object to compare must be HistoricalDate instance')

        if self.year > value.year:
            return True

        elif self.year == value.year:
            if self.month > value.month:
                return True
            elif self.month == value.month:
                if self.day >= value.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __lt__(self, value):
        if not isinstance(value, HistoricalDate):
            raise Exception('Object to compare must be HistoricalDate instance')

        if self.year > value.year:
            return False
        elif self.year < value.year:
            return True
        else:
            if self.month > value.month:
                return False
            elif self.month < value.month:
                return True
            else:
                if self.day > value.day:
                    return False
                elif self.day < value.day:
                    return True

    def __le__(self, value):
        if not isinstance(value, HistoricalDate):
            raise Exception('Object to compare must be HistoricalDate instance')

        if self.year < value.year:
            return True

        elif self.year == value.year:
            if self.month < value.month:
                return True
            elif self.month == value.month:
                if self.day <= value.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def add(self, value):
        raise NotImplemented()

    def subtract(self, value):
        raise NotImplemented()

    def delta(self, value):
        raise NotImplemented()

    def to_string(self):
        return '-'.join([str(self.year), str(self.month), str(self.day)])

    def to_julian(self):
        jd = jdcal.gcal2jd(int(self.year), int(self.month), int(self.day))
        jcal = jdcal.jd2jcal(jd[0], jd[1])[:-1]
        return '-'.join([jcal[0], jcal[1], jcal[2]])

    def __repr__(self):
        return self.to_string()



class HDate(sqlalchemy.types.TypeDecorator):
    """Custom sqlalchemy type for date implementation. Stores data in database as Integer in 'YYYYMMDD' format, e.g. '19001004' or '-100000301'"""

    impl = sqlalchemy.types.Integer

    def process_bind_param(self, value, dialect):
        return int(''.join([str(value.year), str(value.month), str(value.day)]))

    def process_result_value(self, value, dialect):
        return HistoricalDate(value)

    # def copy(self):
    #     return HDate(self.impl)
