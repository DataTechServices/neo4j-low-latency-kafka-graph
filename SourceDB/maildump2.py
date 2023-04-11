import pandas as pd
import datetime, time, os, glob
import email, imaplib
# from email.parser import HeaderParser
#%%
cwd = os.getcwd()

EMAIL_UN = 'orob5280@gmail.com'
EMAIL_PW = 'tebdxqvaptuosszk'
#%%
subject_header = "Notice: Your Mortgage Statement Is Available"
subject_header = "Honeywell"


#%%
def details(subject_header,date=(datetime.datetime.now()-datetime.timedelta(1)).strftime("%d-%b-%Y")):
    #EMAIL SEARCH CRITERIA
    search_criteria = '(ON '+date+' SUBJECT "'+subject_header+'")'
    search_criteria = '(SUBJECT "'+subject_header+'")'
    return search_criteria
#%%
def attachment_download(SUBJECT):
    un = EMAIL_UN
    pw = EMAIL_PW
    url = 'imap.gmail.com'
    cnt = 0

    detach_dir = '.' # directory where to save attachments (default: current)
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL(url,993)
    m.login(un,pw)

    m.select('Inbox')
    resp, items = m.search(None, '(FROM "Cat Tatman")')
    # resp, items = m.search(None, 'ALL')
    print("Searching for emails with: "+SUBJECT)
    # resp, items = m.search(None, SUBJECT)


# you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)

    items2 = items[0].split() #.decode('UTF-8') # getting the mails id
    items = [x.decode('UTF8') for x in items2]
    results = []
    # items = items2.decode('UTF-8')
    for emailid in items:
        cnt+= 1
        if cnt > 100:
            break

        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        try:
            email_body = data[0][1].decode('UTF-8') # getting the mail content
        except Exception:
            continue

        # email_body = data[0][1].decode('UTF-8') # getting the mail content
        mail = email.message_from_string(str(email_body)) # parsing the mail content to get a mail object
        # print(mail.get_content_maintype()+"  ["+mail["From"]+"] :" + mail["Subject"])

        dtimestamp=time.mktime(email.utils.parsedate(mail['Date']))


        printit = False
        if printit == True:
            print("Mail Message Header: ", end="|")
            print(mail['Return-Path'], end="|")
            # print(mail['Received'])     # mail server/routing info
            print(mail['From'], end="|")
            # print(mail['Content-Type'])   multipart/alternative; boundary=Apple-Mail-211--633876483
            print(mail['Subject'], end="|")
            dtimestamp=time.mktime(email.utils.parsedate(mail['Date']))
            print(dtimestamp, end="|")
            # print(mail['References'])   <EEF25BC7-AF75-4365-997C-80D3E4C6C479@ccsecurityservice.com>
            print(mail['To'], end ="\n")
            # print(mail['Message-Id'])      <9F855EAA-679A-4220-9177-6399A372AB66@gmail.com>
            # print(mail[ 'Mime-Version'])     # 1.0 (Apple Message framework v1084)
            # print(mail[ 'X-Mailer'] )   # Apple Mail (2.1084)
            # exit(0)
        if mail['To'] is None:
            continue
        # if 'hkamberovic' in mail['To']:
        #     print("DEBUG: ")
        #     print(mail['To'])
        toEmails = mail['To'].replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').split(' ')
        fromEmails = mail['From'].replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').split(' ')


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


        for sentto in to_emails:
            case = {'from': from_emails[0], 'to': sentto, 'subject':mail['Subject'],
                'FROM':mail['From'],'TO':mail['To']}
            # print(type(case))
            results.append(case)
        '''
        output format of From, MessageId,Subject,Date
        pivot To: 
        '''
        # print("FROM: ", end=" ")
        # print(from_email,end="  :  ")
        # print("TO: ", end=" ")
        # print(to_emails)
    df = pd.DataFrame(results)
    # df.style()
    print(df.to_csv(index=True) )


        # return
def print_multipart(mail):
        #Check if any attachments at all
        if mail.get_content_maintype() != 'multipart':
            return



        # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
        counter = 1
        for part in mail.walk():
            filename = part.get_filename()
            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1
                # print("Setting Filename:"+filename)

        # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                return
            # is this part an attachment:
            if part.get('Content-Disposition') is None:
                return

            # print("Filename:"+filename)

            # if there is no filename, we create one with a counter to avoid duplicates

        att_path = os.path.join(detach_dir, filename)

            #Check if its already there
        if not os.path.isfile(att_path):
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
        # print(str(filename)+ ' downloaded')
        return filename

def attachment_download2(SUBJECT):
    un = EMAIL_UN
    pw = EMAIL_PW
    url = 'imap.gmail.com'

    detach_dir = '.' # directory where to save attachments (default: current)
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL(url,993)
    m.login(un,pw)
    m.select('BofA')
    print(m)
    resp, items = m.search(None, 'ALL')
    print(resp)
    # print(items)
    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)

    items = items[0].split() # getting the mails id

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)") # RFS822 fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1].decode("utf-8") # getting the mail content
        mail = email.message_from_string(str(email_body)) # parsing the mail content to get a mail object

        # print("["+mail["From"]+"] :" + mail["Subject"])
        #Check if any attachments at all
        if mail.get_content_maintype() != 'multipart':
            continue

        print("["+mail["From"]+"] :" + mail["Subject"])

        # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment:
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            counter = 1

            # if there is no filename, we create one with a counter to avoid duplicates
            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1

            att_path = os.path.join(detach_dir, filename)
            print("MSG:"+part.get_payload(decode=True))
            #Check if its already there
            if not os.path.isfile(att_path):
                # finally write the stuff
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        print(str(filename)+ ' downloaded')
        return filename
#%%
def open_csv_file(file_name):
    #WIP - GET EMAIL ALERT TIME DOWN
    #READ FILE
    df = pd.read_csv(os.getcwd()+"/"+file_name,encoding='utf-8',skiprows=9)
    return df
#%%
i = 30
subject_header = "Notice: Your Mortgage Statement Is Available"
subject_header = "Gala"

c = details(subject_header,date=(datetime.datetime.now()-datetime.timedelta(i)).strftime("%d-%b-%Y"))
print("Search Criteria: "+ c)
#%%
file_name = attachment_download(c)
# print(file_name)
#%%



#%%
# df = open_csv_file(file_name)
#%%
print(file_name)