import pdb
import yaml

FILE_NAME = "example-product-team.yaml"

TOP_LEVEL_KEYS = set(['product_narrative', 'company', 'how_might_we',
                    'assets', 'team'])

COMPANY_KEYS = ['logo', 'name']
TEAM_KEYS = ['picture', 'roster']
TEAM_MEMBER_KEYS = ['name', 'email']
ASSETS_KEYS = set(['url', 'title'])

EXTRA = 'EXTRA'
MISSING = 'MISSING'

def diff(provided_keys, required_keys):
    # pdb.set_trace()
    required_keys_set = set(required_keys)
    provided_keys_set = set(provided_keys)
    extra_fields = provided_keys_set - required_keys_set
    missing_fields = required_keys_set - provided_keys_set
    if extra_fields or missing_fields:
        problems = {}
        problems[EXTRA] = extra_fields
        problems[MISSING] = missing_fields
        return problems

def output_error(problems):
    if problems[MISSING]:
        print 'Your report.yaml file is', MISSING, 'the following keys:', \
                problems[MISSING]
    if problems[EXTRA]:
        print 'Your report.yaml file has the following', EXTRA, 'keys:', \
                problems[EXTRA]

if __name__ == '__main__':
    print 'This basic checker reports the first problem it runs into in your report.yaml file.'
    print 'Once you fix that, it can check the rest.'
    print 'You may also want to look at https://codebeautify.org/yaml-validator'
    print '================Problems================'
    yaml_file = open(FILE_NAME, 'r')
    try:
        doc = yaml.load(yaml_file)
        top_level_problems = diff(doc.keys(), TOP_LEVEL_KEYS)
        if top_level_problems:
            output_error(top_level_problems)
        else:
            company_problems = diff(doc['company'].keys(), COMPANY_KEYS)
            if company_problems:
                output_error(company_problems)
            for asset in doc['assets']:
                assets_problems = diff(asset, ASSETS_KEYS)
                if assets_problems:
                    output_error(assets_problems)
            team_problems = diff(doc['team'], TEAM_KEYS)
            if team_problems:
                output_error(team_problems)
            else:
                for member in doc['team']['roster']:
                    roster_problems = diff(member, TEAM_MEMBER_KEYS)
                    if roster_problems:
                        output_error(roster_problems)
    except Exception, e:
        print 'Your yaml file does not parse correctly:\n'
        print str(e)
