from flask import render_template, Flask
from mastercontroller import start

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_html():
	return "Foo"

@app.route('/test', methods=['GET'])
def render_html():
	return render_template('webUI/index.html')

@app.route('/start', methods=['POST'])
def start_app(request):
	# lägg till python app.py längst ner i userdata
	if request.is_ajax():
		try:
			angle_start = request.POST['startAngle']
			angle_stop = request.POST['endAngle']
			n_angles = request.POST['nrAngle']
			nodes = request.POST['nodes']
			levels = request.POST['levels']
			slave_list = start(angle_start, angle_stop, n_angles)
		except e:
			return e
	return slave_list

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)