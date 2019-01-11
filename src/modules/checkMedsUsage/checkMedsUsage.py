from logs import logDecorator as lD 
import json, pprint
from tqdm import tqdm

from modules.checkMedsUsage import utils

from multiprocessing import Pool

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.checkMedsUsage.checkMedsUsage'


@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    print('We are in checkMedsUsage')

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for module1
    
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

    p = Pool()

    print('Getting Users')
    users = utils.getUsers()[:1000]
    N = len(users)
    print('{} users found'.format( N ))



    for i, m in enumerate(tqdm(   p.imap(utils.getUserMeds, users) , total=N ) ):
        if i == 0:
            d = m.copy()
        else:
            d += m

    print(d)

    return

