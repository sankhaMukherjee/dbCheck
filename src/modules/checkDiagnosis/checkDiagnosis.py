from logs import logDecorator as lD 
import json, pprint

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

    print('We are in checkDiagnosis')

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
    print('We get a copy of the result dictionary over here ...')
    pprint.pprint(resultsDict)

    doSomething()

    print('Getting out of checkDiagnosis')
    print('-'*30)

    return

