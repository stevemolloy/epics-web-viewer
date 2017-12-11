from flask import Flask, render_template
import base64
import io
from matplotlib import pyplot as plt
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == '__main__':
    app.run()
