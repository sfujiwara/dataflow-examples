import apache_beam as beam


def add10(element):
    element["result"] = element["value"] + 10
    return element


options = beam.options.pipeline_options.PipelineOptions()
gcloud_options = options.view_as(beam.options.pipeline_options.GoogleCloudOptions)
gcloud_options.job_name = "unko"
gcloud_options.project = "kaggle-playground"
gcloud_options.staging_location = "gs://kaggle-playground-dataflow/staging"
gcloud_options.temp_location = "gs://kaggle-playground-dataflow/temp"
options.view_as(beam.options.pipeline_options.StandardOptions).runner = "DataflowRunner"

p = beam.Pipeline(options=options)

inputs = [
    {"key": 0, "value": 0},
    {"key": 1, "value": 0},
    {"key": 2, "value": 2},
    {"key": 3, "value": 3},
    {"key": 4, "value": 4},
]

(p | "Read" >> beam.Create(inputs)
   | "Add10" >> beam.Map(add10)
   | "Write" >> beam.io.WriteToText("gs://kaggle-playground-dataflow/resutls/simple.txt"))

# p.run().wait_until_finish()
p.run()
