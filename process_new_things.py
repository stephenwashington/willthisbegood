#!/usr/bin/env python3

import sqlite3
import imaplib
import email
from datetime import datetime

EMAIL_ADDR = "willthisbegood@gmail.com"
EMAIL_PASS = "this will be good"
EMAILS = ["qfloof@gmail.com"]

def main():
    dbconn = sqlite3.connect('wtbg.db')
    cur = dbconn.cursor()

    mailbox = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    try:
        mailbox.login(EMAIL_ADDR, EMAIL_PASS)
        print("Successfully logged in!")
    except imaplib.IMAP4.error:
        print("Something went wrong!\n")

    mailbox.select() #defaults to inbox

    for mail in EMAILS:
        status, response = mailbox.search(None, '(UNSEEN)', '(FROM {})'.format(mail))
        unread_msg_nums = response[0].split()

        for email_id in unread_msg_nums:
            _, res = mailbox.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(res[0][1])
            decode = email.header.decode_header(msg['Subject'])[0]

            thing = decode[0].strip()
            if msg.is_multipart():
                for payload in msg.get_payload():
                    if payload.get_content_type() == 'text/plain':
                        isitgood = payload.get_payload()
            else:
                isitgood = msg.get_payload()
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                sent_at = datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
            else:
                sent_at = datetime.utcnow()

            thing = thing.strip()
            isitgood = isitgood.rstrip() #remove trailing \r\n
            args = (thing, isitgood, sent_at.strftime("%Y-%m-%d %H:%M:%S"), 0)

            cur.execute("INSERT INTO things (thing, isitgood, created_at, posted) values (?,?,?,?)", args)

            mailbox.store(email_id, "+FLAGS", "\Seen")

    mailbox.close()
    mailbox.logout()
    dbconn.commit() #write all the inserts to the db

    query = "SELECT * FROM things WHERE posted=0 ORDER BY created_at ASC"
    latest_row = cur.execute(query).fetchone()

    if latest_row:
        thing_id = latest_row[0]
        query = "UPDATE things SET posted=1 WHERE id=?"
        cur.execute(query,(thing_id,))
    else:
        print("No new rows!")
    dbconn.commit()
    dbconn.close()

if __name__ == '__main__':
    main()
