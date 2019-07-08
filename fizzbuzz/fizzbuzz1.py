import apache_beam as beam


def fizzbuzz(element):
    if element % 15 == 0:
        yield beam.pvalue.TaggedOutput("FizzBuzz", element)
    elif element % 3 == 0:
        yield beam.pvalue.TaggedOutput("Fizz", element)
    elif element % 5 == 0:
        yield beam.pvalue.TaggedOutput("Buzz", element)


p = beam.Pipeline()

fizz, buzz, fizzbuzz = (p | "Read" >> beam.Create(range(50))
                          | "FizzBuzz" >> beam.ParDo(fizzbuzz).with_outputs("Fizz", "Buzz", "FizzBuzz"))

(fizz | "Write Fizz" >> beam.io.WriteToText("results/fizzbuzz1/fizz.txt"))
(buzz | "Write Buzz" >> beam.io.WriteToText("results/fizzbuzz1/buzz.txt"))
(fizzbuzz | "Write FizzBuzz" >> beam.io.WriteToText("results/fizzbuzz1/fizzbuzz.txt"))

p.run().wait_until_finish()
