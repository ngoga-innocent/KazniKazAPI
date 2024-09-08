from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import MyWallet,WalletHistory,Payments
from rest_framework.response import Response
from django.http import JsonResponse
from .Serializer import WalletHistorySerializer,MyWalletSerializer
from .SendEmail import sending_email
from paypack.client import HttpClient
from paypack.transactions import Transaction
from paypack.events import Event
from paypack.oauth2 import Oauth
from paypack.merchant import Merchant
import requests
import json
import time
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.utils.decorators import method_decorator
client_id="4645d206-48c1-11ef-a6a2-deade826d28d", 
client_secret="76ff484a244047ecbbc3ffeca5dc79a3da39a3ee5e6b4b0d3255bfef95601890afd80709"
# client_id="66d24278-48cd-11ef-82f6-deade826d28d"
# client_secret="238196c663cfa65f6c0220db4426733cda39a3ee5e6b4b0d3255bfef95601890afd80709"
Base_url="https://payments.paypack.rw/api"

# Create your views here.
def mozilla_browser_redirect(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
        return view_func(request, *args, **kwargs)
    return wrapper
class WalletView(APIView):
   
    permission_classes=[IsAuthenticated]
    @method_decorator(mozilla_browser_redirect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        if 'Mozilla' in request.META.get('HTTP_USER_AGENT', ''):
            return redirect('web_products')
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
        if not request.data['action']:
            return Response({"detail":"No action"},status=400)
        action=request.data['action']
        amount=request.data['amount']
        api_key = request.headers.get('X-API-KEY')
        
        if api_key != 'KazniKazSecuritykey_0782214360':
            return Response({"detail":"Invalid API key."},status=401)
        if action is None:
            return Response({"detail":"Action is required"},status=400)
       
        try:
           
            
            wallet=MyWallet.objects.get(user=request.user)
            if action=='Deposit':
                phone_number=request.data['phone_number']
                cashin=self.Deposit(amount,phone_number,"Deposit")
                # print(cashin.json().get('ref'))
                if cashin.status_code==200:
                    amount=amount-(amount*0.02)
                    # print("status _code verified")
                    history=WalletHistory.objects.create(
                        wallet=wallet,
                        action=action,
                        amount=amount,
                        payment_ref=cashin.json().get('ref')
                    )
                    # previous=wallet.amount
                    # wallet.amount= previous+ amount
                    # wallet.save()
                    
                    # wallet.save()
                    # sending_email(request.user,'Deposit made Successfully',f'Dear ' + request.user.username + ' Your Deposit of ' + str(amount) +' Rwf has been made successfully ')
                    walletSerializer=MyWalletSerializer(wallet)
                    HistorySerializer=WalletHistorySerializer(history)
                    return Response({"data":{
                        "wallet":walletSerializer.data,
                        "history":HistorySerializer.data
                    }})
                else:
                     return Response({"detail":"Payment Failed"},status=400)
            if amount > wallet.amount and action !='Deposit':
                    return Response({"detail":"insuficient Amount"},status=400)
            if action=='Withdraw':
                phone_number=request.data['phone_number']
                cashout=self.Withdraw(amount,phone_number,"Withdraw")
                if cashout.status_code==200:

                    ref=cashout.json().get('ref')
                    history=WalletHistory.objects.create(
                        wallet=wallet,
                        action='Withdraw',
                        amount=amount,
                        payment_ref=ref
                    )
                    # wallet.save()
                    # sending_email(request.user,'Withdraw made Successfully',f'Dear ' + request.user.username + ' Your Withdraw of ' + str(amount) +' Rwf has been made successfully ')
                    walletSerializer=MyWalletSerializer(wallet)
                    HistorySerializer=WalletHistorySerializer(history)
                    return Response({"data":{
                        "wallet":walletSerializer.data,
                        "history":HistorySerializer.data
                    }})
            if action =='Transfer':
                reciever=request.data['reciever']
                if amount < 1000:
                    return Response({"detail":"Transfer amount should not be less Than 1000 Rwf"},status=400)
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
                    }},status=200)
                except MyWallet.DoesNotExist:
                    return Response({'details':'Selected Receiver is not Available'},status=400)
        except MyWallet.DoesNotExist:
            return Response({"detail":"Wallet Doesn't exist"},status=404)
    def authorization(self):
        url = "https://payments.paypack.rw/api/auth/agents/authorize"
        payload = json.dumps({
        "client_id": "4645d206-48c1-11ef-a6a2-deade826d28d",
        "client_secret":client_secret
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)  
        # print(response.json())
        return response.json()

    def Deposit(self,amount,phone_number,action):
          url=f'{Base_url}/transactions/cashin'
          payload = json.dumps({
            "amount": amount,
            "number": phone_number
            })
        #   print(self.authorization()['access'])
          headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.authorization()["access"]}',
            'X-Webhook-Mode':'production'
            }
          response = requests.request("POST", url, headers=headers, data=payload)
          print(response.json())
          if response.status_code==200:
              ref=response.json().get('ref')
              status=response.json().get('status')
              amount=response.json().get('amount')
              user=self.request.user
              Payments.objects.create(referenceKey=ref, amount=amount, payer=user,status=status,number=phone_number,action=action)
          ref=response.json().get('ref')
          
                
          return response
    def Withdraw(self,amount,phone_number,action):
        url = f"{Base_url}/transactions/cashout"

        payload = json.dumps({
        "amount": amount,
        "number": phone_number
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.authorization()["access"]}',
        'X-Webhook-Mode':'production',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.json())
        if not response.status_code:
            return response.json()
        elif response.status_code==200:
              ref=response.json().get('ref')
              status=response.json().get('status')
              amount=response.json().get('amount')
              user=self.request.user
              Payments.objects.create(referenceKey=ref, amount=amount, payer=user,status=status,number=phone_number,action=action)
              return response
        

    def CheckTransaction(self,referenceKey):
        url=f'{Base_url}/events/transactions?ref={referenceKey}'
        
        payload={}
        headers = {'Authorization': f'Bearer {self.authorization()["access"]}'}

        response = requests.request("GET", url, headers=headers, data=payload)
        transaction_status=response.json()
        print(transaction_status)
        status=transaction_status['transactions'][0].get('data')['status']
        print(status)
        if transaction_status['total']>1:
            try:
                payment=Payments.objects.get(referenceKey=referenceKey)
                payment.status=status
            except Payments.DoesNotExist:
                return False


        return status    
    def cashin(self):
        HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
        cashin = Transaction().cashin(amount=100, phone_number="0782214360")
        
        print(cashin)
      
        return Response({"text":"okay"})
    def cashout(self):
        HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
        cashout = Transaction().cashout( amount=100,phone_number="0782214360")
        print(cashout)
        return cashout
def events(request):
        HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
        kind='cashout'  
        limit=10
        offset=0
        all_events = Event().list(limit)

        print(all_events)
        return JsonResponse({"events": all_events})
def AdminAccount(request):
    HttpClient(client_id="66d24278-48cd-11ef-82f6-deade826d28d", client_secret=client_secret)
    account=Merchant().me()
    # print(Merchant().me())
    return JsonResponse({"account": account})
    
      
@csrf_exempt
def Webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Webhook data:", data)
            
            # Now you can access the fields directly
            event_id = data.get('event_id')
            kind = data.get('kind')
            transaction_data = data.get('data', {})
            ref = transaction_data.get('ref')
            status = transaction_data.get('status')
            amount = transaction_data.get('amount')
            try:
                payment=Payments.objects.get(referenceKey=ref, amount=amount)
                payment.status = status
                payment.save()
            except: 
                return JsonResponse({"status":"payment not found"})  
            return JsonResponse({"status": "success", "data": data})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
       

        
