from django.forms import ValidationError


def validate_phone(phone):
    if not (len(phone) > 9 and phone.isdigit()):
        raise ValidationError


def validate_email(email):
    if '@' not in email or '.' not in email:
        raise ValidationError


def validate_color(color):
    color = color.upper()
    valid_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    if len(color) == 6 or len(color) == 3:
        for char in color:
            if char not in valid_characters:
                raise ValidationError
    else:
        raise ValidationError
