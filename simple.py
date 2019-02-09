import apache_beam as beam


def add10(element):
    element["result"] = element["value"] + 10
    return element


p = beam.Pipeline()

inputs = [
    {"key": 0, "value": 0},
    {"key": 1, "value": 0},
    {"key": 2, "value": 2},
    {"key": 3, "value": 3},
    {"key": 4, "value": 4},
]

(p | "Read" >> beam.Create(inputs)
   | "Add10" >> beam.Map(add10)
   | "Write" >> beam.io.WriteToText("results/simple/simple.txt"))

p.run().wait_until_finish()
