import hmac
import hashlib
import time
import json

class WebhookVerificationError(Exception):
    pass

class Webhook:
    def __init__(self, secret):
        self.secret = secret.encode('utf-8')

    def verify(self, payload, headers):
        message = headers['svix-id'].encode('utf-8')
        message += headers['svix-timestamp'].encode('utf-8')
        message += payload

        expected_signature = headers['svix-signature']

        calculated_signature = hmac.new(
            self.secret,
            msg=message,
            digestmod=hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(f'v1,{calculated_signature}', expected_signature):
            raise WebhookVerificationError('Invalid signature')

        return json.loads(payload)
