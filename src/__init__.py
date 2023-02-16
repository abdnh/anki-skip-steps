import time
from pathlib import Path
from aqt.qt import *
from aqt import mw, gui_hooks
from aqt.utils import showWarning
from anki.cards import Card
from anki.collection import Collection

ADDON_NAME = "Skip (Re)Learning steps"
ADDON_DIR = Path(__file__).parent


def on_col_did_load(col: Collection) -> None:
    if col.sched.version != 3:
        showWarning(
            f"The {ADDON_NAME} add-on only works with the V3 scheduler.",
            title=ADDON_NAME,
        )


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    last_review_time = time.time() - (
        mw.col.db.scalar(
            "select id from revlog where cid = ? order by id desc limit 1",
            card.id,
        )
        // 1000
    )
    relearning_steps = [
        d * 60
        for d in mw.col.decks.config_dict_for_deck_id(mw.reviewer.card.did)["lapse"][
            "delays"
        ]
    ]
    js = """
    <script>
        globalThis.lastReviewTime = %s;
        globalThis.relearningSteps = %s;
    </script>
    """ % (
        last_review_time,
        relearning_steps,
    )
    return text + js


def override_custom_scheduling_code() -> None:
    with open(ADDON_DIR / "custom_scheduling.js", "r", encoding="utf-8") as file:
        mw.col.set_config("cardStateCustomizer", file.read())


def add_menu() -> None:
    menu = QMenu(ADDON_NAME, mw)
    action = QAction("Override custom scheduling code", menu)
    qconnect(action.triggered, override_custom_scheduling_code)
    menu.addAction(action)
    mw.form.menuTools.addMenu(menu)


def register_hooks() -> None:
    gui_hooks.card_will_show.append(on_card_will_show)
    gui_hooks.collection_did_load.append(on_col_did_load)


add_menu()
register_hooks()
