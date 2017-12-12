from flask import Flask, render_template
import base64
import io
import os
from matplotlib import pyplot as plt
from bokeh.models import FactorRange, Range1d
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyepicsContainer.pyepics.initialise_db import BPMSumAmplitude, BPMSumPhase


user = os.getenv('POSTGRES_USER')
passwd = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
host = '0.0.0.0'
# host = 'postgres'
port = '5432'
db_session = sessionmaker()

app = Flask(__name__)


def create_bar_chart(data, width=1000, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=[str(x) for x in data['points']])
    ydr = Range1d(start=0, end=max(data['vals'])*1.5)

    tools = ['pan', 'save', 'reset', 'box_zoom']

    plot = figure(title='BPM Sum Data', y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  sizing_mode='scale_width')

    plot.circle(x='points', y='vals', source=source)

    return plot


@app.route("/bokeh/")
def chart():
    engine = create_engine(
            f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}',
            echo=True
        )
    db_session.configure(bind=engine)
    session = db_session()
    obj = session.query(BPMSumAmplitude).order_by(BPMSumAmplitude.id.desc()).first()
    print(obj.signal)

    data = {
        'points': range(len(obj.signal)),
        'vals': obj.signal,
    }
    plot = create_bar_chart(data)
    script, div = components(plot)

    session.close()

    return render_template("chart.html", the_div=div, the_script=script)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/matplotlib')
def build_plot():
    img = io.BytesIO()

    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == '__main__':
    app.run()
