# app.py
import os
import sys


def main():
    # plik konfiguracyjny ustawień Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nie można zaimportować Django. Upewnij się, że jest zainstalowane "
            "i środowisko wirtualne (venv) jest aktywne."
        ) from exc

    args = sys.argv
    if len(args) == 1:
        args = [args[0], 'runserver', '0.0.0.0:5000']

    execute_from_command_line(args)


if __name__ == '__main__':
    main()