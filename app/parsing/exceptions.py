class Bank2ExcelError(Exception):
    pass


class InputFileStructureError(Bank2ExcelError):
    pass


class BalanceVerificationError(Bank2ExcelError):
    pass


class UserInputError(Bank2ExcelError):
    pass


class TestingError(Bank2ExcelError):
    pass
