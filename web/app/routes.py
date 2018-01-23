from flask import Flask, render_template
import os
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from pyepicsContainer.pyepics.initialise_db import CCStrace1


user = os.getenv('POSTGRES_USER')
passwd = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
host = '0.0.0.0'
# host = 'postgres'
port = '5432'
db_session = sessionmaker()

app = Flask(__name__)


def create_charts(data, width=1000, height=300):
    """
        Creates charts of a PV kept in the postgres DB
    """
    sum_src = ColumnDataSource(data)
    ydr_amp = Range1d(start=min(data['amp_vals'])*1.5, end=max(data['amp_vals'])*1.5)

    tools = ['pan', 'save', 'reset', 'box_zoom']

    amp_plot = figure(title='Postgres Data', y_range=ydr_amp, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  sizing_mode='scale_width')
    amp_plot.circle(x='points', y='amp_vals', source=sum_src)

    return column([amp_plot])


@app.route("/")
def chart():
    engine = create_engine(
            f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}',
            echo=True
        )
    db_session.configure(bind=engine)
    session = db_session()
    postgres_data = session.query(CCStrace1).order_by(CCStrace1.id.desc()).first()
    session.close()

    data = {
        'points': range(len(postgres_data.signal)),
        'amp_vals': postgres_data.signal,
    }
    plot = create_charts(data)
    script, div = components(plot)

    return render_template("chart.html", timestamp=postgres_data.time_created, the_div=div, the_script=script)


if __name__ == '__main__':
    app.run()
