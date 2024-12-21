import json
from rest_framework import views, response, status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from webhooks.models import WebHook
from webhooks.messages import outflow_message
from services.callmebot import CallMebot


class WebHookOrderView(views.APIView):
    
    def post(self, request):
        data = request.data

        WebHook.objects.create(
            event_type=data.get('event_type'),
            event=json.dumps(data, ensure_ascii=False)
        )

        product_name = data.get('product')
        quantity = data.get('quantity')
        product_selling_price = data.get('product_selling_price')
        product_cost_price = data.get('product_cost_price')
        total_value = product_selling_price * quantity
        profit_value = total_value - (product_cost_price * quantity)

        message = outflow_message.format(
            product_name,
            quantity,
            total_value,
            profit_value,
        )

        callmebot = CallMebot()
        callmebot.send_message(message)

        data['total_value'] = total_value
        data['profit_value'] = profit_value
        send_mail(
            subject='Nova Saída',
            message='',
            from_email=f'<{settings.EMAIL_HOST_USER}>',
            recipient_list=[settings.EMAIL_ADMIN_RECEIVER],
            html_message=render_to_string('outflow.html', data),
            fail_silently=False,
        )

        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )
