from logs import logDecorator as lD 
import json, pprint
import numpy as np

from lib.databaseIO import pgIO
from psycopg2 import sql

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.checkMedsUsage.utils'

@lD.log( logBase + '.getUsers' )
def getUsers(logger):

    query = '''
        SELECT siteid, backgroundid
        from mdd.patient_result
        '''

    result = pgIO.getAllData( query )

    return result 

@lD.log( logBase + '.getUserMeds' )
def getUserMeds(logger, user):

    siteid, backgroundid = user

    query = sql.SQL('''
            SELECT 
                agomelatine,
                amitriptyline,
                amoxapine,
                aripiprazole,
                brexpiprazole,
                bupropion,
                citalopram,
                clomipramine,
                desipramine,
                desvenlafaxine,
                doxepin,
                duloxetine,
                escitalopram,
                fluoxetine,
                fluvoxamine,
                imipramine,
                isocarboxazid,
                lamotrigine,
                levomilnacipran,
                maprotiline,
                mianserin,
                milnacipran,
                mirtazapine,
                moclobemide,
                nefazodone,
                nortryptyline,
                noxiptiline,
                olanzapine,
                opipramol,
                paroxetine,
                phenelzine,
                pipofezine,
                pirlindole,
                protriptyline,
                quetiapine,
                reboxetine,
                selegiline,
                sertraline,
                tianeptine,
                tranylcypromine,
                trazodone,
                trimipramine,
                venlafaxine,
                vilazodone,
                vortioxetine
            from mdd.master_result
            where 
                siteid       = {} and 
                backgroundid = {}
        ''').format(
            sql.Literal(siteid), sql.Literal(backgroundid))

    result = pgIO.getAllData( query )
    result = np.array(result)
    result = result.sum( axis=0 )
    result = (result > 0)*1
    
    return result
