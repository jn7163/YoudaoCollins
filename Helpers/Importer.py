from anki.importing import TextImporter
from aqt import mw

def ImportText(file,deck,model):
    # select deck
    did = mw.col.decks.id(deck)
    mw.col.decks.select(did)
    # set note type for deck
    m = mw.col.models.byName(model)
    deck = mw.col.decks.get(did)
    deck['mid'] = m['id']
    mw.col.decks.save(deck)
    # import into the collection
    ti = TextImporter(mw.col, file)
    ti.initMapping()
    ti.allowHTML = True
    ti.run()
