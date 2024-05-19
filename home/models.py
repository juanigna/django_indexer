from django.db import models


class NativeTx(models.Model):
    hash = models.CharField("Hash", max_length=100, primary_key=True)
    blockNumber = models.IntegerField("Block number")
    fromAddr = models.CharField("From address", max_length=100)
    toAddr = models.CharField("To address", max_length=100)
    tokenAddress = models.CharField("Token Address", max_length=100, null=True, blank=True)
    blockHash = models.CharField("Block Hash", max_length=100)
    gasPrice = models.IntegerField("Gas price")
    inputTx = models.TextField("Input tx")
    gas = models.IntegerField("Gas")
    nonce = models.IntegerField("Nonce")
    transactionIndex = models.IntegerField("Transaction Index")
    v = models.CharField("v", max_length=100)
    r = models.CharField("r", max_length=100)
    s = models.CharField("s", max_length=100)

    def __str__(self):
        return self.hash


class ERC20Tx(models.Model):
    hash = models.CharField("Hash", max_length=100)
    fromAddr = models.CharField("From address", max_length=100)
    toAddr = models.CharField("To address", max_length=100)
    amount = models.IntegerField("Amount")
    tokenAddress = models.CharField("Token Address", max_length=100)
    nativeTx = models.ForeignKey(NativeTx, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.hash
