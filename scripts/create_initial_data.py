from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
from ortelius.database import db
import ortelius
# from ortelius.types.historical_date import HistoricalDate as hd
# from ortelius.models.Coordinates import Coordinates, Shape, Quadrant
# from ortelius.models.Date import Date, Millenium, Century, Year
# from ortelius.models.Fact import Fact, FactType
# from ortelius.models.Process import Process, ProcessType
# from ortelius.models.Persona import Persona, PersType
# from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.User import User, UsersRoles, Role
#
# from test_data.test_facts import test_facts
# from test_data.test_hist_regions import test_hist_regions
# from test_data.test_processes import test_processes
# from test_data.test_personas import test_personas
#
def make_session(db):
    return sessionmaker(bind=db)
#
def create_admin(db):
    session = make_session(db)
    """Creates the admin user."""
    admin_role = Role(id=1, name='admins', label='Administrators')
    admin_user = User(id=1, username='admin',
                      email='ad@min.com', password='admin', active=True)
    admin_user_role = UsersRoles(user_id=admin_user.id, role_id=admin_role.id)
    session.add(admin_role)
    session.add(admin_user)
    session.commit()
    session.add(admin_user_role)
    session.commit()
#
# def create_years(db):
#     session = make_session(db)
#     # Create millenimus, centuries and years from -5000 to 2999
#     for i in (-5, -4, -3, -2, -1, 1, 2, 3):
#         print('Create millenium: ' + str(i))
#         mil = Millenium(number=i)
#         session.add(mil)
#         for j in range(0, 10):
#             centNumber = j+(i*10) if i < 0 else j + 1 + ((i-1)*10)
#             cent = Century(number=centNumber, millenium=mil)
#             session.add(cent)
#             for k in range(0, 100):
#                 yearNumber = k+(centNumber*100) - 1 if i < 0 else k + ((centNumber-1)*100)
#                 year = Year(number=yearNumber, century=cent)
#                 session.add(year)
#
#     session.commit()
#
# def create_fact_types(db):
#     session = make_session(db)
#     f_types = [
#                 ['battle', 'сражение'],
#                 ['peace_treaty', 'мирный договор']
#               ]
#
#     for t in f_types:
#         new_type = FactType(name=t[0], label=t[1])
#         session.add(new_type)
#         try:
#             session.commit()
#         except IntegrityError:
#             session.rollback()
#
# def create_facts():
#     session = make_session()
#     for f in test_facts:
#         new_start_date = Date.create(date=hd(f['start_date']))
#         new_end_date = Date.create(date=hd(f['end_date']))
#         if f['coordinates']:
#             point = Coordinates.create(f['coordinates'][0], f['coordinates'][1])
#             session.add(point)
#
#             new_shape = Shape(start_date=new_start_date, end_date=new_end_date, coordinates=[point])
#             session.add(new_shape)
#
#         new_fact = Fact(name = f['name'],
#                         label=f['label'],
#                         description=f['description'],
#                         info=f['info'],
#                         weight=f['weight'],
#                         type=FactType.create(name=f['type'][0], label=f['type'][1]),
#                         start_date=new_start_date,
#                         end_date=new_end_date,
#                         text=f['text'],
#                         shape=new_shape
#                        )
#         session.add(new_fact)
#         session.commit()
#
# def create_hist_regions():
#     session = make_session()
#     for region in test_hist_regions:
#         region_facts = []
#         region_shapes = []
#         start_date = None
#         end_date = None
#         if region['start_date'] != None:
#             start_date = Date.create(date=hd(region['start_date']))
#
#         if region['end_date'] != None:
#             end_date = Date.create(date=hd(region['end_date']))
#
#         if region['facts']:
#             for fact in region['facts']:
#                 region_facts.append(Fact.query.get(fact))
#
#         if region['shapes']:
#             for shape in region['shapes']:
#                 region_shapes.append(Shape.query.get(shape))
#
#         hr = HistRegion(name=region['name'],
#                         label=region['label'],
#                         description=region['description'],
#                         text=region['text'],
#                         start_date=start_date,
#                         end_date=end_date,
#                         shapes=region_shapes,
#                         facts=region_facts
#                         )
#         session.add(hr)
#     session.commit()
#
#
# def create_shape():
#     session = make_session()
#     point = Coordinates.create(66.82, 10.5)
#     sh = Shape(start_date=Date.create(date=hd(datetime.date.today())), end_date=Date.create(date=hd(datetime.date.today())), coordinates=[point])
#     session.add(sh)
#     session.commit()
#
# def create_quadrants():
#     session = make_session()
#     for q in Quadrant.quadrants:
#         quadrant = Quadrant(hash=Quadrant.make_hash(q[0], q[1]))
#         session.add(quadrant)
#     session.commit()
#
# def create_processes():
#     session = make_session()
#     for process in test_processes:
#         new_start_date = Date.create(date=hd(process['start_date']))
#         process_type = ProcessType.create(name=process['type'][0], label=process['type'][1])
#         new_end_date = Date.create(date=hd(process['end_date']))
#         p_hist_regions = [ HistRegion.query.get(x) for x in process['hist_regions'] ]
#         p_facts = [ Fact.query.get(x) for x in process['facts'] ]
#         new_process = Process(name=process['name'],
#                               label=process['label'],
#                               description=process['description'],
#                               start_date=new_start_date,
#                               end_date=new_end_date,
#                               text=process['text'],
#                               hist_regions=p_hist_regions,
#                               type=process_type,
#                               facts=p_facts
#                               )
#
#         session.add(new_process)
#     session.commit()
#
# def create_personas():
#     session = make_session()
#     for persona in test_personas:
#         new_start_date = Date.create(date=hd(persona['start_date']))
#         new_end_date = Date.create(date=hd(persona['end_date']))
#         p_hist_regions = [ HistRegion.query.get(x) for x in persona['hist_regions'] ]
#         p_facts = [ Fact.query.get(x) for x in persona['facts'] ]
#         p_processes = [ Process.query.get(x) for x in persona['processes'] ]
#         persona_type = PersType.create(name=persona['type'][0], label=persona['type'][1])
#
#         new_persona = Persona(
#             name = persona['name'],
#             label = persona['label'],
#             description = persona['description'],
#             start_date = new_start_date,
#             end_date = new_end_date,
#             text = persona['text'],
#             type = persona_type,
#             facts = p_facts,
#             hist_regions = p_hist_regions,
#             processes = p_processes
#         )
#         session.add(new_persona)
#     session.commit()
#
# def main(db):
#     create_admin()
#     create_quadrants()
#     create_years()
#     create_shape()
#     create_fact_types()
#     create_facts()
#     create_hist_regions()
#     create_processes()
#     create_personas()
