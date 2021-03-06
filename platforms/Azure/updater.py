import argparse
import github
import json
import yaml
import os
import testrail
import requests


def get_testrail_client(args):
    testrail_username = args['testrail_username']
    testrail_password = args['testrail_password']
    client = testrail.APIClient('https://openebs.testrail.io')
    client.user = testrail_username
    client.password = testrail_password
    return client


def github_authentication(args):
    github_username = args['github_username']
    github_password = args['github_password']
    github_auth = github.Github(github_username, github_password)
    return github_auth


def get_yaml_file_data(path):
    try:
        yaml_file = open(path, 'r')
        data = yaml.load(yaml_file.read())
        yaml_file.close()
    except EnvironmentError as e:
        print("File operation failed, Error: %s" % e)
        return None, -1
    except yaml.YAMLError as e:
        print("YAML operation failed, Error: %s" % e)
        return None, -1

    return data, 1


def get_json_file_data(path):
    try:
        json_file = open(path, 'r')
        data = json.load(json_file)
        json_file.close()
    except EnvironmentError as e:
        print("File operation failed, Error: %s" % e)
        return None, -1
    except ValueError as e:
        print("JSON operation failed, Error: %s" % e)
        return None, -1
    return data, 1


def get_file_data(path):
    try:
        file = open(path, 'r')
        data = file.read()
        file.close()
    except EnvironmentError as e:
        print("File operation failed, Error: %s" % e)
        return None, -1

    return data, 1


def update_github_issue_comment(args, case, logs):
    # API_ENDPOINT = 'https://api.github.com/repos/ashishranjan738/%s/issues/%s/comments' % (case['reponame'], case['issue_number'])
    # github_token = args['github_token']
    # headers = {'Authorization': 'token %s' % github_token}
    # data = { 'body': '%s' % logs }
    # r = requests.post(url = API_ENDPOINT, data = json.dumps(data), headers = headers)

    github_client = github_authentication(args)
    print(github_client.get_user().get_repo(case['reponame']).get_issue(int(case['issue_number'])).create_comment(str(logs)))

def check_error(err):
    if err == -1:
        exit(err)


def get_workspace_path():
    path = os.path.expanduser('~') + "/e2e/Azure"
    return path


def update_testrail_with_status(args):
    testrail_client = get_testrail_client(args)
    # test_plans, err = get_yaml_file_data(path + '/GCP.yml')
    # check_error(err)

    suites, err = get_json_file_data(args['workspace_path']+'/mapping.json')
    if err==-1:
        return err

    # print(suites)
    for suite_id, suite_value in suites.items():
        suite_cases = suite_value['cases']
        suite_run_id = suite_value['run_id']

        for case in suite_cases:
            result, err = get_json_file_data(
                args['workspace_path'] + "/cases/" + str(case['case_id']) + '/result.json')
            if err != -1:
                status_id = result['status_id']

                testrail_client.send_post('add_results_for_cases/' + str(suite_run_id),
                                          {
                                              'results': [
                                                  {
                                                      'case_id': case['case_id'],
                                                      'status_id': str(status_id)
                                                  }
                                              ]
                                          }
                                          )

            logs, err = get_file_data(args['workspace_path'] + "/cases/" + str(case['case_id']) + '/logs')
            print("------------------------>"+str(logs)+"<----------------------------")
            logs = logs+"Logs comming soon"
            if err != -1 :
                update_github_issue_comment(args, case, logs)
            print('Successfully updated case_id - %s' % case['case_id'])

def main():
    parser = argparse.ArgumentParser(description='cli to get required details')
    # parser.add_argument('-bn', '--build-number', help='buildnumber', required=True)
    parser.add_argument('-guser', '--github-username', help='username for github', required=True)
    parser.add_argument('-gpass', '--github-password', help='password for github', required=True)
    parser.add_argument('-tuser', '--testrail-username', help='username for testrail', required=True)
    parser.add_argument('-tpass', '--testrail-password', help='password for testrail', required=True)
    args = vars(parser.parse_args())
    args['workspace_path'] = get_workspace_path()
    update_testrail_with_status(args)


if __name__ == "__main__":
    main()
