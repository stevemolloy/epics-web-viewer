from flask import Flask, render_template
import base64
import io
import os
from matplotlib import pyplot as plt
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from pyepicsContainer.pyepics.initialise_db import BPMSumAmplitude, BPMSumPhase


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
        Creates charts of the BPM-sum phase & amplitude
    """
    sum_src = ColumnDataSource(data)
    ydr_amp = Range1d(start=0, end=max(data['amp_vals'])*1.5)
    phs_rms = np.std(data['phs_vals'])
    lims = 5*phs_rms
    if lims > 180:
        lims = 180
    ydr_phs = Range1d(start=min(data['phs_vals'])-lims, end=max(data['phs_vals'])+lims)

    tools = ['pan', 'save', 'reset', 'box_zoom']

    sum_plot = figure(title='BPM Sum Data', y_range=ydr_amp, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  sizing_mode='scale_width')
    sum_plot.circle(x='points', y='amp_vals', source=sum_src)

    phs_plot = figure(title='BPM Phase Data', y_range=ydr_phs, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  sizing_mode='scale_width')
    phs_plot.circle(x='points', y='phs_vals', source=sum_src)

    return column([sum_plot, phs_plot])


@app.route("/")
def chart():
    engine = create_engine(
            f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}',
            echo=True
        )
    db_session.configure(bind=engine)
    session = db_session()
    sumamp = session.query(BPMSumAmplitude).order_by(BPMSumAmplitude.id.desc()).first()
    sumphase = session.query(BPMSumPhase).order_by(BPMSumPhase.id.desc()).first()
    session.close()

    data = {
        'points': range(len(sumamp.signal)),
        'amp_vals': sumamp.signal,
        'phs_vals': sumphase.signal,
    }
    plot = create_charts(data)
    script, div = components(plot)

    return render_template("chart.html", timestamp=sumamp.time_created, the_div=div, the_script=script)


if __name__ == '__main__':
    app.run()
