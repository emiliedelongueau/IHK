import argparse
import io
import util
import health

#Define commmand line arguments which can be passed to main.py
#Currently irrelevant, but could be useful later
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Simulate Indian health solutions')
    parser.add_argument('--solution', dest='solution', 
            help='the solution to test', default='health kiosk')
    parser.add_argument('-i', '--import-data', dest='import_data',
            action='store_true', default=False,
            help='Recreate database from raw data files')
    parser.add_argument('-s', '--test-state', dest='test_state', type=str,
            choices = util.state_names)
    parser.add_argument('-d', '--test-district', dest='test_district', type=str)
    return vars(parser.parse_args())

def avg(x):
    return float(sum(x)/len(x))

#Put test code here so it doesn't clutter up the main method
def test(data, args):
    test_state_name = args['test_state']
    test_state = data.get_state_by_name(test_state_name)
    print 'test_state', test_state
    if args['test_district']:
        test_district = data.get_district_by_name(args['test_district'])
    else:
        test_district = data.get_districts_by_state_name(test_state_name)[0]
    print 'test:', test_district.name, 'in', test_state.name
    
    #Generate the population
    data.populate_district(test_district)

    #Fetch the population from the database
    population = data.get_population_district(test_district.name, limit=10000)
    print 'Testing population of', len(population), 'people'

    #Get the MPCE data for the district for debugging purposes
    #This will not be done in the final version
    mpce = data.session.query(io.Mpce).filter_by(state=test_state.name).first()
    print mpce.mpce_average
    filter_test = util.FilterPopulation(mpce.mpce_average*0, 0, 0)

    #Create a hospital to treat the population
    treatable_symptoms = ['diabetes', 'cardio']
    hospital = health.Hospital(test_district, treatable_symptoms, None)

    #Treat the population using the hospital
    treated_population = [hospital.treat(person) if filter_test.filter_all(person) else person for person in population]

    #Perform analytics on the treated population
    print 'Average diabetes in treated population', avg([person.diabetes for person in treated_population])
    
if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io.Database(import_data=args['import_data'])
    test(data, args)
