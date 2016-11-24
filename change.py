# -*- coding: utf-8 -*-
import time
import requests
import smtplib

#by threebones https://github.com/threebarber
start = timer()

def send_email(user, pwd, recipient, subject, body): #snippet courtesy of david / email sending function

    gmail_user = user
    gmail_pwd = pwd      #assign info to params
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try: #try to send mail except statement
        server = smtplib.SMTP("smtp.gmail.com", 587) #start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd) #login to gmail server
        server.sendmail(FROM, TO, message) #actually perform sending of mail
        server.close() #end server
        print 'successfully sent the mail' #alert user mail was sent
    except Exception, e: #else tell user it failed and why (exception e)
        print "failed to send mail, " +str(e)

def main(): #main function



    with requests.Session() as c:
        url        =      'https://SITETOWATCHHERE.com/'
        wait_time  =      10 #customizable time to wait to check for changes IE every 5 secs

        user            = '@gmail.com' #emailuser@gmail.com
        pwd             =  ''  #app password generated by google IE "djfj rubi sifu sofi"
        recipient       = '@gmail.com' #recievingemail@gmail.com
        subject         = 'SITE UPDATED' #message subject
        body            = 'CHANGE AT ' + str(url) #

        page1 = c.get(url) #base page that will be compared against

        time.sleep(wait_time) #wait inbeetween initial retrieval and comparison actions

        page2 = c.get(url) #page to be compared against page1 / the base page

        if page1.content == page2.content: #if else statement to check if content of page remained same
            end = timer()
            print "[-]No Change Detected @ " +str(url)+ "\n[-]Elapsed Time: " +str((end-start))+ " seconds"
        else:
            end = timer()
            print print '[+]Change Detected - \n[+]Elapsed Time: ' +str((end-start))+ " seconds"  #if anything was changed - it sends an email alerting the user

            send_email(user, pwd, recipient, subject, body) #send notification email

        page2  = None #clear page2 variable before looping through main function again

        #time.sleep(wait_time) optional wait beetween starting again

        main() #super simple easy loop method :)


if __name__ == "__main__": #start main function
    main()
