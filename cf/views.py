from django.http import JsonResponse, Http404
from cf.models import Handle, Problems


def add_handle(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            handle = request.POST['handle']
            Handle.objects.get_or_create(name=name, handle=handle)
            return JsonResponse({'status':True})
        except KeyError:
            return JsonResponse({'status':False, 'reason': 'KeyError'})
    else:
        raise Http404


def add_problem(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            link = request.POST['link']
            solver_handle = request.POST['solver']
            try:
                problem = Problems.objects.get(name=name)
            except Problems.DoesNotExist:
                Problems.objects.create(name=name, link=link)
                problem = Problems.objects.get(name=name)
            try:
                problem.solver.get(handle=solver_handle)
                return JsonResponse({'status': False, 'reason': 'AlreadyAdded'})
            except Handle.DoesNotExist:
                Handle.objects.get_or_create(handle=solver_handle)
                solver_id = Handle.objects.get(handle=solver_handle).id
                problem.solver.add(solver_id)
                problem.num_sol += 1
                problem.save()
                return JsonResponse({'status':True})
        except KeyError:
            return JsonResponse({'status': False, 'reason': 'KeyError'})


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
