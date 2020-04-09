from django.core.management.base import BaseCommand
import requests

from project.apps.device42.models import DownloadModel, UpdateModel, ContactModel, ScheduleModel


CRMPUSERURL = 'https://registration.device42.com/api/1.0/addpotentialuser/'
#CRMPUSERURL = 'http://192.168.52.128:7000/api/1.0/addpotentialuser/'


class Command(BaseCommand):
  def handle(self, *args, **options):
    downloads = DownloadModel.objects.filter(clicky_cookie__isnull=False)
    for download in downloads:
      user_data = {'email': download.email,
                   'clicky_cookie': download.clicky_cookie, }  # 'reverse_lookup':digged, 'dazzle': ipjson, 'tzone': rawoffval }
      r = requests.post(CRMPUSERURL, data=user_data, verify=False)
      # print r.content
      if r.status_code == 200:
        print 'done'

    # updates = UpdateModel.objects.filter(id__gt=processed_table.id_processed_update)
    # for update in updates:
    #   # ipjson, rawoffval, digged  = resolve_ip(update[5].strip())
    #   user_data = {'email': update.email,
    #                'time_linked': update.time_linked,
    #                'ip_addresses': update.ip_address,
    #                'first_action': 'update', }  # 'reverse_lookup':digged, 'dazzle': ipjson, 'tzone': rawoffval }
    #   r = requests.post(CRMPUSERURL, data=user_data, verify=False)
    #   # print r.content
    #   if r.status_code == 200:
    #     processed_table.id_processed_update = update.id
    #     processed_table.full_clean()
    #     processed_table.save()

    contacts = ContactModel.objects.filter(clicky_cookie__isnull=False)

    for contact in contacts:

      user_data = {'email': contact.email, 'clicky_cookie': contact.clicky_cookie, }
      r = requests.post(CRMPUSERURL, data=user_data, verify=False)
      # print r.content
      if r.status_code == 200:

        print 'done'

    schedule_demos = ScheduleModel.objects.filter(clicky_cookie__isnull=False)
    for schedule_demo in schedule_demos:
      user_data = {'email': schedule_demo.email,
                   'clicky_cookie': contact.clicky_cookie, }
      r = requests.post(CRMPUSERURL, data=user_data, verify=False)
      # print r.content
      if r.status_code == 200:
        print 'done'
