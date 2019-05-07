from logs import logDecorator as lD 
import json, pprint
from lib.databaseIO import pgIO

from tqdm import tqdm

from collections import Counter

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.checkDiagnosis.checkDiagnosis'


@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    counts = Counter()

    query = ''' SELECT diagnosis
    from 
        info.user_diagn 
    where not 
    dsmno && array [
        '296.20', '296.21', '296.22', '296.23', '296.24', '296.25', 
        '296.26', '296.2', '296.30', '296.31', '296.32', '296.33', 
        '296.34', '296.35', '296.36', '296.3', 'F32.0', 'F32.1', 'F32.2', 
        'F32.3', 'F32.4', 'F32.5', 'F32.9','F33.0', 'F33.1', 'F33.2', 
        'F33.3', 'F33.4', 'F33.40', 'F33.41', 'F33.42', 'F33.9', 
        '300.0', '300.00', '300.01', '300.02', '300.09', 'F41', 'F41.0', 
        'F41.1', 'F41.3', 'F41.8', 'F41.9', '296.0', '296.00', '296.01', 
        '296.02', '296.03', '296.04', '296.05', '296.06', '296.4', '296.40', 
        '296.41', '296.42', '296.43', '296.44', '296.45', '296.46', '296.5', 
        '296.50', '296.51', '296.52', '296.53', '296.54', '296.55', '296.56', 
        '296.6', '296.60', '296.61', '296.62', '296.63', '296.64', '296.65', 
        '296.66', '296.7', '296.8', '296.80', '296.81', '296.82', '296.89',
        'F31', 'F31.0', 'F31.1', 'F31.10', 'F31.11', 'F31.12', 'F31.13', 
        'F31.2', 'F31.3', 'F31.30', 'F31.31', 'F31.32', 'F31.4', 'F31.5', 
        'F31.6', 'F31.60', 'F31.61', 'F31.62', 'F31.63', 'F31.64', 'F31.7', 
        'F31.70', 'F31.71', 'F31.72', 'F31.73', 'F31.74', 'F31.75', 'F31.76', 
        'F31.77', 'F31.78', 'F31.8', 'F31.81', 'F31.89', 'F31.9', '295', 
        '295.0', '295.00', '295.01', '295.02', '295.03', '295.04', '295.05', 
        '295.1', '295.10', '295.11', '295.12', '295.13', '295.14', '295.15', 
        '295.2', '295.20', '295.21', '295.22', '295.23', '295.24', '295.25', 
        '295.3', '295.30', '295.31', '295.32', '295.33', '295.34', '295.35', 
        '295.4', '295.40', '295.41', '295.42', '295.43', '295.44', '295.45', 
        '295.5', '295.50', '295.51', '295.52', '295.53', '295.54', '295.55', 
        '295.6', '295.60', '295.61', '295.62', '295.63', '295.64', '295.65', 
        '295.7', '295.70', '295.71', '295.72', '295.73', '295.74', '295.75', 
        '295.8', '295.80', '295.81', '295.82', '295.83', '295.84', '295.85', 
        '295.9', '295.90', '295.91', '295.92', '295.93', '295.94', '295.95', 
        'F20', 'F20.0', 'F20.1', 'F20.2', 'F20.3', 'F20.5', 'F20.8', 'F20.81', 
        'F20.89', 'F20.9', '314.0', '314.00', '314.01', 'F90', 'F90.0', 
        'F90.1', 'F90.2', 'F90.8', 'F90.9', '309.81', 'F43.1', 'F43.10', 'F43.11', 
        'F43.12' ]
    '''

    print('Downloading the data')
    data = pgIO.getAllData(query)

    for d in tqdm(data):
        try:
            counts.update(d[0])
        except Exception as e:
            logger.error(f'Problem: {e}')

    for c in counts:
        try:
            print(f'{c:50} --> {counts[c]}')
        except Exception as e:
            print(c, counts[c])

    with open('../results/symptoms.json', 'w') as fOut:
        json.dump( counts , fOut)

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for checkDiagnosis
    
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
    print('Main function of checkDiagnosis')
    print('='*30)
    # print('We get a copy of the result dictionary over here ...')
    # pprint.pprint(resultsDict)

    doSomething()

    print('Getting out of checkDiagnosis')
    print('-'*30)

    return

