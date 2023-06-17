class PhoneNumberHelper:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def validator(self):
        if not self.phone_number.startswith(('0', '+84')):
            raise ValueError('this phone number not Vietnamese format')

        self.phone_number = self.phone_number.replace('+84', '0').replace(' ', '')

        if not self.phone_number.isdigit():
            raise ValueError('phone number must be a number')

        if len(self.phone_number) != 10:
            raise ValueError('length of phone number must be 10 characters')

        return self.phone_number
