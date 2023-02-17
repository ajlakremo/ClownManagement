from marshmallow import ValidationError

from authentication_service import User


def validate_registration(email, password, confirm_password):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError('Email already exists.')
    elif password != confirm_password:
        raise ValidationError('Passwords don\'t match.')
    elif len(password) < 7:
        raise ValidationError('Password must be at least 7 characters.')
