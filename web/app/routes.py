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


def create_charts(data):
    """
        Creates charts of a PV kept in the postgres DB
    """
    sum_src = ColumnDataSource(data)
    plot_data = np.array(data['amp_vals']).reshape((1024, 1024))

    tools = ['pan', 'save', 'reset', 'box_zoom']

    amp_plot = figure(x_range=(0, 1024), y_range=(0, 1024))
    amp_plot.image(image=[plot_data], x=0, y=0, dw=1024, dh=1024, palette='Spectral11')

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
