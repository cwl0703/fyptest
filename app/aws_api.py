import boto3
from botocore.exceptions import ClientError
from datetime import datetime

class amazonApi:
    
    def __init__(self):
        self.client = boto3.client('pinpoint')
        self.awsRegion = 'ap-south-1'
        self.awsAppId = '4f29848d50ba4cd2a1b45fd1e9b6523d'
        self.senderId = 'TESTING_USER'
        
    def sendSMSCode(self,mobile, code):
        try:
            response = self.client.send_messages(ApplicationId=self.awsRegion, MessageRequest={
            'Addresses':{
              mobile:{'ChannelType':'SMS'}},
            'MessageConfiguration':{
              'SMSMessage':{'Body':code,'MessageType':'TRANSACTIONAL','senderId':self.senderId}}
          })
        except ClientError as e:
            print(e.response['Error']['Message'])
            return e.response['Error']['Message']
        else:
            print("Message sent!")
            return "Message sent!"
            
            
    def sendEmailCode(self,email, code, location):
        emailTemplate = self.client.get_email_template(TemplateName='Send_SMS_Code', Version='latest')
        try:
            response = self.client.send_messages(ApplicationId=self.awsAppId, MessageRequest={
                'Addresses':{
                email:{'ChannelType':'EMAIL'}},
                'MessageConfiguration':{
                    'EmailMessage':{'FromAddress':'carousell@gmail.com',
                    'SimpleEmail':{
                        'HtmlPart':{
                            'Data': self.getEmailTemplate(emailTemplate['EmailTemplateResponse']['HtmlPart'],email,code,location)
                        },
                        'Subject':{
                            'Data':emailTemplate['EmailTemplateResponse']['Subject']
                        }}}}})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return e.response['Error']['Message']
        else:
            print("Message sent!")
            return "Message sent!"
            
            
    def getEmailTemplate(self, template, email, code, location):
        template.replace("{User.Email}", email)
        template.replace("{User.Code}", code)
        now = datetime.now()
        template.replace("{App.Timezone}",now.strftime("%d/%m/%Y %H:%M:%S"))
        template.replace("{App.Location}", location);
        template.replace("{App.Name}", 'Carousell Shop')
        return template