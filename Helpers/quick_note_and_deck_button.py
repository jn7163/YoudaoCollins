model_buttons = [
    {"label": '有道柯林斯', "name": '有道柯林斯'},
]
deck_buttons = [
    {"label": '单词', 'name': '单词'},
]

from anki.hooks import runHook
from anki.lang import _
from anki.utils import isMac
from aqt.modelchooser import QHBoxLayout, QPushButton, QShortcut, QKeySequence


def setup_buttons(chooser, buttons, text, do_function):
    u"""Set up the note type and deck buttons."""
    bhbl = QHBoxLayout()
    if not isMac:
        bhbl.setSpacing(0)
    for button_item in buttons:
        b = QPushButton(button_item["label"])
        b.setToolTip(
            _("Change {what} to {name}.").format(
                what=text, name=button_item["name"]))
        l = lambda s=chooser, nn=button_item["name"]: do_function(s, nn)
        try:
            s = QShortcut(
                QKeySequence(_(button_item["shortcut"])), chooser.widget)
        except KeyError:
            pass
        else:
            # s.connect(s, SIGNAL("activated()"), l)
            s.activated.connect(l)
        if isMac:
            b.setStyleSheet("padding: 5px; padding-right: 7px;")
        bhbl.addWidget(b)
        # chooser.connect(b, SIGNAL("clicked()"), l)
        b.clicked.connect(l)
    chooser.addLayout(bhbl)


def change_model_to(chooser, model_name):
    """Change to model with name model_name"""
    # Mostly just a copy and paste from the bottom of onModelChange()
    m = chooser.deck.models.byName(model_name)
    chooser.deck.conf['curModel'] = m['id']
    # When you get a “TypeError: 'NoneType' object has no attribute
    # '__getitem__'” directing you here, the most likely explanation
    # is that the model names are not set up correctly in the
    # model_buttons list of dictionaries above.
    cdeck = chooser.deck.decks.current()
    cdeck['mid'] = m['id']
    chooser.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    chooser.mw.reset()


def change_deck_to(chooser, deck_name):
    chooser.deck.setText(deck_name)
