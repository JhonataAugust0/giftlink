from tortoise import Model, fields


class Grupo(Model):
    """Tabela de grupos."""
    id = fields.IntField(pk=True)
    nome = fields.CharField(max_length=100)
    valor_maximo = fields.FloatField()
    status_sorteio = fields.BooleanField(default=False)

    class Meta:
        table = "grupos"

    

class Pessoa(Model):
    """Tabela de pessoas."""
    id = fields.IntField(pk=True)
    nome = fields.CharField(max_length=100)
    codigo = fields.IntField(max_length=4, unique=True)
    sugestao_presente = fields.TextField(null=True)
    grupo = fields.ForeignKeyField("models.Grupo", related_name="pessoas")

    class Meta:
        table = "pessoas"
