import uuid
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import WorkerOptions


PROJECT_ID = 'kaggle-playground'


def wakati(text):
    # type: (str) -> str
    """
    Parameters
    ----------
    text:
        Text to be wakati.

    Returns
    -------
    result:
        Text applied wakati.
    """

    import logging
    import MeCab
    neologd_path = '/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd/'
    logging.info('NEologd path: {}'.format(neologd_path))
    m = MeCab.Tagger('-d {}'.format(neologd_path))
    result = m.parse(text)
    logging.info(result)
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

    # worker options
    worker_options = options.view_as((WorkerOptions))
    worker_options.disk_size_gb = 100
    worker_options.machine_type = 'n1-standard-2'

    # standard options
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    # sample input
    inputs = [
        'すもももももももものうち',
        '私は元気です',
        '8月3日に放送された「中居正広の金曜日のスマイルたちへ」(TBS系)で、1日たった5分でぽっこりおなかを解消するというダイエット方法を紹介。キンタロー。のダイエットにも密着。'
    ]

    p = beam.Pipeline(options=options)

    (p | 'Read' >> beam.Create(inputs)
       | 'Wakati' >> beam.Map(wakati))
    p.run()


if __name__ == '__main__':
    main()
