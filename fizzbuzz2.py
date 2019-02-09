import apache_beam as beam


p = beam.Pipeline()

input_pc = (p | "Read" >> beam.Create(range(50)))

fizzbuzz = (input_pc | "FizzBuzz" >> beam.Filter(lambda row: row % 15 == 0))
fizz = (input_pc | "Fizz" >> beam.Filter(lambda row: row % 3 == 0 and row % 15 != 0))
buzz = (input_pc | "Buzz" >> beam.Filter(lambda row: row % 5 == 0 and row % 15 != 0))

(fizz | "Write Fizz" >> beam.io.WriteToText("results/fizzbuzz2/fizz.txt"))
(buzz | "Write Buzz" >> beam.io.WriteToText("results/fizzbuzz2/buzz.txt"))
(fizzbuzz | "Write FizzBuzz" >> beam.io.WriteToText("results/fizzbuzz2/fizzbuzz.txt"))

p.run().wait_until_finish()
