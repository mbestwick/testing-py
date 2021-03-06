"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from random import choice

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?

    Both true:
    >>> is_mel("Mel Melitpolski", "mel@ubermelon.com")
    True

    Just email true, name false:
    >>> is_mel("Random Person", "mel@ubermelon.com")
    True

    Just email false, name true:
    >>> is_mel("Mel Melitpolski", "random@gmail.com")
    True

    Both false:
    >>> is_mel("Random Person", "random@gmail.com")
    False

    Random capital letters:
    >>> is_mel("MEl Melitpolski", "mel@UBERmelon.com")
    True

    Just mel:
    >>> is_mel("Mel", "mel@UBERmelon.com")
    True

    """

    return "mel" in name.lower() or email.lower() == "mel@ubermelon.com"


def most_and_least_common_type(treats):
    """Given list of treats, return most and least common treat types.

    Return most and least common treat types in tuple of format (most, least).


    Main has 3, drink has 1:
    >>> most_and_least_common_type([{'type': 'main'}, {'type': 'drink'}, {'type': 'dessert'}, {'type': 'main'}, {'type': 'dessert'}, {'type': 'main'}])
    ('main', 'drink')

    Same as previous, but mixed up
    >>> most_and_least_common_type([{'type': 'main'}, {'type': 'dessert'}, {'type': 'main'}, {'type': 'dessert'}, {'type': 'drink'}, {'type': 'main'}])
    ('main', 'drink')

    Only one item:
    >>> most_and_least_common_type([{'type': 'main'}])
    ('main', 'main')

    Two items:
    >>> most_and_least_common_type([{'type': 'main'}, {'type': 'dessert'}])
    ('dessert', 'dessert')

    Tie for main and dessert with 2:
    >>> most_and_least_common_type([{'type': 'main'}, {'type': 'dessert'}, {'type': 'dessert'}, {'type': 'main'}, {'type': 'drink'}])
    ('dessert', 'drink')

    Empty list:
    >>> most_and_least_common_type([])
    (None, None)


    """

    types = {}

    # Count number of each type
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for treat_type, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = treat_type

        if least_count is None or count < least_count:
            least_count = count
            least_type = treat_type

    return (most_type, least_type)


def get_treats():
    """Return treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


def white_elephant(gifts):
    """ Plays a white elephant game with a given dictionary of guests and gifts


    >>> white_elephant({})
    {}

    >>> white_elephant({'Leslie': 'stuffed dog'})
    {'Leslie': 'stuffed dog'}

    >>> len({'Leslie': 'stuffed dog', 'Joel': 'crossword puzzle', 'Meggie': 'candy', 'Bonnie': 'cat food', 'Katie': 'rubiks cube', 'Anges': 'starbucks gift card', 'Henry': 'graphic t-shirt', 'Sarah': 'christmas mug'}) == len(white_elephant({'Leslie': 'stuffed dog', 'Joel': 'crossword puzzle', 'Meggie': 'candy', 'Bonnie': 'cat food', 'Katie': 'rubiks cube', 'Anges': 'starbucks gift card', 'Henry': 'graphic t-shirt', 'Sarah': 'christmas mug'}))
    True

    """


    gift_list = [gift for gift in gifts.values()]

    new_gifts = {person: None for person in gifts.keys()}

    for person, gift in new_gifts.items():
        new_gift = choice(gift_list)
        gift_list.remove(new_gift)
        new_gifts[person] = new_gift

    return new_gifts




@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run()
