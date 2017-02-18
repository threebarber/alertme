# -*- coding: utf-8 -*-
import time
import requests
import smtplib
from timeit import default_timer as timer
from config import *


def send_email(user, pwd, recipient, subject, body): #snippet courtesy of david / email sending function
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd) #login to gmail server
        server.sendmail(FROM, TO, message) #actually perform sending of mail
        server.close() #end server
        print '[+]Successfully sent email notification' #alert user mail was sent
    except Exception, e: #else tell user it failed and why (exception e)
        print "[-]Failed to send notification email, " +str(e)

def main():
    print "[+]Starting up monitor on " +url+ ",notify on change detect is set to " +str(notify)
    start = timer()
    
    with requests.Session() as c:
        try:
            page1 = c.get(url) #base page that will be compared against
        except Exception, e:
            print "[-]Error Encountered during initial page retrieval: " +e
         
        while 1:
                time.sleep(wait_time) #wait beetween comparisons
        
                try:
                    page2 = c.get(url) #page to be compared against page1 / the base page
                except Exception, e:
                    print "[+]Error Encountered during secondary page retrieval: " +e
        
                if page1.content == page2.content: #if else statement to check if content of page remained same
                    end = timer()
                    if ((end-start)) >= 60:
                        timeMinutes = (end-start) / 60
                        print "[-]No Change Detected @ " +str(url)+ "\n[-]Elapsed Time: " +str(timeMinutes)+ " minutes"
                    else:
                        print '[-]No Change Detected @ ' +str(url)+ "\n[+]Elapsed Time: " +str((end-start))+ " seconds"
                    
                else:
                    end = timer()
                    if int((end-start)) >= 60:
                        timeMinutes = (end-start) / 60
                        print '[+]Change Detected  \n[+]Elapsed Time: ' +str(timeMinutes)+ " minutes" #if anything was changed - it sends an email alerting the user
                        if notify == True:
                            send_email(user, pwd, recipient, subject, body) #send notification email
                        else:
                            pass
                        print '\n[+]Retrieving new base page and restarting\n' 
                        main()
                    else:
                        print '[+]Change Detected  \n[+]Elapsed Time: ' +str((end-start))+ " seconds \n[+]Retrieving new base page and restarting\n"  #if anything was changed - it sends an email alerting the user
                        if notify == True:
                            send_email(user, pwd, recipient, subject, body) #send notification email
                        else:
                            pass
                        print '\n[+]Retrieving new base page and restarting\n'     
                        main()
                    
if __name__ == '__main__':
    main()



