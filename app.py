from flask import Flask, render_template, request, session
import secrets
import string

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_real_secret_key'

def generate_password(
    length: int,
    uppercase: bool,
    lowercase: bool,
    numbers: bool,
    special: bool
) -> str:
    """
    Generate a secure password using the specified character sets.

    Args:
        length (int): The desired password length.
        uppercase (bool): Include uppercase letters.
        lowercase (bool): Include lowercase letters.
        numbers (bool): Include digits.
        special (bool): Include special characters.

    Returns:
        str: The generated password.
    """
    chars = ''
    if uppercase:
        chars += string.ascii_uppercase
    if lowercase:
        chars += string.ascii_lowercase
    if numbers:
        chars += string.digits
    if special:
        chars += string.punctuation
    if not chars:
        return ''
    return ''.join(secrets.choice(chars) for _ in range(length))

def password_strength(password):
    length = len(password)
    score = 0
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    percent = int((score / 6) * 100)
    if score <= 2:
        return 'Weak', percent, '#ef4444'
    elif score <= 4:
        return 'Medium', percent, '#fbbf24'
    else:
        return 'Strong', percent, '#22c55e'

def is_password_palindrome(password: str) -> bool:
    """Check if the password is a palindrome (for fun)."""
    return password == password[::-1]

def count_unique_characters(password: str) -> int:
    """Return the number of unique characters in the password."""
    return len(set(password))

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ''
    strength = ''
    strength_percent = 0
    strength_color = '#ef4444'
    length = 12
    uppercase = True
    lowercase = True
    numbers = True
    special = True
    error = ''
    history = session.get('history', [])
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        uppercase = 'uppercase' in request.form
        lowercase = 'lowercase' in request.form
        numbers = 'numbers' in request.form
        special = 'special' in request.form
        if not (uppercase or lowercase or numbers or special):
            error = 'Please select at least one character type.'
        else:
            password = generate_password(length, uppercase, lowercase, numbers, special)
            if password:
                strength, strength_percent, strength_color = password_strength(password)
                # Update history
                history = session.get('history', [])
                if password not in history:
                    history.insert(0, password)
                history = history[:5]
                session['history'] = history
    return render_template('index.html', password=password, strength=strength, strength_percent=strength_percent, strength_color=strength_color, length=length, uppercase=uppercase, lowercase=lowercase, numbers=numbers, special=special, error=error, history=history)

if __name__ == '__main__':
    app.run(debug=True) 