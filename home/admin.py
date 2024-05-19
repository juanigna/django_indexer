from django.contrib import admin

from home.models import ERC20Tx, NativeTx

# Register your models here.
admin.site.register(ERC20Tx)
admin.site.register(NativeTx)
