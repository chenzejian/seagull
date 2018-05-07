from .celery import short_default
from django.core.mail import send_mail, send_mass_mail, EmailMessage, EmailMultiAlternatives
from .models import Email
from lib import utils


@short_default
def send_mail(email_id):
    # send_mail()
    # send_mail('Subject here', 'Here is the message.', '405048922@qq.com', \
    #     ['chenzejian304@163.com', 'chenzejian304@126.com'], fail_silently=False)

    # send_mass_mail()
    # message1 = ('Subject here', 'Here is the message', '405048922@qq.com', ['chenzejian304@163.com', 'chenzejian304@126.com'])
    # message2 = ('Another Subject', 'Here is another message', '405048922@qq.com', ['chenzejian304@163.com'])
    # send_mass_mail((message1, message2), fail_silently=False)

    # EmailMessage类
    # message = EmailMessage('Hello', 'Body goes here', '405048922@qq.com',
    #         ['chenzejian304@163.com'], ['chenzejian304@126.com'],
    #         reply_to=['405048922@qq.com'], headers={'Message-ID': 'foo'})
    # img_data = 'lalalalalala'
    # message.attach('design.png', img_data, 'image/png')
    # message.attach_file('/home/chenzejian/www/ym-email/design.png')
    # message.send()

    # EmailMultiAlternatives类
    # subject, from_email, to = 'hello', '405048922@qq.com', 'chenzejian304@163.com'
    # text_content = 'This is an important message.'
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    email = Email.objects.get(id=email_id)
    
    subject = email.title 
    html_content = email.content
    from_user = email.from_user
    receive_user = email.receive_user.split(',') 
    cc_user = email.cc_user.split(',') 
    send_type = Email.SEND_TYPE_NAME[email.send_type]
    email.send_times=email.send_times+1
    email.save()

    if send_type == 'mailgun':
        utils.mailgun_send_email(receive_user, subject, html_content, from_user)
    elif send_type == 'qqsmtp':
        # 配置里写的就是qq smtp服务
        msg = EmailMessage(subject, html_content, from_user, receive_user, cc_user)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
    elif send_type == 'self_service':
        pass
    else:
        raise 