from django.db import models

class Client(models.Model):
    code = models.AutoField(primary_key=True,auto_created=True)
    nom=models.CharField(max_length=255)
    prenom=models.CharField(max_length=255)
    def __str__(self):
        return f"code = {self.code} nom = {self.nom}  prenom = {self.prenom} "

class Compte(models.Model):
    numero = models.IntegerField(unique=True)
    dateCreation =models.DateField()
    solde= models.FloatField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE,related_name="cl")
    def __str__(self):
        return f"numero = {self.numero} dateCreation = {self.dateCreation}  solde = {self.solde} ** client -> {self.client} "
class Operation(models.Model):
    numeroOperation = models.AutoField(primary_key=True, auto_created=True)
    dateOperation = models.DateField()
    montant = models.FloatField()
    typechoices = [('versement', 'Versement'),('retrait', 'Retrait'),]
    type = models.CharField(choices=typechoices,max_length=9,default='versement',)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name="compte")
    def __str__(self):
        return f"numeroOperation = {self.numeroOperation} dateOperation = {self.dateOperation}  montant = {self.montant} type = {self.type}" \
               f" ** compte -> {self.compte} "