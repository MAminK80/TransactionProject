from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db import transaction


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    difference = models.FloatField(default=0)
    transaction_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.balance < 0:
            raise ValidationError('Balance can not be less than zero', code='balance_less_zero')


class Sell(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='sell')
    phone_number = models.CharField(max_length=100)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.phone_number

    def clean(self):
        if self.seller.balance < 0:
            raise ValidationError('Balance can not be less than zero', code='balance_sell_less_zero')


class Transaction(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transaction')
    charge = models.FloatField(default=0)
    withdraw = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.seller.user.username

    def clean(self):
        if self.seller.balance < 0:
            raise ValidationError('Balance can not be less than zero', code='balance_transaction_less_zero')

    def clean_charge(self):
        if self.charge < 0:
            raise ValidationError('Charge can not be less than zero')
        return self.charge

    def clean_withdraw(self):
        if self.withdraw < 0:
            raise ValidationError('Withdraw can not be less than zero')
        return self.withdraw


@receiver(post_save, sender=Transaction)
def transaction_signal(instance, created, *args, **kwargs):
    try:
        with transaction.atomic():
            if created & instance.active:
                seller = Seller.objects.get(id=instance.seller.id)
                seller.balance = seller.balance + instance.charge - instance.withdraw
                if seller.balance >= 0:
                    seller.transaction_active = False
                    seller.save()

                else:
                    raise ValidationError('Balance can not be less than zero')

    except IntegrityError:
        raise IntegrityError


@receiver(post_save, sender=Sell)
def sell_signal(instance, created, *args, **kwargs):
    try:
        with transaction.atomic():
            if created:
                seller = Seller.objects.get(id=instance.seller.id)
                seller.balance = seller.balance - instance.amount
                if seller.balance >= 0:
                    seller.transaction_active = False
                    seller.save()
                else:
                    raise ValidationError('Balance can not be less than zero')
    except IntegrityError:
        raise IntegrityError


@receiver(pre_save, sender=Seller)
def before_change_balance(instance, *args, **kwargs):
    try:
        with transaction.atomic():
            if instance.id:
                last_balance = Seller.objects.get(user=instance.user).balance
                amount = instance.balance - last_balance

            else:
                amount = instance.balance
            instance.difference = amount

    except IntegrityError:
        raise IntegrityError


@receiver(post_save, sender=Seller)
def after_change_balance(instance, created, *args, **kwargs):
    try:
        with transaction.atomic():
            if instance.transaction_active:
                Transaction.objects.create(seller=instance, charge=instance.difference, active=False)
                instance.transaction_active = True

    except IntegrityError:
        raise IntegrityError
