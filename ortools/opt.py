import numpy as np
import apache_beam as beam


def solve(element):
    from ortools.linear_solver import pywraplp
    A = element['A']
    req = element['req']
    store = element['store']

    solver = pywraplp.Solver('prob', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = {i_pack: solver.IntVar(0, solver.infinity(), 'pack_{0}'.format(i_pack)) for i_pack, ai in enumerate(A)}
    y = {j_sku: solver.Sum([A[i_pack][j_sku] * x[i_pack] for i_pack in range(len(A))]) for j_sku in range(len(A[0]))}
    abs_diff = {}
    for j_sku in y:
        abs_diff[j_sku] = solver.NumVar(0, solver.infinity(), 'diff_{0}'.format(j_sku))
        diff = req[j_sku] - y[j_sku]
        solver.Add(-abs_diff[j_sku] <= diff)
        solver.Add(diff <= abs_diff[j_sku])
    solver.Minimize(solver.Sum(abs_diff.values()) + 0.1 * solver.Sum(x.values()))
    status = solver.Solve()
    if status == solver.OPTIMAL:
        print('optimal_{0}'.format(store))
    else:
        print('error')
    sol = {i: x[i].solution_value() for i in x}
    sol.update({'store': store})
    return sol


def main():
    A = [[10, 10, 0], [0, 10, 10], [5, 10, 5], [2, 0, 0], [0, 2, 0], [0, 0, 2]]
    np.random.seed(1)
    R = np.random.randint(0, 50, (100, 3))
    inputs = [{'store': store, 'req': req.tolist(), 'A': A} for store, req in enumerate(R)]

    options = beam.options.pipeline_options.PipelineOptions()
    setup_options = options.view_as(beam.options.pipeline_options.SetupOptions)
    setup_options.setup_file = './setup.py'
    gcloud_options = options.view_as(beam.options.pipeline_options.GoogleCloudOptions)
    gcloud_options.job_name = "opt2"
    gcloud_options.project = "kaggle-playground"
    gcloud_options.staging_location = "gs://kaggle-playground-dataflow/staging"
    gcloud_options.temp_location = "gs://kaggle-playground-dataflow/temp"
    options.view_as(beam.options.pipeline_options.StandardOptions).runner = "DataflowRunner"
    p = beam.Pipeline(options=options)
    (p | "Read" >> beam.Create(inputs)
     | "Solve" >> beam.Map(solve)
     | "Write" >> beam.io.WriteToText("results/simple/opt.txt"))#("gs://shibuya-dataflow-dataflow/results/simple.txt"))
    p.run()


if __name__ == '__main__':
    main()
