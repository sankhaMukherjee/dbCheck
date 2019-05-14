from logs import logDecorator as lD 
import json, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO

from modules.cohort import utils
from multiprocessing import Pool

from tqdm import tqdm

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.cohort.cohort'


@lD.log(logBase + '.generateSchema')
def generateSchema(logger, schemaName):
    '''Generates the required schema
    
    This function generates the required schema
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        query = SQL('CREATE SCHEMA if not exists {}').format( Identifier(schemaName) )
        pgIO.commitData( query )
    except Exception as e:
        logger.error(f'Unable to generate the schema [{schemaName}]: {e}')

    return

@lD.log(logBase + '.generateTable')
def generateTable(logger, schemaName, tableName):
    '''Generates the required schema
    
    This function generates the required schema
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        query = SQL('''
            CREATE TABLE if not exists {}.{} (
                siteid        text,
                backgroundid  text,
                diagn         text[],
                dsmno         text[],
                n_ednum       integer,
                n_days        integer,
                n_days_meds   integer,
                n_days_stress integer,
                n_days_cgi    integer,
                n_days_mse    integer,
                n_days_gaf    integer) ''').format(
                Identifier(schemaName),
                Identifier(tableName) )

        pgIO.commitData(query)
    except Exception as e:
        logger.error(f'Unable to generate the tale [{schemaName}.{tableName}]: {e}')

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for cohort
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    print('='*30)
    print('Main function of cohort')
    print('='*30)
    
    cfg = json.load(open('../config/modules/cohort.json'))['params']
    generateSchema(cfg['schema'])
    generateTable(cfg['schema'], cfg['table'])

    p = Pool()

    totalUsers = 510000
    chunkSize  = 1000
    N = totalUsers // chunkSize
    query = "select siteid, id from raw_data.background"
    usersIter = pgIO.getDataIterator(query, chunks=chunkSize)
    for header, data in tqdm(p.imap(utils.findDataUsers, usersIter), total=N):
        utils.insertDataIntoDatabase(header, data, cfg['schema'], cfg['table'])
        
    p.close()

    print('Getting out of cohort')
    print('-'*30)

    return

