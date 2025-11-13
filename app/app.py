# app.py

from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from random import randint
import app.exporter as exporter

# Creating a Flask app instance
app = Flask(__name__)

# Automatically instruments Flask app to enable tracing
FlaskInstrumentor().instrument_app(app)

# Retrieving a tracer from the custom exporter
tracer = exporter.service1_tracer

@app.route("/rolldice")
def roll_dice(parent_span=None):
    # Starting a new span for the dice roll. If a parent span is provided, link to its span context.
    with tracer.start_as_current_span("roll_dice_span",
          links=[trace.Link(parent_span.get_span_context())] if parent_span else None) as span:
        # Spans can be created with zero or more Links to other Spans that are related.
        # Links allow creating connections between different traces
        return str(roll())

@app.route("/roll_with_link")
def roll_with_link():
    # Starting a new 'parent_span' which may later link to other spans
    with tracer.start_as_current_span("parent_span") as parent_span:
        # A common scenario is to correlate one or more traces with the current span.
        # This can help in tracing and debugging complex interactions across different parts of the app.
        result = roll_dice(parent_span)
        return f"Dice roll result (with link): {result}"

def roll():
    # Function to generate a random number between 1 and 6
    return randint(1, 6)

if __name__ == "__main__":
    # Starting the Flask server on the specified PORT and enabling debug mode
    app.run(port=8080, debug=True)