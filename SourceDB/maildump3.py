import pandas as pd
import time as tm, os, glob
import datetime as dt
import email, imaplib
# from email.parser import HeaderParser

cwd = os.getcwd()

EMAIL_UN = 'orob5280@gmail.com'
EMAIL_PW = 'tebdxqvaptuosszk'

subject_header = "Notice: Your Mortgage Statement Is Available"
subject_header = "Honeywell"


def details(subject_header,date=(dt.datetime.now()-dt.timedelta(1)).strftime("%d-%b-%Y")):
    #EMAIL SEARCH CRITERIA
    search_criteria = '(ON '+date+' SUBJECT "'+subject_header+'")'
    search_criteria = '(SUBJECT "'+subject_header+'")'
    return search_criteria

def attachment_download(SUBJECT):
    un = EMAIL_UN
    pw = EMAIL_PW
    url = 'imap.gmail.com'
    cnt = 0
    detach_dir = '.' # directory where to save attachments (default: current)
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL(url,993)
    m.login(un,pw)
    m.select()
    print("Searching Mailboxes")
    resp, items = m.search(None, 'ALL')
    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items2 = items[0].split() # decode('UTF-8') # getting the mails id
    print(len(items2))
    items = [x.decode('UTF8') for x in items2]
    results = []
    errcnt=0
    for emailid in items:
        cnt+= 1
        if cnt%100 == 0:
              print("Cnt is :",cnt)
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        try:
            email_body = data[0][1].decode('UTF-8') # getting the mail content
        except Exception:
            errcnt+=1
            continue
        mail = email.message_from_string(str(email_body)) # parsing the mail content to get a mail object
        dtimestamp = tm.mktime(email.utils.parsedate(mail['Date']))
        dt_object = dt.datetime.fromtimestamp(dtimestamp)

        printit = False
        if printit == True:
            print("Mail Message Header: ", end="|")
            print(mail['Return-Path'], end="|")
            print(mail['From'], end="|")
            print(mail['To'], end ="\n")
            print(dtimestamp, end="|")
            # print(mail['Content-Type'])   multipart/alternative; boundary=Apple-Mail-211--633876483
            # print(mail['Received'])     # mail server/routing info            print(mail['Subject'], end="|")
            # print(mail['References'])   <EEF25BC7-AF75-4365-997C-80D3E4C6C479@ccsecurityservice.com>
            # print(mail['Message-Id'])      <9F855EAA-679A-4220-9177-6399A372AB66@gmail.com>
            # print(mail[ 'Mime-Version'])     # 1.0 (Apple Message framework v1084)
            # print(mail[ 'X-Mailer'] )   # Apple Mail (2.1084)
            # exit(0)


        if mail['To'] is None:
            continue
        # if 'hkamberovic' in mail['To']:
        #     print("DEBUG: ")
        #     print(mail['To'])
        toEmails = mail['To'].replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')
        fromEmails = mail['From'].replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')
        to_emails = []
        for e in toEmails:
            if '@' in e:
                to_email = e.replace('<', '')
                to_email = to_email.replace('>', '')
                to_email  = to_email.replace(',', '')
                to_emails.append(to_email)
        from_emails = []
        for e in fromEmails:
            if '@' in e:
                from_email = e.replace('<', '')
                from_email = from_email.replace('>', '')
                from_email  = from_email.replace(',', '')
                from_emails.append(from_email)

        if '@' in mail['Message-Id']:
            message_id = mail['Message-Id'].replace('<', '')
            message_id = message_id.replace('>', '')
            message_id = message_id.replace('-', '')
            message_id = message_id.split('@')[0]
        else:
            message_id = ''

        subject = mail['Subject'] or ""

        dt_object = dt_object or ""
        message_id = message_id.replace('\t', '').replace('\r', '').replace('\n', '')  or ""

        for sentto in to_emails:
            case = {'category':'email','from_user': from_emails[0], 'to_user': sentto,
                    'subject_txt': subject[:45],'sent_timestamp':dt_object,
                    'msg_id':message_id.replace('\t', '').replace('\r', '').replace('\n', '')}

            results.append(case)


    df = pd.DataFrame(results)
    df.reset_index()
    df.index.name = 'Id'
    df['srcTmpId'] = df[['from_user']].sum(axis=1).map(hash)
    #   df['sourceId']= df.groupby(['from'])['srcTmpId'].rank(ascending=True)
    df['tgtTmpId'] = df[['to_user']].sum(axis=1).map(hash)
    #  df['targetId']= df.groupby(['to'])['tgtTmpId'].rank(ascending=True)
    df['sourceId'] = df.groupby(df['from_user'].tolist(), sort=False).ngroup() + 1
    df['targetId'] = df.groupby(df['to_user'].tolist(), sort=False).ngroup() + 1

    df["msg_id"] = df["msg_id"].str.encode("ascii", "ignore")
    df["msg_id"] = df["msg_id"].str.decode('UTF-8')
    df = df[['category','sourceId','from_user','targetId','to_user','sent_timestamp','subject_txt','msg_id']]

    print("Error count %i"%errcnt)
    return df


def open_csv_file(file_name):
    #WIP - GET EMAIL ALERT TIME DOWN
    #READ FILE
    df = pd.read_csv(os.getcwd()+"/"+file_name,encoding='utf-8',skiprows=9)
    return df


i = 30
subject_header = "Notice: Your Mortgage Statement Is Available"
subject_header = "Gala"
subject_header = 'Party'

c = details(subject_header,date=(dt.datetime.now()-dt.timedelta(i)).strftime("%d-%b-%Y"))
print("Search Criteria: "+ c)

pd_output = attachment_download(c)



pd_output.to_csv('email_all.csv',sep='|',index=True,header=True)

