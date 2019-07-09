import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions


def main():

    options = PipelineOptions()

    # setup options
    setup_options = options.view_as(SetupOptions)
    setup_options.setup_file = './setup.py'

    # gcloud options
    gcloud_options = options.view_as(GoogleCloudOptions)
    gcloud_options.job_name = "mecab-example"
    gcloud_options.project = "kaggle-playground"
    gcloud_options.staging_location = "gs://kaggle-playground-dataflow/staging"
    gcloud_options.temp_location = "gs://kaggle-playground-dataflow/temp"

    # standard options
    options.view_as(StandardOptions).runner = "DataflowRunner"

    inputs = [0, 1, 2]

    p = beam.Pipeline(options=options)

    (p | "Read" >> beam.Create(inputs))
    p.run()


if __name__ == '__main__':
    main()
