from logs import logDecorator as lD
import json
import pprint

from tqdm import tqdm

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

@lD.log(logBase + '.findUserGAF_nDays')
def findUserGAF_nDays(logger, siteId, backgroundId, daysMapper):
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
            SELECT distinct ednum 
            from
                raw_data.gaf
            where
                siteid       = %s and 
                backgroundid = %s and 
                gaf is not null
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results = [daysMapper.get(r[0])
                   for r in results if daysMapper.get(r[0]) is not None]
        results = len(set(results))
        return results

    except Exception as e:
        logger.error(
            f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')

    return results

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
            SELECT distinct ednum 
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

@lD.log(logBase + '.findUserMSE_nDays')
def findUserMSE_nDays(logger, siteId, backgroundId, daysMapper):
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
            SELECT distinct ednum 
            from
                raw_data.mse
            where
                siteid       = %s and 
                backgroundid = %s
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results = [daysMapper.get(r[0])
                   for r in results if daysMapper.get(r[0]) is not None]
        results = len(set(results))
        return results

    except Exception as e:
        logger.error(
            f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')

    return results

@lD.log(logBase + '.findUserStress_nDays')
def findUserStress_nDays(logger, siteId, backgroundId, daysMapper):
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
            SELECT distinct ednum 
            from
                raw_data.psycho
            where
                siteid       = %s and 
                backgroundid = %s
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results = [daysMapper.get(r[0])
                   for r in results if daysMapper.get(r[0]) is not None]
        results = len(set(results))
        return results

    except Exception as e:
        logger.error(
            f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')

    return results

@lD.log(logBase + '.findUserMeds_nDays')
def findUserMeds_nDays(logger, siteId, backgroundId, daysMapper):
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
            SELECT distinct ednum 
            from
                raw_data.meds
            where
                siteid       = %s and 
                backgroundid = %s and
                psymed       = 'Yes'
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results = [daysMapper.get(r[0])
                   for r in results if daysMapper.get(r[0]) is not None]
        results = len(set(results))
        return results

    except Exception as e:
        logger.error(
            f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')

    return results

@lD.log(logBase + '.findUserDiagn')
def findUserDiagn(logger, siteId, backgroundId, daysMapper):
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
    
    try:
        query = '''
            SELECT 
                siteid,
                array_agg( distinct ednum ),
                array_agg( distinct dsmno ),
                array_agg( distinct diagnosis )
            from
                raw_data.pdiagnose
            where
                siteid       = %s and 
                backgroundid = %s
            group by
                siteid
        '''

        results = pgIO.getAllData(query, (siteId, backgroundId))
        results1 = [daysMapper.get(r)
                   for r in results[0][1] if daysMapper.get(r) is not None]
        results1 = len(set(results1))
        results2 = [('n_days_diagn', results1)]
        results2.append(('dsmno', results[0][2]))
        results2.append(('diagn', results[0][3]))

        return results2

    except Exception as e:
        logger.error(
            f'Unable to generate CGI for the user ({siteId},{backgroundId}): {e}')

    results = [
        ('n_days_diagn', None),
        ('dsmno', []),
        ('diagn', []),
    ]

    return results

@lD.log(logBase + '.findUserData')
def findUserData(logger, siteId, backgroundId):

    try:
        results = findUserBasics(siteId, backgroundId)
        if results is None:
            print(f'Unable to get information for user {siteId},{backgroundId}')
            return None

        nEdnum, nDays, daysMapper = results
        results = [
            ('siteid', siteId),
            ('backgroundid', backgroundId),
            ('n_ednum', nEdnum),
            ('n_days', nDays),
        ]
        cgi = findUserCGI_nDays(siteId, backgroundId, daysMapper)
        results.append(('n_days_cgi', cgi))

        gaf = findUserGAF_nDays(siteId, backgroundId, daysMapper)
        results.append(('n_days_gaf', gaf))

        mse = findUserMSE_nDays(siteId, backgroundId, daysMapper)
        results.append(('n_days_mse', mse))

        stress = findUserStress_nDays(siteId, backgroundId, daysMapper)
        results.append(('n_days_stress', stress))

        meds = findUserMeds_nDays(siteId, backgroundId, daysMapper)
        results.append(('n_days_meds', meds))

        diagn = findUserDiagn(siteId, backgroundId, daysMapper)
        results += diagn

        return results

    except Exception as e:
        logger.error(f'Unable to get user data for user {siteId}{backgroundId}: {e}')
        return None

    return

@lD.log(logBase + '.findDataUsers')
def findDataUsers(logger, userList):
    """[summary]
    
    Parameters
    ----------
    logger : [type]
        [description]
    userList : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    
    allData = []
    for user in tqdm(userList):
        userData = findUserData(*user)
        headers, values = zip(*userData)
        allData.append( values )

    headers = headers

    return headers, allData
