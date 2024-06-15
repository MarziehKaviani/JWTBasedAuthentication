from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from modeltranslation.translator import translator

# @receiver(post_save)
# def override_translated_fields(sender, instance, **kwargs):
#     if sender in translator._registry:
#         translation_options = translator.get_options_for_model(sender)
#         for field in translation_options.fields:
#             english_value = getattr(instance, f"{field}_en", None)
#             if english_value is not None:
#                 setattr(instance, field, english_value)
