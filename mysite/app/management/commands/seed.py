from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from app.models import VooBase,VooReal
import random,datetime

# python manage.py seed --mode=refresh

""" Clear all data and create users """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete VooBase instances")
    VooBase.objects.all().delete()
    print("Delete VooReal instances")
    VooReal.objects.all().delete()


def create_users():
    """Creates an address object combining different elements from the list"""
    piloto = User.objects.get(username='piloto')
    if not piloto:
        print("Creating piloto")
        piloto = User.objects.create_user('piloto', 'piloto@mail.com', 'piloto')
        piloto.save()
        print("piloto created.")
    pilotos, created = Group.objects.get_or_create(name='pilotos')
    pilotos.user_set.add(piloto)

    funcionario = User.objects.get(username='funcionario')
    if not funcionario:
        print("Creating funcionário")
        funcionario = User.objects.create_user('funcionario', 'funcionario@mail.com', 'funcionario')
        funcionario.save()
        print("funcionário created.")
    funcionarios, created = Group.objects.get_or_create(name='funcionarios')
    funcionarios.user_set.add(funcionario)

    operador = User.objects.get(username='operador')
    if not operador:
        print("Creating operador")
        operador = User.objects.create_user('operador', 'operador@mail.com', 'operador')
        operador.save()
        print("operador created.")
    operadores, created = Group.objects.get_or_create(name='operadores')
    operadores.user_set.add(operador)

    torre = User.objects.get(username='torre')
    if not torre:
        print("Creating torre de controle")
        torre = User.objects.create_user('torre', 'torre@mail.com', 'torre')
        torre.save()
        print("operador torre de controle.")
    torres, created = Group.objects.get_or_create(name='torres')
    torres.user_set.add(torre)

    gerente = User.objects.get(username='gerente')
    if not gerente:
        print("Creating gerente")
        gerente = User.objects.create_user('gerente', 'gerente@mail.com', 'gerente')
        gerente.save()
        print("operador gerente.")
    gerentes, created = Group.objects.get_or_create(name='gerentes')
    gerentes.user_set.add(gerente)

    return 

def create_voo():
    voo1 = VooBase.objects.create(codigo_voo='011',companhia_aerea='Tesla',dia_da_semana='Segunda',
                                horario_partida_base=str(datetime.date.today().strftime("%H:%M:%S")), duracao_base=5,origem='SP',destino='TO')
    voo1.save()

    vooreal1 = VooReal.objects.create(voo_base=voo1,estado_voo='Autorizado',data_voo=datetime.date.today() )
    vooreal1.save()
    voo2 = VooBase.objects.create(codigo_voo='012',companhia_aerea='Tesla',dia_da_semana='Terça',
                                horario_partida_base=str(datetime.date.today().strftime("%H:%M:%S")), duracao_base=5,origem='RJ',destino='PE')
    voo2.save()

    vooreal2 = VooReal.objects.create(voo_base=voo2,estado_voo='Aterrisado',data_voo=datetime.date.today() )
    vooreal2.save()


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    if mode == MODE_CLEAR:
      clear_data()
      return

    # Creating users
    create_users()
    create_voo()