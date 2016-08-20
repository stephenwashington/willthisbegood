#WILL THIS BE GOOD

[willthisbegood.website](http://willthisbegood.website) is a singe-page website that tells you if certain things will be good or not. All opinions are final.

This website updates daily. To complain about the website, email minervaheavyindustries@gmail.com. To complain about the opinions, tweet [@badpun](https://twitter.com/badpun)

#Installation

willthisbegood runs on Flask, python3, and a Gmail account. `process_new_things.py` looks at the gmail account, and grabs all emails sent by the whitelisted email. These are then stored in a sqlite3 database, which `wtbg.py` uses to populate the page. To actually install:

1. Clone this repository

    ```shell
    git clone https://github.com/stephenwashington/willthisbegood
    ```

2. Set up a virtual environment

    ```shell
    cd willthisbegood
    virtualenv venv
    . venv/bin/activate
    ```

3. Install the necessary dependencies via pip3

    ```shell
    pip3 install -r requirements.txt
    ```

4. Set the environmental variables

    ```shell
    export FLASK_APP="wtbg.py"
    export EMAIL_ADDR="email.to.get.things.from@example.com"
    export EMAIL_PASS="yourp4ssword"
    export WTBG_EMAIL="whtielisted.email@example.com"
    ```

5. Run init_db() in `wtbg.py`

    ```shell
    >>> from wtbg.py import init_db
    >>> init_db()
    ```

6. Run the Flask app (App will be on http://127.0.0.1:5000)

    ```shell
    flask run
    ```
