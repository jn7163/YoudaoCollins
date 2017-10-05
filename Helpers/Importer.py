from anki.importing import Importers, TextImporter
from aqt import mw
from aqt.importing import importFile
from aqt.utils import getFile, showText

from ..settings import settings


def ImportToAnki(model_name, import_to_deck, *args, **kwargs):
    # get file
    file = kwargs.get("file", None)
    if not file:
        file = getFile(mw, _("Import"), None, key="import", filter=Importers[0][0])
    if not file:
        return
    file = str(file)

    # check default model
    try:
        model = mw.col.models.byName(model_name)
        if not model:
            raise Exception("没有找到【{}】".format(model_name))
    except:
        importFile(mw, settings.deck_template_file)
        try:
            model = mw.col.models.byName(model_name)
        except:
            model = None

    importer = TextImporter(mw.col, file)
    importer.delimiter = "\t"
    importer.importMode = 0
    importer.allowHTML = True

    did = mw.col.decks.id(import_to_deck)
    mw.col.conf['curDeck'] = did

    mw.col.decks.select(did)
    importer.mapping = ['单词']
    importer.run()
    mw.reset()
    txt = _("Importing complete.") + "\n"
    if importer.log:
        txt += "\n".join(importer.log)
    showText(txt)
