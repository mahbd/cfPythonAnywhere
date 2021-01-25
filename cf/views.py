import json

from django.http import JsonResponse, Http404

from cf.models import Handle, Problems


def add_handle(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            handle = request.POST['handle']
            Handle.objects.get_or_create(name=name, handle=handle)
            return JsonResponse({'status': True})
        except KeyError:
            return JsonResponse({'status': False, 'reason': 'KeyError'})
    else:
        raise Http404


def _add_problem(name, link, handle, check=True):
    if check:
        Problems.objects.get_or_create(name=name, link=link)
    problem = Problems.objects.get(name=name, link=link)
    try:
        problem.solver.get(handle=handle)
        return 'D'
    except Handle.DoesNotExist:
        solver = Handle.objects.create(handle=handle)
        problem.solver.add(solver)
        problem.num_sol += 1
        problem.save()
        return 'O'


def add_problem(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            link = request.POST['link']
            solver_handle = request.POST['solver']
            res = _add_problem(name, link, solver_handle)
            if res == 'D':
                return JsonResponse({'status': False, 'reason': 'AlreadyAdded'})
            else:
                return JsonResponse({'status': True})
        except KeyError:
            return JsonResponse({'status': False, 'reason': 'KeyError'})


def add_problems(request):
    data = json.loads(request.body)
    added_problems = {}
    for problems in Problems.objects.all():
        added_problems[problems.name] = []
        for solver in problems.solver.all():
            added_problems[problems.name].append(solver.handle)
    dp, su = 0, 0
    for problem in data['problems']:
        if not added_problems.get(problem['name']) or problem['solver'] not in added_problems.get(problem['name']):
            check = True if added_problems.get(problem['name']) else False
            res = _add_problem(problem['name'], problem['link'], problem['solver'], check)
            if res == 'D':
                dp += 1
            else:
                su += 1
    return JsonResponse({"success": su, "duplicate": dp})


def get_list(request, start=0, end=30):
    all_prob = Problems.objects.all()
    try:
        to_send = all_prob[start:end]
    except IndexError:
        return JsonResponse({'status': False, 'reason': 'Wrong start or end'})
    if start >= end:
        return JsonResponse({'status': False, 'reason': 'Wrong start or end'})
    res = {'status': True, 'total': len(all_prob), 'showing': str(start) + ' - ' + str(end)}
    for problem in to_send:
        info = {'total_solvers': problem.num_sol, 'link': problem.link}
        solvers = []
        for solver in problem.solver.all():
            solver_name = solver.name
            if solver_name is None:
                solver_name = solver.handle
            solvers.append(solver_name)
        info['solvers'] = solvers
        res[problem.name] = info
    return JsonResponse(res)
