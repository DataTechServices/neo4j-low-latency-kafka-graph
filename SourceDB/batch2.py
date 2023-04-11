import imaplib
import email
import time as tm, os, glob , re
import datetime as dt
import pandas as pd

obj = imaplib.IMAP4_SSL('imap.gmail.com', 993)
# obj.login('orob5280@gmail.com', 'tebdxqvaptuosszk')
obj.login('owenr@dts5280.com', 'ihhxowrfazutbbil')

folders = obj.list()
for fld in folders[1]:
    folder = fld.decode('UTF-8')
    print("Folder:",folder)
    for allfolders in re.findall('"\/"(.*)',folder):

        finalfolders = allfolders.replace(" ",' ')

        obj.select(finalfolders, readonly=True)
        print("Final Folders:",finalfolders)
        # typ, data = obj.search(None, 'ALL')

        # obj.select('Inbox')
        resp,data = obj.uid('FETCH', '1:*' , '(RFC822.HEADER)')
        print(resp,data)
        print ("data type",type(data),len(data))
        print(obj)
        if data[0] is None:
            continue
        exit()
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
            message_date = msg_str.get('Date')
            message_subject = msg_str.get('Subject')


            dtimestamp = tm.mktime(email.utils.parsedate(message_date))
            dt_object = dt.datetime.fromtimestamp(dtimestamp)
            message_to = message_to or "default@unknown.com"
            message_from = message_from or "default@unknown.com"
            message_subject  = message_subject or ""
            if message_to is None:
            #   continue
                message_to = ''
                print(msg_str)
                # if 'hkamberovic' in mail['To']:
                #     print("DEBUG: ")
                #     print(mail['To'])
            toEmails = message_to.replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')
            fromEmails = message_from.replace(';',' ').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace(',',' ').split(' ')


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

            if '@' in message_id:
                message_id = message_id.replace('<', '')
                message_id = message_id.replace('>', '')
                message_id = message_id.replace('-', '')
                message_id = message_id.split('@')[0]
            else:
                message_id = ''

            subject = message_subject or ""
            # from_email[0] = from_email[0] or ""
            dt_object = dt_object or ""
            message_id = message_id.replace('\r\n','').replace('\t', '') or ""
            # print("Content Type:",msg_str.get('Content-Type'))
            # print("MIME-Version:",msg_str.get('MIME-Version'))

            # if 'Cosmic' in subject:
            #     print(msg_str)
            subject_cln = subject.encode('ascii', 'ignore').decode()
            subject_cln = subject_cln.replace('|', '##').replace('\t', '').replace('\r', '').replace('\n', '')

            if subject_cln.startswith("="):
                # print("Image value likely ",subject_cln)
                subject_cln="image"
            for sentto in to_emails:
                case = {'category':'email','from_user': from_emails[0], 'to_user': sentto,
        #                 'subject_txt': subject[:100].replace('\|', '').replace('"', '').replace('\r', '').replace('\n', ''),
                    'subject_txt':subject_cln, # .replace('\|', ''),
                    'sent_timestamp':dt_object,
                    'msg_id':message_id.replace('|', '').replace('\t', '').replace('\r', '').replace('\n', '')}
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
df["msg_id"] = df["msg_id"].str.encode("ascii", "ignore")
df["msg_id"] = df["msg_id"].str.decode('UTF-8')
df = df[['category','sourceId','from_user','targetId','to_user','sent_timestamp','subject_txt','msg_id']]
df.to_csv('email_dts.csv',sep='|',index=True,header=True)
