from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyWallet,WalletHistory,Payments
from Account.models import Notifications,Device,User
from Account.serializers import NotificationSerializer
from Account.firebase import send_push_notification
@receiver(post_save,sender=MyWallet)
def CreatedWallet(sender,instance,created,**Kwargs):
    if created:
        print(instance)
        try:
            user=User.objects.get(id=instance.user.id)
            device=Device.objects.get(User=user)
            notification_data={
                'notification_title':"Wallet Created",
                'notification_body':f'Hello '+instance.user.username+ 'Your Wallet is not Ready, Join now the journey of Kaz ni Kaz',
                'type': 'Self',
                'User': user.id
            }
            notification=NotificationSerializer(data=notification_data)
            if notification.is_valid():
                notification.save()
                send_push_notification(device.token,'Wallet Created',f'Hello '+instance.user.username+ 'Your Wallet is not Ready, Join now the journey of Kaz ni Kaz')
            else:
                print(notification.errors)    
        except Device.DoesNotExist:
            print('Error: Device does not exist')

@receiver(post_save,sender=WalletHistory)
def AnyActionOnWallet(sender,instance,created,**kwargs):
    if created:
        try:
            if instance.action=='Transfer':
                try:
                    reciever_device=Device.objects.get(User=instance.reciever.user)
                    sender_device=Device.objects.get(User=instance.wallet.user)
                except Device.DoesNotExist:
                    pass    
            else:
                device=Device.objects.get(User=instance.wallet.user)    
            notification_data={
                'notification_title':f"" + instance.action + " has been made SuccessFully",
                'notification_body':f'Dear '+instance.wallet.user.username+ 'Your' + instance.action + 'of '+ str(instance.amount)+' has been processed',
                'type': 'Self',
                'User': instance.wallet.user.id
            }
            if instance.action=='Transfer':
                notification_receiver_data={
                'notification_title':f" " + instance.action + " has been made SuccessFully",
                'notification_body':f'Dear '+ instance.reciever.user.username + ' Your' + instance.action + 'of '+ str(instance.amount) +' has been processed',
                'type': 'Self',
                'User': instance.reciever.user.id
                }
                notification_receiver_save=NotificationSerializer(data=notification_receiver_data)
                if notification_receiver_save.is_valid():
                    notification_receiver_save.save()
                    try:
                        send_push_notification(reciever_device.token,f'You Have Received ' +str(instance.amount) + ' on Your Kaz ni kaz Wallet',f'Dear ' + instance.reciever.username + 'You have Received' + str(instance.amount) + 'From' + instance.wallet.user.username)
                    except Exception as e:
                        print("failed to send notification to reciever",e)    
                else:
                    print(notification_receiver_save.errors)    
            notification=NotificationSerializer(data=notification_data)
            if notification.is_valid():
                notification.save()
                try:
                    send_push_notification(device.token,f'Dear '+instance.wallet.user.username + ' You have Successfully ' +instance.action ,' Explore the World ')
                except Exception as e:
                    print("failed to send notification to user",e)
            else:
                print(notification.errors)    
        except Device.DoesNotExist:
            print("Device does not exist")
@receiver(post_save,sender=Payments)
def PaymentStatus(sender,instance,created,**kwargs):
    # print("Signal prints",instance)
    try:
        wallet=MyWallet.objects.get(user=instance.payer)   
        if instance.status=='successful':
            try:
                history=WalletHistory.objects.get(payment_ref=instance.referenceKey)
                history.status=instance.status
                if instance.action=='Deposit':
                    wallet.amount=wallet.amount + instance.amount
                elif instance.action=='Withdraw':
                    wallet.amount=wallet.amount - instance.amount    
                wallet.save()
                history.save()
                print("WalletHistory prints",history)
            except WalletHistory.DoesNotExist:
                print('no history for this payment from signals') 
        elif instance.status=='failed':
              try:
                   history=WalletHistory.objects.get(payment_ref=instance.referenceKey)
                   history.status=instance.status
                   history.save()
              except WalletHistory.DoesNotExist:
                  print("wallet history for payment not found from Signals")                      
    except MyWallet.DoesNotExist:
        print("wallet not found",instance.payer)    