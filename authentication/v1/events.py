from event_driven.producer.events.events import LogEvent
from event_driven.producer.producers import Producer
from event_driven.producer.serializers import LogEventSerializer


def sign_up_event_adapter(phone_number, created):
    if created:
        log_event_data = {
            "name": "user_created",
            "source": "sign_up",
            "level": "info",
            "message": f"User registered: {phone_number} and recieved otp.",
        }

    else:
        log_event_data = {
            "name": "change_user_to_pending",
            "source": "sign_up",
            "level": "info",
            "message": f"User state changed to Pending: {phone_number} and then recieved otp.",
        }

    log_event = LogEvent(**log_event_data)
    serialized_log_event = LogEventSerializer(
        log_event.serializer_format).serialize(log_event)

    Producer().produce_message(serialized_message=serialized_log_event,
                               exchange_type='direct', exchange_name='logs', routing_key='info', delivery_mode=1)
