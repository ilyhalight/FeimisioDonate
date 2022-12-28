import re
import time
import math
import requests
from lxml import etree


class SteamConverters():
    def __init__(self) -> None:
        self.steam_id_regex = "^STEAM_"
        self.steam_id3_regex = "^\[.*\]$"
        self.steam_url_regex = re.compile("^(https:\/\/|http:\/\/)?steamcommunity.com\/(id|profiles)\/.*$")
        self.id64_base = 76561197960265728 

    def convert_steamID(self, steamID, target_format: str, as_int: bool = False):
        """
        Wrapper for conversion methods to allow you to call different conversions via the same function

        Parameters
        ----------
        steamID : int or str
            steamID of any format to convert
        
        target_format : str
            Format to convert steamId to
            Possible values are: SteamID, SteamID3, SteamID64

        as_int : bool
            If a SteamId64 is returned as an int or a string
            Only used when target_format = SteamId64
            Default = False


        Returns
        -------
        int or str
            steamID value

        """

        if target_format == 'SteamID':
            return self.to_steamID(steamID)
        elif target_format == 'SteamID3':
            return self.to_steamID3(steamID)
        elif target_format == 'SteamID64':
            return self.to_steamID64(steamID, as_int)
        else:
            raise ValueError("Incorrect target Steam ID format. Target_format must be one of: SteamID, SteamID3, SteamID64")

    def to_steamID(self, steamID):
        """
        Convert to steamID

        A steamID is unique to each steam account, 
        Formatted with digits as x "STEAM_0:x:xxxxxxxx"

        Parameters
        ----------
        steamID : int or str
            steamID3 or steamID64 to convert to steamID

        Returns
        -------
        str
            steamID value

        """

        id_str = str(steamID)

        if re.search(self.steam_id_regex, id_str): # Already a steamID
            return id_str
        elif re.search(self.steam_id3_regex, id_str): # If passed steamID3
            id_split = id_str.split(":") # Split string into 'Universe', Account type, and Account number
            account_id3 = int(id_split[2][:-1]) # Remove ] from end of steamID3

            if account_id3 % 2 == 0:
                account_type = 0
            else:
                account_type = 1

            account_id = (account_id3 - account_type) // 2
        elif id_str.isnumeric(): # Passed steamID64
            self.check_steamID64_length(id_str) # Validate id passed in

            offset_id = int(id_str) - self.id64_base

            # Get the account type and id
            if offset_id % 2 == 0:
                account_type = 0
            else:
                account_type = 1

            account_id = ((offset_id - account_type) // 2)

        return "STEAM_0:" + str(account_type) + ":" + str(account_id)

    def to_steamID3(self, steamID):
        """
        Convert to steamID3

        A steamID3 is unique to each steam account, 
        Formatted with digits as x "[U:1:xxxxxxxx]"

        Parameters
        ----------
        steamID : int or str
            steamID or steamID64 to convert to steamID3

        Returns
        -------
        str
            steamID3 value

        """

        id_str = str(steamID)

        if re.search(self.steam_id3_regex, id_str): # Already a steamID3
            return id_str
        elif re.search(self.steam_id_regex, id_str): # If passed steamID
            id_split = id_str.split(":") # Split string into 'Universe', Account type, and Account number

            account_type = int(id_split[1]) # Check for account type
            account_id = int(id_split[2]) # Account number, needs to be doubled when added to id3

            # Join together in steamID3 format
            return "[U:1:" + str(((account_id + account_type) * 2) - account_type) + "]"
        elif id_str.isnumeric(): # Passed steamID64
            self.check_steamID64_length(id_str) # Validate id passed in

            offset_id = int(id_str) - self.id64_base

            # Get the account type and id
            if offset_id % 2 == 0:
                account_type = 0
            else:
                account_type = 1

            account_id = ((offset_id - account_type) // 2) + account_type

            # Join together in steamID3 format
            return "[U:1:" + str((account_id * 2) - account_type) + "]"
        else:
            raise ValueError(f"Unable to decode steamID: {steamID}")

    def to_steamID64(self, steamID, as_int = False):
        """
        Convert to steamID64

        A steamID64 is a 17 digit number, unique to each steam account

        Parameters
        ----------
        steamID : int or str
            steamID or steamID3 to convert to steamID64
        as_int : bool
            If the steamID64 is returned as an integer rather than string, Default = False

        Returns
        -------
        int or str
            steamID64 value

        """

        id_str = str(steamID)
        id_split = id_str.split(":") # Split string into 'Universe', Account type, and Account number

        if id_str.isnumeric(): # Already a steamID64
            self.check_steamID64_length(id_str) # Validate id passed in
            if as_int:
                return int(id_str)
            else:
                return id_str
        elif re.search(self.steam_id_regex, id_str): # If passed steamID
            
            account_type = int(id_split[1]) # Check for account type
            account_id = int(id_split[2]) # Account number, needs to be doubled when added to id64
        elif re.search(self.steam_id3_regex, id_str): # If passed steamID3
            account_id3 = int(id_split[2][:-1]) # Remove ] from end of steamID3

            if account_id3 % 2 == 0:
                account_type = 0
            else:
                account_type = 1

            account_id = (account_id3 - account_type) // 2
        else:
            raise ValueError(f"Unable to decode steamID: {steamID}")


        id64 = self.id64_base + (account_id * 2) + account_type

        # Check if returning as string or integer
        if as_int:
            return id64
        else:
            return str(id64)

    def check_steamID64_length(self, id_str: str):
        """
        Check if a steamID64 is of the correct length, raises ValueError if not.

        Not really for you to use

        Parameters
        ----------
        id_str : str
            steamID64 to check length of

        """

        if len(id_str) != 17:
            raise ValueError(f"Incorrect length for steamID64: {id_str}")

    def url_to_steam64(self, url: str):
        """
        Convert a steam profile URL to a steamID64
        """
        if self.steam_url_regex.match(url):
            res = requests.get(f'{url}?xml=1')
            if res.status_code == 200:
                tree = etree.XML(res.content)
                steamid = tree.find('steamID64').text
                return steamid
            raise ValueError(f"Unable to get steamID64 from URL: {url}")
        raise ValueError(f"Invalid URL: {url}")

    def url_to_nickname(self, url: str):
        """
        Convert a steam profile URL to a nickname
        """
        if self.steam_url_regex.match(url):
            res = requests.get(f'{url}?xml=1')
            if res.status_code == 200:
                tree = etree.XML(res.content)
                steamid = tree.find('steamID').text
                return steamid
            raise ValueError(f"Unable to get nickname from URL: {url}")
        raise ValueError(f"Invalid URL: {url}")


class TimeConverters():
    def __init__(self) -> None:
        self.time_regex = "^[0-9]{1,3}[smhdw]$" # Regex for time format
        self.time_rotation = {
            's': '1',
            'm': '60',
            'h': '3600',
            'd': '86400',
            'w': '604800'
        }

    def is_str_time(self, str_time: str) -> bool:
        """
        Check if a string is a valid time format

        Parameters
        ----------
        str_time : str
            String to check if valid time format

        Returns
        -------
        bool
            True if valid time format, False if not
        """

        return re.search(self.time_regex, str(str_time))

    def convert_str_time_to_seconds(self, str_time: str) -> int:
        """Конвертирует время в формате 1s, 1m, 1h, 1d, 1w в секунды в формате int

        Args:
            time (str): время в формате 1s, 1m, 1h, 1d, 1w

        Returns:
            int: секунды
        """

        if self.is_str_time(str_time):
            alternative_time = ''

            for s in str_time:
                if s.lower() in self.time_rotation:
                    intermediate_time = self.time_rotation[s.lower()]
                else:
                    alternative_time += f'{s}'

            if int(alternative_time) <= 0:
                alternative_time = 1

            final_time = int(alternative_time) * int(intermediate_time)
            return final_time
        return None

    def add_str_time_to_unix_time(self, str_time: str) -> int:
        """Конвертирует время в формате 1s, 1m, 1h, 1d, 1w в секунды и добавляет их к текущему unix времени

        Args:
            str_time (str): время в формате 1s, 1m, 1h, 1d, 1w

        Returns:
            int: секунды
        """
        seconds = self.convert_str_time_to_seconds(str_time)
        if seconds:
            timestamp = int(time.time())
            result_timestamp = timestamp + seconds
            return result_timestamp
        return None

    def multiply_str_time(self, str_time: str, multiply: int|float) -> str:
        """Умножает время в формате 1s, 1m, 1h, 1d, 1w и возвращает в формате * дн. * час., * сек. и т.д.

        Args:
            str_time (str): время в формате 1s, 1m, 1h, 1d, 1w
            multiply (int|float): число на которое надо умножить

        Returns:
            msg (str): Перемноженное время
        """
        seconds = self.convert_str_time_to_seconds(str_time)
        if seconds:
            multiplied_time = seconds * multiply
            days, hours, minutes, seconds = self.secs_to_time(multiplied_time)

            if all((days, hours, minutes)):
                msg = f"{days} дн. {hours} час. {minutes} мин. {seconds} сек."
            elif all((hours, minutes)):
                msg = f"{hours} час. {minutes} мин. {seconds} сек."
            elif minutes != 0:
                msg = f"{minutes} мин. {seconds} сек."
            else:
                msg = f"{seconds} сек."
            return msg
        return None

    def secs_to_max_unit(self, seconds: int) -> str:
        """Конвертирует секунды в максимальную еденицу времени (часы/минуты/секунды)

        Args:
            seconds (int): Время в секундах
        
        Returns:
            msg (str): Максимальная единица времени
        """
        hours_up = round(seconds) // 3600
        seconds %= 3600
        minutes_up = round(seconds) // 60
        seconds = round(seconds % 60)

        if hours_up != 0:
            msg = f"{hours_up} час."
        elif minutes_up != 0:
            msg = f"{minutes_up} мин."
        else:
            msg = f"{seconds} сек."
        return msg

    def secs_to_time(self, seconds: int) -> tuple[int, int, int, int]:
        """Преобразует секунды в понятное человеку время в формате: "День, час, минута, секунда"

        Args:
            seconds (int): Время в секундах

        Returns:
            tuple[int, int, int, int]: кортеж из мер времени в формате: [День, час, минута, секунда]
        """    
        days = round(seconds) // 86400
        seconds %= 86400
        hours = round(seconds) // 3600
        seconds %= 3600
        minutes = round(seconds) // 60
        seconds = round(seconds % 60)
        return days, hours, minutes, seconds


class OtherConverter:
    def __init__(self) -> None:
        self.size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s%s" % (s, self.size_name[i])
