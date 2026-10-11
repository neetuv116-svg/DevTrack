import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

REPORTERS_FILE = os.path.join(settings.BASE_DIR, 'reporters.json')
ISSUES_FILE = os.path.join(settings.BASE_DIR, 'issues.json')


def read_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def write_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def bad_request(message):
    return JsonResponse({'error': message}, status=400)


def get_records(request, path, label, allow_status=False):
    items = read_data(path)
    record_id = request.GET.get('id')
    if record_id is not None:
        try:
            record_id = int(record_id)
        except ValueError:
            return bad_request('id must be an integer')
        for item in items:
            if item['id'] == record_id:
                return JsonResponse(item, status=200)
        return JsonResponse({'error': f'{label} not found'}, status=404)

    status = request.GET.get('status')
    if allow_status and status:
        items = [i for i in items if i['status'] == status]
    return JsonResponse(items, safe=False, status=200)


@csrf_exempt
def reporters(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reporter = Reporter(data['id'], data['name'], data['email'], data['team'])
            reporter.validate()
        except json.JSONDecodeError:
            return bad_request('Invalid JSON')
        except KeyError as e:
            return bad_request(f'Missing field: {e.args[0]}')
        except ValueError as e:
            return bad_request(str(e))

        items = read_data(REPORTERS_FILE)
        items.append(reporter.to_dict())
        write_data(REPORTERS_FILE, items)
        return JsonResponse(reporter.to_dict(), status=201)

    if request.method == 'GET':
        return get_records(request, REPORTERS_FILE, 'Reporter')

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def issues(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            args = (data['id'], data['title'], data['description'],
                    data['status'], data['priority'], data['reporter_id'])
            if data['priority'] == 'critical':
                issue = CriticalIssue(*args)
            elif data['priority'] == 'low':
                issue = LowPriorityIssue(*args)
            else:
                issue = Issue(*args)
            issue.validate()
        except json.JSONDecodeError:
            return bad_request('Invalid JSON')
        except KeyError as e:
            return bad_request(f'Missing field: {e.args[0]}')
        except ValueError as e:
            return bad_request(str(e))

        items = read_data(ISSUES_FILE)
        items.append(issue.to_dict())
        write_data(ISSUES_FILE, items)

        response_data = issue.to_dict()
        response_data['message'] = issue.describe()
        return JsonResponse(response_data, status=201)

    if request.method == 'GET':
        return get_records(request, ISSUES_FILE, 'Issue', allow_status=True)

    return JsonResponse({'error': 'Method not allowed'}, status=405)