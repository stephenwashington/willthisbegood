#!/usr/bin/env python3
import sqlite3
import imaplib
import email
import logging
from os import getenv
from logging.handlers import RotatingFileHandler
from datetime import datetime

EMAIL_ADDR = getenv("WTBG_EMAIL",'')
EMAIL_PASS = getenv("WTBG_PASS",'')
WHITELISTED_EMAIL = getenv("WTBG_WHITELISTED_EMAIL",'')

# stuff for logging
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler('wtbg_email.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s (%(levelname)s): %(message)s'))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

def main():
    dbconn = sqlite3.connect('wtbg.db')
    cur = dbconn.cursor()

    # login to the gmail account
    mailbox = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    try:
        mailbox.login(EMAIL_ADDR, EMAIL_PASS)
        logger.info("Successfully logged into email")
    except imaplib.IMAP4.error as e:
        logger.exception("Couldn't log into email")

    mailbox.select() #defaults to inbox

    # loop through all whitelisted emails
    status, response = mailbox.search(None, '(UNSEEN)', '(FROM {})'.format(WHITELISTED_EMAIL))
    unread_msg_nums = response[0].split()

    for email_id in unread_msg_nums:
        _, res = mailbox.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(res[0][1])

        # thing is the subject of the email
        decode = email.header.decode_header(msg['Subject'])[0]
        thing = decode[0].strip().upper()

        # isitgood is the body
        if msg.is_multipart():
            for payload in msg.get_payload():
                if payload.get_content_type() == 'text/plain':
                    isitgood = payload.get_payload()
        else:
            isitgood = msg.get_payload()
        isitgood = isitgood.rstrip().upper() # remove trailing \r\n

        # sent_at is the date the email was sent
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            sent_at = datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
        else:
            sent_at = datetime.utcnow()

        args = (thing.upper(), isitgood.upper(), sent_at.strftime("%Y-%m-%d %H:%M:%S"), 0)
        duplicate = cur.execute("SELECT * FROM THINGS WHERE thing=? AND isitgood=?", (thing, isitgood)).fetchall()

        if not duplicate:
            cur.execute("INSERT INTO things (thing, isitgood, sent_at, posted) values (?,?,?,?)", args)
            mailbox.store(email_id, "+FLAGS", "\Seen")
            logger.info("EMAIL LOGGED: {}".format(args))
    logger.info("{} emails from {}".format(len(unread_msg_nums), WHITELISTED_EMAIL))

    mailbox.close()
    mailbox.logout()
    dbconn.commit() # write all the inserts to the db

    # Update the oldest non-published thing to be published
    query = "SELECT * FROM things WHERE posted=0 ORDER BY sent_at ASC"
    latest_row = cur.execute(query).fetchone()

    if latest_row:
        thing_id = latest_row[0]
        query = "UPDATE things SET posted=1 WHERE id=?"
        cur.execute(query,(thing_id,))
        logger.info("New thing: {}\n".format(latest_row))
    else:
        logger.info("No new thing added to HTML\n")
    dbconn.commit()
    dbconn.close()

if __name__ == '__main__':
    main()
