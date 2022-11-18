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
    try:
        piloto = User.objects.get(username='piloto')
    except:
        piloto = None
    if not piloto:
        print("Creating piloto")
        piloto = User.objects.create_user('piloto', 'piloto@mail.com', 'piloto')
        piloto.save()
        print("piloto created.")
    pilotos, created = Group.objects.get_or_create(name='pilotos')
    pilotos.user_set.add(piloto)

    try:
        funcionario = User.objects.get(username='funcionario')
    except:
        funcionario = None
    if not funcionario:
        print("Creating funcionário")
        funcionario = User.objects.create_user('funcionario', 'funcionario@mail.com', 'funcionario')
        funcionario.save()
        print("funcionário created.")
    funcionarios, created = Group.objects.get_or_create(name='funcionarios')
    funcionarios.user_set.add(funcionario)

    try:
        operador = User.objects.get(username='operador')
    except:
        operador = None 
    if not operador:
        print("Creating operador")
        operador = User.objects.create_user('operador', 'operador@mail.com', 'operador')
        operador.save()
        print("operador created.")
    operadores, created = Group.objects.get_or_create(name='operadores')
    operadores.user_set.add(operador)

    try:
        torre = User.objects.get(username='torre')
    except:
        torre = None
    if not torre:
        print("Creating torre de controle")
        torre = User.objects.create_user('torre', 'torre@mail.com', 'torre')
        torre.save()
        print("operador torre de controle.")
    torres, created = Group.objects.get_or_create(name='torres')
    torres.user_set.add(torre)

    try:
        gerente = User.objects.get(username='gerente')
    except:
        gerente = None
    if not gerente:
        print("Creating gerente")
        gerente = User.objects.create_user('gerente', 'gerente@mail.com', 'gerente')
        gerente.save()
        print("operador gerente.")
    gerentes, created = Group.objects.get_or_create(name='gerentes')
    gerentes.user_set.add(gerente)

    return 



def create_voo():
    voo_1 = VooBase.objects.create(codigo_voo='011',
                                  companhia_aerea = 'Gol',
                                  dia_da_semana = 'Segunda',
                                  horario_partida_base = datetime.time(12, 0, 0),
                                  duracao_base = datetime.time(5, 0, 0),
                                  origem = 'SP',
                                  destino = 'TO')
    voo_1.save()

    voo_2 = VooBase.objects.create(codigo_voo='021',
                                  companhia_aerea = 'Latam',
                                  dia_da_semana = 'Terca',
                                  horario_partida_base = datetime.time(3, 0, 0),
                                  duracao_base = datetime.time(2, 0, 0),
                                  origem = 'SP',
                                  destino = 'RJ')
    voo_2.save()
    
    voo_3 = VooBase.objects.create(codigo_voo='092',
                                  companhia_aerea = 'Latam',
                                  dia_da_semana = 'Terca',
                                  horario_partida_base = datetime.time(10, 0, 0),
                                  duracao_base = datetime.time(5, 0, 0),
                                  origem = 'RJ',
                                  destino = 'AM')
    voo_3.save()
    
    voo_4 = VooBase.objects.create(codigo_voo='22',
                                  companhia_aerea = 'Latam',
                                  dia_da_semana = 'Terca',
                                  horario_partida_base = datetime.time(10, 0, 0),
                                  duracao_base = datetime.time(3, 30, 0),
                                  origem = 'DF',
                                  destino = 'AM')
    voo_4.save()
    
    voo_real_1 = VooReal.objects.create(voo_base = voo_1,
                                        estado_voo = 'AGD',
                                        horario_real_chegada = datetime.time(10, 0, 0),
                                        horario_real_partida = datetime.time(15, 0, 0),
                                        data_voo = datetime.date.today() )
    voo_real_1.save()


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