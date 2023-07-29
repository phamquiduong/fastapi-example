def phone_number_validator(phone_number: str):
    if not phone_number.startswith(('0', '+84')):
        raise ValueError('This phone number not Vietnamese format')

    phone_number = phone_number.replace('+84', '0').replace(' ', '')

    if not phone_number.isdigit():
        raise ValueError('Phone number must be a isdigit')

    if len(phone_number) != 10:
        raise ValueError('Length of phone number must be 10 characters')

    return phone_number
