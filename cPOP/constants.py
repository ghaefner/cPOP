
PATH_TO_DATA = "cPOP/data/by_tag_year.csv"
PATH_TO_TAG_MODEL = "cPOP/models/tag_classifier_model.pkl"
PATH_TO_PLOT_FOLDER = "cPOP/plots/"

PATH_TO_DB = 'sqlite:///mydatabase.db'


class Columns:
    YEAR = "year"
    TAG = "tag"
    COUNT = "number"
    YEAR_COUNT = "year_total"

    TAG_COUNT = "tag_total"
    FRACTION = "fraction"

    TAG_GROUP = "tag_group"

    MEASURE = "measure"
    ID = "table_id"


DICT_LANGUAGES = {
    "javascript": ['^javascript'],
    "java": ['^java(?!script).*'],
    "c#": [r'^c#.*'],
    "php": [r'^php.*'],
    "android": [r'.*android.*'],
    "python": [r'.*apache.*', r'^django.*', r'.*python.*', r'.*pandas.*', r'.*numpy.*', r'.*matplotlib.*', r'.*seaborn.*'],
    "ruby": [r'^ruby$'],
    "c++": [r'^c\+\+.*'],
    "objective-c": [r'.*objective-c.*'],
    "c": [r'^c$'],
    ".net": [r'^\.net.*'],
    "sql": [r'.*sql*'],
    "r": [r'^r$',r'^dplyr.*', r'^tidy.*', r'^shiny.*'],
    "swift": [r'^swift'],
    "html": [r'^html.*'],
    "css": [r'^css.*'],
    "perl": [r'^perl.*'],
    "typescript": [r'^typescript.*']
}