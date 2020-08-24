if __name__ == '__main__':
    import argparse
    import requests
    import json

    parser = argparse.ArgumentParser(description='Query a New Relic RPM for all Event Types and their row counts')
    parser.add_argument('apikey', help='New Relic Query API Key')
    parser.add_argument('-a', '--accountid', help='New Relic RPM Account ID. A required argument.', required=True)
    parser.add_argument('-d', '--daysago', help='Number of days to search. Default is 1.', type=int, default='1')
    parser.add_argument('-o', '--outputfile', help='File name to report results', default='output.csv')
    parser.add_argument('-p', '--printoutput', help='Print output file to screen in addition to file',
                        action='store_true')

    args = parser.parse_args()

    api_key = args.apikey
    account_id = args.accountid
    days_ago = str(args.daysago)
    output_file = args.outputfile
    print_output = args.printoutput
    output = ''

    system_events = ['NrConsumption', 'NrDailyUsage', 'NrMTDConsumption', 'NrUsage', 'Public_APICall', 'NrAuditEvent']

    url = 'https://insights-api.newrelic.com/v1/accounts/' + account_id + '/query'

    headers = {
        'Accept': 'application/json',
        'X-Query-Key': api_key,
    }

    params = (
        ('nrql', 'SHOW EVENT TYPES SINCE ' + days_ago + ' DAYS AGO'),
    )

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == requests.codes.ok:
        print('API responded with 200. Retrieving row counts for all Event Types since ' + days_ago + ' days ago.')
        print('Stand by...')
        output = 'Event Type,Row Count\n'
        responseBody = json.loads(response.text)
        result = response.json().get('results')
        for eventTypes in result:
            for et in eventTypes.values():
                for e in et:
                    if e not in system_events:
                        et_params = (
                            ('nrql', 'SELECT count(*) FROM `' + e + '` SINCE ' + days_ago + ' DAYS AGO'),
                        )
                        et_response = requests.get(url, headers=headers, params=et_params)
                        if et_response.status_code == requests.codes.ok:
                            count_result = et_response.json().get('results')
                            for ec in count_result:
                                output = output + e + "," + str(ec['count']) + "\n"
    else:
        print('Call to API failed with Status ' + str(response.status_code) + ': ' + response.reason)

    if print_output:
        print('Output file:\n' + output)

    file = open(output_file, 'w')
    file.write(output)
    file.close()

    print('CSV report written to ' + output_file + '...')
    print('Script complete.')
