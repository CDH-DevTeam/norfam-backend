# Nordisk familjebok backend

## Quick setup

1. Install requirements with venv:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    Or conda:

    ```bash
    conda env create -f environment.yml
    conda activate nordisk-familjebok
    ```

2. Create MySQL database `nor_fam_1` and import SQL dump to it

3. Create `norfam/settings_local.py` along the lines of:

    ```python
    DATABASES = {
        'nor_fam_1': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nor_fam_1',
            'USER': '(username)',
            'PASSWORD': '(password)',
            'HOST': 'localhost',
            'PORT': '3306',
        },
    }

    DATABASES['default'] = DATABASES['nor_fam_1']
    ```

    See [Configuring Django Settings: Best Practices](https://djangostars.com/blog/configuring-django-settings-best-practices/#header3) for why.

4. Set up Django in database. The first command will perform some migrations and then end with an error because some of the DB structure is already reflected in the dump. Ignore the error and continue with the next command.

    ```bash
    ./manage.py migrate # Ignore error
    ./manage.py migrate --fake
    ```

5. Run server:

    ```bash
    ./manage.py runserver 8080
    ```
