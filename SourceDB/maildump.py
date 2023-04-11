#!/usr/bin/env python
#
# maildump.py
#
# Very simple Python script to
# 1st dump all emails within an IMAP account to files, and
# 2nd extract header and attachments from the dumped email
# files.
#
# This code bases on:
# - the script of Rob Iwancz (robulouski) 
#   (see https://gist.github.com/robulouski/7442321 )
# - and on an example from the Python documentation
#   (see https://docs.python.org/3/library/email-examples.html)
#
#
# This code is released into the public domain.
#
# honel // September 02, 2014
#
import sys
import imaplib
import getpass
import email
import mimetypes
from email.parser import Parser
from numpy import asarray
from time import sleep

#
# Edit the following lines with the respective IMAP
# account information and then run the program.
#
IMAP_SERVER = 'imap.gmail.com' # IMAP server
EMAIL_ACCOUNT = "orob5280@gmail.com" # Login name
OUTPUT_DIRECTORY = './out' + '/' # directory for dumped emails, make sure it ends with a slash 
PASSWORD = 'tebdxqvaptuosszk' # getpass.getpass() # do not edit this line


#
# BEGIN
#
def filename(num,filetype,email_folder):
    """
    Generate a string to use as filename
    """
    DIGITCOUNT=4         # number of leading zeros 
    filename= OUTPUT_DIRECTORY + email_folder + 'mail-' +  str(num).zfill(DIGITCOUNT)  +  filetype
    return filename

def listMailboxes(M):
    """
    Return list of mailboxes
    """
    rv, mailboxes = M.list()
    if rv != 'OK':
        sys.exist(5)
    mailboxlist=['BofA']
    # for mailbox in mailboxes:
    #    mailboxlist.append(mailbox.split('"')[-2])
    return ['BofA']

def postprocess_mail(num,folder):
    """
    Extract header and attachments from dumped files
    """
    fileRead=open(filename(num,".eml",folder), 'r')
    msg_headers = Parser().parse(fileRead)
    fileRead.close()
    fileWrite = open(filename(num,"-head.txt",folder), 'wb')
    fileWrite.write('Date: %s\n' % msg_headers['date'])
    fileWrite.write('From: %s\n' % msg_headers['from'])
    fileWrite.write('To: %s\n' % msg_headers['to'])
    fileWrite.write('CC: %s\n' % msg_headers['cc'])
    fileWrite.write('BCC: %s\n' % msg_headers['bcc'])
    fileWrite.write('\n')
    fileWrite.close()
    fileRead = open(filename(num,".eml",folder), 'r')
    msg = email.message_from_file(fileRead)
    fileRead.close()
    counter = 1
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue                                          # multipart/* are just containers
        fname = part.get_filename()
        if not fname:
            ext = mimetypes.guess_extension(part.get_content_type())
            if ext!= None :
                fname = 'part-'+str(counter).zfill(2)+ext
            else:
                fname = 'part-'+str(counter).zfill(2)+".none"
        fname=fname.replace("/", "-")
        counter +=1
        fileWrite = open(filename(num,"-"+fname,folder), 'wb')
        if not part.get_payload(decode=True)==None:
            fileWrite.write(part.get_payload(decode=True))
        else:
            print( "Attachment of mail /", filename(num,".eml",folder), " is empty:", fname)
        fileWrite.close()

def process_mailbox(M,folder):
    """
    Dump all emails in the folder to files in output directory.
    """
    rv, data = M.search(None, "ALL") # filter list of eMails, e.g.,
    # rv, data = M.search(None,'(FROM "Alice")')
    # rv, data = M.search(None,'(TO "Bob")')
    mailcount= asarray(data[0].split(" "))[-1]

    if rv != 'OK':
        print ("No messages found!" )
        sys.exist(1)
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print ("ERROR getting message", num )
            sys.exit(10)
            return
        print ("Processing Message ", num, " Of ", mailcount )
        fileWrite = open(filename(num,'.eml',folder), 'wb') # open a file to which email is dumped
        fileWrite.write(data[0][1]) # dump email
        fileWrite.close() # close file to which email was dumped to
        postprocess_mail(num,folder) # post-process dumped message

def main():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    print ("Names of the found " + str(len(listMailboxes(M))) + " Folders:",  listMailboxes(M) )
    print ("Programm will proceed in 10 seconds. Press CRTL+C to cancel program now."  )
    sleep(2)
    # exit(0)
    for mailbox in listMailboxes(M):
        rv, data = M.select(mailbox)
        if rv == 'OK':
            print( "=======================" )
            print( "Processing mailbox: ", mailbox )
            print ("======================="   )
            process_mailbox(M,mailbox)
            M.close()
        else:
            print ("ERROR: Unable to open mailbox ", rv  )
    M.logout()

if __name__ == "__main__":
    main()
#
# END
#