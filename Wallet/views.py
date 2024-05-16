from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import MyWallet,WalletHistory
from rest_framework.response import Response
from .Serializer import WalletHistorySerializer,MyWalletSerializer
from .SendEmail import sending_email
# Create your views here.
class WalletView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        try:
            wallet=MyWallet.objects.get(user=user)
            history=WalletHistory.objects.filter(wallet=wallet).order_by('-created_at')
            serializer=MyWalletSerializer(wallet)
            historySerializer=WalletHistorySerializer(history,many=True)
            if len(history)>0:
               
                return Response({"wallet":serializer.data,"history":historySerializer.data},status=200)
            else:
                
                return Response({"wallet":serializer.data,"history":None},status=200)
        except MyWallet.DoesNotExist:
            return Response({'detail':'Wallet Does\'t exist'},status=404)
    def post(self,request):
        user=request.user
        try:
            MyWallet.objects.get(user=user)
            return Response({'detail':f'wallet for this user exists'},status=400)
        except MyWallet.DoesNotExist:
            data={'user':user.id}
            seriazer=MyWalletSerializer(data=data,context={"request":user})
            
            if seriazer.is_valid():
                seriazer.validated_data['user']=user
                seriazer.save()
                return Response({"wallet":"Wallet created successfully"},status=200)
            else:
                return Response({"details":seriazer.errors},status=401)
            
    def put(self,request):
        action=request.data['action']
        amount=request.data['amount']
        try:
            wallet=MyWallet.objects.get(user=request.user)
            if action=='Deposit':
                previous=wallet.amount
                wallet.amount= previous+ amount
                wallet.save()
                history=WalletHistory.objects.create(
                    wallet=wallet,
                    action='Deposit',
                    amount=amount
                )
                wallet.save()
                sending_email(request.user,'Deposit made Successfully',f'Dear ' + request.user.username + ' Your Deposit of ' + str(amount) +' Rwf has been made successfully ')
                walletSerializer=MyWalletSerializer(wallet)
                HistorySerializer=WalletHistorySerializer(history)
                return Response({"data":{
                    "wallet":walletSerializer.data,
                    "history":HistorySerializer.data
                }})
            if amount > wallet.amount:
                    return Response({"detail":"insuficient Amount"},status=400)
            if action=='Withdraw':
               
                wallet.amount-=amount

                history=WalletHistory.objects.create(
                    wallet=wallet,
                    action='Withdraw',
                    amount=amount
                )
                wallet.save()
                sending_email(request.user,'Withdraw made Successfully',f'Dear ' + request.user.username + ' Your Withdraw of ' + str(amount) +' Rwf has been made successfully ')
                walletSerializer=MyWalletSerializer(wallet)
                HistorySerializer=WalletHistorySerializer(history)
                return Response({"data":{
                    "wallet":walletSerializer.data,
                    "history":HistorySerializer.data
                }})
            if action =='Transfer':
                reciever=request.data['reciever']
                try:
                    reciever_object=MyWallet.objects.get(user=reciever)
                
                    wallet.amount-=amount
                    reciever_object.amount =+amount
                    history=WalletHistory.objects.create(
                        wallet=wallet,
                        action='Withdraw',
                        amount=amount
                    )
                    wallet.save()
                    reciever_object.save()
                    sending_email(request.user,'Transfer made Successfully',f'Dear ' + request.user.username + ' Your Transfer of ' + str(amount) +' Rwf has been made successfully ')
                    sending_email(reciever_object.user,'Transfer made Successfully',f'Dear ' + reciever_object.user.username + ' Your Transfer of ' + str(amount) +' Rwf has been made successfully transfered to your account ')
                    walletSerializer=MyWalletSerializer(wallet)
                    HistorySerializer=WalletHistorySerializer(history)
                    return Response({"data":{
                        "wallet":walletSerializer.data,
                        "history":HistorySerializer.data
                    }})
                except MyWallet.DoesNotExist:
                    return Response({'details':'Selected Receiver is not Available'},status=400)
        except MyWallet.DoesNotExist:
            return Response({"detail":"Wallet Doesn't exist"},status=404)
        
