import attr
from clldutils.misc import slug
from clldutils.path import Path
from lingpy import *
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Language
from tqdm import tqdm


@attr.s
class OurLanguage(Language):
    Type = attr.ib(default=None)
    Coverage = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Date = attr.ib(default=None)
    Transcriber = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "mitterhoferbena"
    language_class = OurLanguage

    def split_forms(self, item, value):
        value = self.lexemes.get(value, value)
        return [self.clean_form(item, form) for form in value.split("/")]

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.
        """
        csv = csv2list(self.raw.posix("Wordlist.csv"), strip_lines=False)

        concept2id = {c.english: c.concepticon_id for c in self.conceptlist.concepts.values()}

        header, rest = csv[0], csv[1:]
        idx = 1

        with self.cldf as ds:
            D = {0: ["doculect", "concept", "form"]}
            for line in rest:
                tmp = dict(zip(header, line))
                concept = tmp["CONCEPT"]
                for language in self.languages:
                    if tmp[language["Name"]]:
                        D[idx] = [language["Name"], concept, tmp[language["Name"]]]
                        idx += 1
                ds.add_concept(ID=slug(concept), Name=concept, Concepticon_ID=concept2id[concept])

            wl = Wordlist(D)

            ds.add_sources(*self.raw.read_bib())
            ds.add_languages(id_factory=lambda l: l["Name"])
            for idx, language, concept, form in tqdm(
                wl.iter_rows("doculect", "concept", "form"), desc="cldfify", total=len(wl)
            ):
                ds.add_lexemes(
                    Language_ID=language,
                    Parameter_ID=slug(concept),
                    Value=form,
                    Form=form,
                    Source="Mitterhofer2013",
                    Loan=False,
                )
