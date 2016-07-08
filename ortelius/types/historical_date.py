from datetime import datetime
import sqlalchemy
import jdcal

from ortelius.types.errors import APIError

class DateError(APIError):
    """DateError exception"""
    def __init__(self, message):
        APIError.__init__(self)
        self.message = message

    def __repr__(self):
        return 'DateError: %s' % (self.message)


class HistoricalDate(object):
    """HistoricalDate"""

    __month = 0
    __day = 0
    __year = 0

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

    @property
    def year(self):
        return str(self.__year)

    @year.setter
    def year(self, value):
        self.__year = value

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
            bc = False
            if value.startswith('-'):
                value = value[1:]
                bc = True

            arr_value = value.split('-')
            if len(arr_value) != 3:
                raise DateError('Date must be in format YYYY-MM-DD')
            year = int(arr_value[0]) if not bc else -int(arr_value[0])
            month = int(arr_value[1])
            day = int(arr_value[2])

        elif isinstance(value, datetime):
            year = value.year
            month = value.month
            day = value.day

        elif isinstance(value, HDate):
            s_value = str(value.date)
            year = int(s_value[:-4])
            month = int(s_value[-4:-2])
            day = int(s_value[-2:])

        else:
            raise DateError('Argument should be int, string in format YYYY-MM-DD or datetime.datetime object')

        if year == 0:
            raise DateError("Year cannot be 0")

        if month <= 0 or month > 12:
            raise DateError("Month must be between 1 and 12")

        if day <= 0:
            raise DateError("Day cannot be 0")

        if month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
            raise DateError("This month has only 31 days")

        if month == 2 and jdcal.is_leap(year) and day > 29:
            raise DateError("This month has only 29 days")

        if month == 2 and not jdcal.is_leap(year) and day > 28:
            raise DateError("This month has only 28 days")

        if month in [4, 6, 9, 11] and day > 30:
            raise DateError("This month has only 30 days")

        self.year = year
        self.month = month
        self.day = day


    def __eq__(self, value):
        return self.year == value.year and self.month == value.month and self.day == value.day

    def __gt__(self, value):
        if not isinstance(value, HistoricalDate):
            raise DateError('Object to compare must be HistoricalDate instance')

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
            raise DateError('Object to compare must be HistoricalDate instance')

        if self.year > value.year:
            return True

        elif self.year == value.year:
            if self.month > value.month:
                return True
            elif self.month == value.month:
                return self.day >= value.day
            else:
                return False
        else:
            return False

    def __lt__(self, value):
        if not isinstance(value, HistoricalDate):
            raise DateError('Object to compare must be HistoricalDate instance')

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
            raise DateError('Object to compare must be HistoricalDate instance')

        if self.year < value.year:
            return True

        elif self.year == value.year:
            if self.month < value.month:
                return True
            elif self.month == value.month:
                return self.day <= value.day
            else:
                return False
        else:
            return False

    def add(self, value):
        raise NotImplementedError()

    def subtract(self, value):
        raise NotImplementedError()

    def delta(self, value):
        raise NotImplementedError()

    def to_string(self):
        # NOTE: It's not really fast
        return '-'.join([str(self.year), str(self.month), str(self.day)])

    def to_julian(self):
        jd = jdcal.gcal2jd(int(self.year), int(self.month), int(self.day))
        jcal = jdcal.jd2jcal(jd[0], jd[1])[:-1]
        return '-'.join([str(jcal[0]), str(jcal[1]), str(jcal[2])])

    def to_int(self):
        return int(''.join([str(self.year), str(self.month), str(self.day)]))

    def __repr__(self):
        return self.to_string()



class HDate(sqlalchemy.types.TypeDecorator):
    """Custom sqlalchemy type for date implementation. Stores data in database as Integer in 'YYYYMMDD' format, e.g. '19001004' or '-100000301' Note that leading zero in days and months lesser than 10 is requred (e.g. 09 or 04 in 12800904)"""

    impl = sqlalchemy.types.Integer

    def process_bind_param(self, value, dialect):
        return int(''.join([str(value.year), str(value.month), str(value.day)]))

    def process_result_value(self, value, dialect):
        return HistoricalDate(value)

    def coerce_compared_value(self, op, value):
        if isinstance(value, int):
            return sqlalchemy.types.Integer()
        elif isinstance(value, HistoricalDate):
            return HDate()
        else:
            return self.impl.coerce_compared_value(op, value)

    # def copy(self):
    #     return HDate(self.impl)
