'''
Created on Sep 29, 2011

@author: Alexander
'''
from tipfy import RequestHandler
from google.appengine.api import mail

class MailSender(RequestHandler):
        def post(self):
            to = self.request.form.get('to')
            subject = self.request.form.get('subject')
            body = self.request.form.get('body')
            mail.send_mail("alex.milano@gmail.com", to, subject, body)
            return to

class MailBulkSender(RequestHandler):
        def post(self):
            to = self.request.form.getlist('to')
            subject = self.request.form.get('subject')
            body = self.request.form.get('body')
            mail.send_mail("alex.milano@gmail.com", to, subject, body)
            return to
                