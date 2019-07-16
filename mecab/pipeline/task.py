import uuid
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions


PROJECT_ID = 'kaggle-playground'


def wakati(text):
    import MeCab
    m = MeCab.Tagger("-Ochasen")
    result = m.parse(text)
    print(result)
    return result


def main():

    options = PipelineOptions()

    # setup options
    setup_options = options.view_as(SetupOptions)
    setup_options.setup_file = './setup.py'

    # gcloud options
    gcloud_options = options.view_as(GoogleCloudOptions)
    gcloud_options.job_name = 'mecab-example-{}'.format(uuid.uuid4())
    gcloud_options.project = '{}'.format(PROJECT_ID)
    gcloud_options.staging_location = 'gs://{}-dataflow/staging'.format(PROJECT_ID)
    gcloud_options.temp_location = 'gs://{}-dataflow/temp'.format(PROJECT_ID)

    # standard options
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    # sample input
    inputs = [
        'すもももももももものうち',
        '私は元気です',
    ]

    p = beam.Pipeline(options=options)

    (p | 'Read' >> beam.Create(inputs)
       | 'Wakati' >> beam.Map(wakati)
    )
    p.run()


if __name__ == '__main__':
    main()
