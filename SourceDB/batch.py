import imaplib
import email
import time as tm, os, glob
import datetime as dt
import pandas as pd
# userid , passwd= 'orob5280@gmail.com'  , 'tebdxqvaptuosszk''
userid, passwd  = 'owenr@dts5280.com',      'ihhxowrfazutbbil'

obj = imaplib.IMAP4_SSL('imap.gmail.com', 993)
obj.login(userid, passwd)
# obj.login('owenr@dts5280.com', 'ihhxowrfazutbbil')

# for i in obj.list()[1]:
#     print(i)

fld = '"[Gmail]/All Mail"'
# fld='Inbox'
fld = fld.encode()
# print("obj:",obj)
# print("fld",fld)
obj.select(fld)
# print("obj:",obj)
resp,data = obj.uid('FETCH', '1:*' , '(RFC822.HEADER)')
# print(data)
messages = [data[i][1].strip().decode('UTF-8') + "\r\nSize:" + data[i][0].split()[4].decode('UTF-8') + "\r\nUID:" + data[i][0].split()[2].decode('UTF-8')  for i in range(0, len(data), 2)]
print(len(data))
# for i in range(1,len(data)):
#     i=+1
#     messages = data[i][1].strip().decode('UTF-8')
#
# print(i)
results = []
for mail in messages:
    msg_str = email.message_from_string(mail)
    message_id = msg_str.get('Message-ID')
    message_from = msg_str.get('From')
    message_to = msg_str.get('To')
    message_date = msg_str.get('Date') or 'Mon, 01 Jan 2000 00:00:01 +0100'
    message_subject = msg_str.get('Subject')
    # print(message_date)

    dtimestamp = tm.mktime(email.utils.parsedate(message_date))
    dt_object = dt.datetime.fromtimestamp(dtimestamp)
    message_to = message_to or "default@unknown.com"
    message_from = message_from or "default@unknown.com"
    message_subject  = message_subject or "No Subject"
    if message_to is None:
    #   continue
        message_to = ''
        print(msg_str)
        # if 'hkamberovic' in mail['To']:
        #     print("DEBUG: ")
        #     print(mail['To'])
    toEmails = message_to.replace('"','').replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')
    fromEmails = message_from.replace('"','').replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')
    # print("Content Type:",msg_str.get('Content-Type'))
    # print("MIME-Version:",msg_str.get('MIME-Version'))
    # if 'Cosmic' in subject:
    #     print(msg_str)

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
            from_email = from_email.replace(',', '')
            if from_email != '@':
                from_emails.append(from_email)
    from_emails = from_emails or ["default@unknown.com"]
    if message_id:
        message_id = message_id.replace('<', '')
        message_id = message_id.replace('>', '')
        message_id = message_id.replace('-', '')
        message_id = message_id.split('@')[0]
    else:
        message_id = 'UNKNOWN'


    dt_object = str(dt_object) or ""
    message_id = message_id.replace('\r\n','').replace('\t', '') or ""

    subject = message_subject.replace('""', '').replace('""', '').replace('""', '').replace('""', '') or ""
    subject_cln = subject.encode('ascii', 'ignore').decode()
    subject_cln = subject_cln.replace('|', '##').replace('\t', '').replace('\r', '').replace('\n', '')
    if subject_cln.startswith("="):
        # print("Image value likely ",subject_cln)
        subject_cln = "image"

    messageId = message_id.replace('|', '').replace('\t', '').replace('\r', '').replace('\n', '')
    # print(type(
    node_prop = {}
    if subject:
        node_prop['subject'] = subject_cln
    # if messageId:
    #     node_prop['msg_id'] = messageId
    if dt_object:
        node_prop['event_dt'] = dt_object
    node_prop['source'] = userid

    for sentto in to_emails:
        case = {'category':'email',
                'from_user': from_emails[0],
                'to_user': sentto,
                'subject_txt':subject_cln, # .replace('\|', ''),
                'msg_id':messageId,
                'node_properties':node_prop }
        # print(type(case))
        results.append(case)
    # print(case)
df = pd.DataFrame(results)
df.reset_index()
df.index.name = 'Id'
df['srcTmpId'] = df[['from_user']].sum(axis=1).map(hash)
#    df['sourceId']= df.groupby(['from'])['srcTmpId'].rank(ascending=True)
#
df['tgtTmpId'] = df[['to_user']].sum(axis=1).map(hash)
#    df['targetId']= df.groupby(['to'])['tgtTmpId'].rank(ascending=True)
df['sourceId'] = df.groupby(df['from_user'].tolist(), sort=False).ngroup() + 1
df['targetId'] = df.groupby(df['to_user'].tolist(), sort=False).ngroup() + 1

# df.drop(columns=['srcTmpId'])
# df.drop(columns=['tgtTmpId'])
# df = df [['category','srcTmpId','tgtTmpId','sourceId','from','targetId','to','timestamp','subject','msg_id']]
# df["msg_id"] = df["msg_id"].str.encode("ascii", "ignore")
# df["msg_id"] = df["msg_id"].str.decode('UTF-8')
df = df[['category','sourceId','from_user','targetId','to_user','msg_id','node_properties']]
df.to_csv('email_orob.csv',sep='|',index=True,header=True)
