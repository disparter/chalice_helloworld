from chalice import Chalice, BadRequestError
from eliot import start_action
from eliot.stdlib import EliotHandler

app = Chalice(app_name='helloworld')
app.log.addHandler(EliotHandler())
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/cities/{city}')
def state_of_city(city):
    with start_action(action_type="helloworld:state_of_city", city=city):
        try:
            return {'state': CITIES_TO_STATE[city]}
        except KeyError:
            raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
                city, ', '.join(CITIES_TO_STATE.keys())))


def test_state_of_city():
    assert state_of_city('seattle') == {'state': 'WA'}


def test_index():
    assert index() == {'hello': 'world'};


