from logs import logDecorator as lD
import json
import pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.cohort.utils'

@lD.log(logBase + '.findUserCGI_nDays')
def findUserBasics(logger, siteId, backgroundId):
    """[summary]
    
    Parameters
    ----------
    logger : [type]
        [description]
    siteId : [type]
        [description]
    backgroundId : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """

    try:
        query = '''
        select ednum, days from raw_data.typepatient where siteid = %s and backgroundid = %s
        '''

        data = pgIO.getAllData(query, (siteId, backgroundId))
        ednum, days = zip(*data)
        nEdnum = len(list(set(ednum)))
        nDays  = len(list(set(days)))
        daysMapper = dict(data)

        return nEdnum, nDays, daysMapper

    except Exception as e:
        logger.error(f'Unable to get data for the user: {e}')
        return None

    return 

@lD.log(logBase + '.findUserCGI_nDays')
def findUserCGI_nDays(logger, siteId, backgroundId, daysMapper):
    """[summary]
    
    Parameters
    ----------
    logger : [type]
        [description]
    siteId : [type]
        [description]
    backgroundId : [type]
        [description]
    daysMapper : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    results = None

    try:
        query = '''
            SELECT ednum 
            from
                raw_data.cgi
            where
                siteid       = %s and 
                backgroundid = %s and 
                severity is not null
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results = [daysMapper.get(r[0]) for r in results if daysMapper.get(r[0]) is not None ]
        results = len(set(results))
        return results

    except Exception as e:
        logger.error(f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')


    return results
